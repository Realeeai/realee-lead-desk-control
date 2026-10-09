"""Run one arm of the control test: every question in questions.md, in order, one fresh session each.

    python harness/run_arms.py control 1
    python harness/run_arms.py treatment 1
    python harness/run_arms.py control 1 my-questions.md     your own questions file, same format;
                                                               writes <arm>/my-questions-run-1/

control    system prompt = harness/base-system-prompt.txt, nothing else
treatment  system prompt = the same line + the lead-desk files in LOAD_ORDER

Writes <arm>/run-<n>/:
  q<N>.json          the CLI's JSON output, byte for byte (stderr beside it if there was any)
  system-prompt.txt  exactly what was passed as the system prompt
  run-info.json      model, effort, CLI version, the command, the repo commit, start and end times
  transcript.md      each prompt and reply, rendered from the .json files with no edits

To re-run against the folder exactly as a past run saw it, check out the commit in its
run-info.json (run 1 predates that field; it ran at commit 0cd68c5).

A question that times out gets q<N>.timeout.txt instead of q<N>.json, grades as a fail, and the
run continues. Refuses to overwrite a run folder: a bad run is kept, and the next run gets a new
number (treatment/run-5 is one: the runner crashed on a timeout before this handling existed).
Needs Claude Code on PATH and logged in. Standard library only.
"""
import datetime
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from grade import QUESTIONS, REPO, parse_questions

MODEL = "claude-opus-5-5"
EFFORT = "high"
TIMEOUT = 600  # seconds per question
LOAD_ORDER = [
    "README.md",
    "identity.md",
    "rules.md",
    "examples.md",
    "reference/icp.md",
    "reference/output-format.md",
]
# --safe-mode: no CLAUDE.md, memory, skills, plugins or hooks. --tools "": no tools.
# --strict-mcp-config with no config: no MCP servers. Each question is its own session.
FLAGS = [
    "-p", "--safe-mode", "--tools", "", "--strict-mcp-config", "--no-session-persistence",
    "--model", MODEL, "--effort", EFFORT, "--output-format", "json",
]


def system_prompt(arm):
    base = (REPO / "harness" / "base-system-prompt.txt").read_text(encoding="utf-8").strip()
    if arm == "control":
        return base + "\n"
    parts = [base, "", "The following folder is loaded for this conversation.", ""]
    for name in LOAD_ORDER:
        body = (REPO / "lead-desk" / name).read_text(encoding="utf-8").strip()
        parts += [f'<file path="lead-desk/{name}">', body, "</file>", ""]
    return "\n".join(parts)


def fence(text):
    """A code fence longer than any backtick run inside text, so replies render unchanged."""
    longest, run = 0, 0
    for ch in text:
        run = run + 1 if ch == "`" else 0
        longest = max(longest, run)
    return "`" * max(4, longest + 1)


def main():
    if len(sys.argv) not in (3, 4) or sys.argv[1] not in ("control", "treatment") or not sys.argv[2].isdigit():
        sys.exit(__doc__)
    arm, number = sys.argv[1], sys.argv[2]
    questions_path = Path(sys.argv[3]).resolve() if len(sys.argv) == 4 else QUESTIONS
    claude = shutil.which("claude")
    if not claude:
        sys.exit("Claude Code (`claude`) is not on PATH")
    run_name = f"run-{number}" if questions_path == QUESTIONS else f"{questions_path.stem}-run-{number}"
    out = REPO / arm / run_name
    if out.exists():
        sys.exit(f"{out} already exists. Runs are never overwritten; use the next number.")

    template, questions = parse_questions(questions_path)
    out.mkdir(parents=True)
    prompt_file = out / "system-prompt.txt"
    prompt_file.write_text(system_prompt(arm), encoding="utf-8", newline="\n")
    version = subprocess.run([claude, "--version"], capture_output=True, text=True).stdout.strip()
    git = ["git", "-C", str(REPO)]
    commit = subprocess.run([*git, "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    uncommitted = subprocess.run([*git, "status", "--porcelain", "--", "lead-desk", "harness", str(questions_path)],
                                 capture_output=True, text=True).stdout.strip()
    info = {
        "arm": arm,
        "run": int(number),
        "questions_file": questions_path.relative_to(REPO).as_posix() if questions_path.is_relative_to(REPO) else questions_path.name,
        "model": MODEL,
        "effort": EFFORT,
        "claude_code_version": version,
        "repo_commit": commit,
        "uncommitted_changes_to_folder_questions_or_harness": uncommitted.splitlines(),
        "command": ["claude", *FLAGS, "--system-prompt-file", f"{arm}/{run_name}/system-prompt.txt"],
        "prompt_delivery": "stdin, one fresh session per question, from an empty temporary folder",
        "questions": [q["id"] for q in questions],
        "started_at": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
    }

    transcript = [f"# {arm} {run_name}", "",
                  f"Rendered from the q<N>.json files in this folder, no edits. Model `{MODEL}`, effort `{EFFORT}`, {version}.",
                  "System prompt: `system-prompt.txt` in this folder.", ""]
    for q in questions:
        prompt = template.replace("{lead}", q["lead"])
        stem = q["id"].lower()
        try:
            with tempfile.TemporaryDirectory(prefix="lead-desk-run-") as empty:
                done = subprocess.run(
                    [claude, *FLAGS, "--system-prompt-file", str(prompt_file)],
                    input=prompt.encode("utf-8"), capture_output=True, cwd=empty, timeout=TIMEOUT,
                )
        except subprocess.TimeoutExpired:
            # Recorded, not retried: a timeout counts as a failed answer (no qN.json) and the run goes on.
            stats = f"timed out after {TIMEOUT} s, no answer"
            (out / f"{stem}.timeout.txt").write_text(stats + "\n", encoding="utf-8", newline="\n")
            transcript += [f"## {q['id']}", "", f"_{stats}_", ""]
            print(f"{arm} run {number} {q['id']}: {stats}", flush=True)
            continue
        (out / f"{stem}.json").write_bytes(done.stdout)
        if done.stderr.strip():
            (out / f"{stem}.stderr.txt").write_bytes(done.stderr)
        try:
            raw = json.loads(done.stdout.decode("utf-8"))
            reply = raw.get("result") or ""
            stats = f"{raw.get('duration_ms', 0) / 1000:.1f} s · {(raw.get('usage') or {}).get('output_tokens', '?')} output tokens · session {raw.get('session_id', '?')}"
        except (ValueError, UnicodeDecodeError):
            reply, stats = done.stdout.decode("utf-8", "replace"), f"exit code {done.returncode}, output was not JSON"
        f_prompt, f_reply = fence(prompt), fence(reply)
        transcript += [f"## {q['id']}", "", f"_{stats}_", "", "**Prompt (sent on stdin, exact):**", "",
                       f_prompt + "text", prompt, f_prompt, "", "**Reply:**", "", f_reply + "text", reply, f_reply, ""]
        print(f"{arm} run {number} {q['id']}: {stats}", flush=True)

    info["finished_at"] = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    (out / "run-info.json").write_text(json.dumps(info, indent=2) + "\n", encoding="utf-8", newline="\n")
    (out / "transcript.md").write_text("\n".join(transcript), encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
