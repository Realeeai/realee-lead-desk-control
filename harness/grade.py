"""Grade Lead Desk runs, and check that the worked examples add up.

    python harness/grade.py examples              re-add every SCORE line in lead-desk/examples.md
    python harness/grade.py run control/run-1     grade one run against the key in questions.md

Points come from the table in lead-desk/rules.md (the only file with numbers), so a
digit changed in an example, in a run, or in the rules shows up here by name.
Standard library only. Exit code 1 when anything fails.
"""
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RULES = REPO / "lead-desk" / "rules.md"
EXAMPLES = REPO / "lead-desk" / "examples.md"
QUESTIONS = REPO / "questions.md"

TIERS = ("HOT", "WARM", "COLD", "DISQUALIFY", "FLAG")
TERM = re.compile(r"\b(\d[a-z](?:-lite)?)\(\s*([+\-−]\s*\d+)\s*\)")
TOTAL = re.compile(r"=\s*(\d+)\s*/\s*10")
ANSWER = re.compile(r"ANSWER:\s*TIER\s*=\s*([A-Za-z]+)\s*\|\s*NEXT\s*=\s*(.+)", re.I)


def _int(text):
    return int(text.replace("−", "-").replace(" ", ""))


def rule_points():
    """Rule ID -> points, read from the scoring table in rules.md."""
    points = {}
    row = re.compile(r"^\|\s*\*\*(\d[a-z](?:-lite)?)\*\*\s*\|.*\|\s*([+\-−]\d+)\s*\|\s*$")
    for line in RULES.read_text(encoding="utf-8").splitlines():
        m = row.match(line)
        if m:
            points[m.group(1)] = _int(m.group(2))
    if not points:
        sys.exit(f"No scoring table found in {RULES}")
    return points


def tier_for(total):
    """rules.md section 3: 8-10 HOT, 5-7 WARM, 0-4 COLD."""
    return "HOT" if total >= 8 else "WARM" if total >= 5 else "COLD"


def check_score_line(line, points):
    """Problems with one SCORE line, as plain sentences. Empty list = it adds up."""
    clean = line.replace("*", "")
    if "not scored" in clean:
        return []
    terms = TERM.findall(clean)
    total = TOTAL.search(clean)
    if not terms or not total:
        return [f"SCORE line doesn't show the addition: {line.strip()}"]
    problems = []
    running = 0
    for rule, written in terms:
        value = _int(written)
        running += value
        if rule not in points:
            problems.append(f"{rule} is not a scoring rule in rules.md")
        elif points[rule] != value:
            problems.append(f"{rule} written as {value:+d}, rules.md says {points[rule]:+d}")
    expected = max(0, min(10, running))
    if int(total.group(1)) != expected:
        problems.append(f"terms add to {expected}, line says {total.group(1)}")
    return problems


def check_examples():
    points = rule_points()
    text = EXAMPLES.read_text(encoding="utf-8")
    sections = re.split(r"^## (Example \d+[^\n]*)$", text, flags=re.M)[1:]
    failures = 0
    for title, body in zip(sections[::2], sections[1::2]):
        name = title.split(" — ")[0]
        problems = []
        tier = re.search(r"\*\*TIER:\*\*\s*([A-Z]+)", body)
        score = re.search(r"^.*\*\*SCORE:\*\*.*$", body, flags=re.M)
        if not tier or not score:
            problems.append("missing TIER or SCORE line")
        else:
            tier = tier.group(1)
            problems += check_score_line(score.group(0), points)
            total = TOTAL.search(score.group(0).replace("*", ""))
            if tier == "DISQUALIFY" and "not scored" not in score.group(0):
                problems.append("DISQUALIFY must read 'not scored (<rule>)'")
            if total and tier in ("HOT", "WARM", "COLD") and tier_for(int(total.group(1))) != tier:
                problems.append(f"total {total.group(1)} maps to {tier_for(int(total.group(1)))}, example says {tier}")
            if total:
                for quoted in re.findall(r"(?:Score|Provisional)\s+(\d+)/10", body):
                    if quoted != total.group(1):
                        problems.append(f"alert says {quoted}/10, SCORE line says {total.group(1)}/10")
        print(f"{name}: {'ok' if not problems else 'FAIL'}")
        for p in problems:
            print(f"  - {p}")
        failures += bool(problems)
    print(f"\n{len(sections) // 2 - failures}/{len(sections) // 2} examples add up")
    return failures == 0


def parse_questions():
    """The shared prompt and each question's lead text and expected tier, from questions.md."""
    text = QUESTIONS.read_text(encoding="utf-8")
    template = re.search(r"## The prompt both arms get.*?```text\n(.*?)\n```", text, flags=re.S)
    if not template or "{lead}" not in template.group(1):
        sys.exit("questions.md: no shared prompt with a {lead} slot")
    questions = []
    for m in re.finditer(r"^### (Q\d+)[^\n]*\n(.*?)(?=^### Q\d+|^## |\Z)", text, flags=re.S | re.M):
        qid, body = m.group(1), m.group(2)
        lead = re.search(r"```text\n(.*?)\n```", body, flags=re.S)
        tier = re.search(r"\*\*Expected tier:\*\*\s*([A-Z]+)", body)
        if not lead or not tier or tier.group(1) not in TIERS:
            sys.exit(f"questions.md: {qid} needs a ```text lead block and an **Expected tier:**")
        questions.append({"id": qid, "lead": lead.group(1), "expected": tier.group(1)})
    return template.group(1), questions


def grade_run(run_dir):
    points = rule_points()
    _, questions = parse_questions()
    run_dir = Path(run_dir)
    passed = 0
    print(f"Run: {run_dir.as_posix()}\n")
    print("| Q | Expected | Answered | Tier | Addition shown and correct | Seconds | Output tokens |")
    print("|---|----------|----------|------|----------------------------|---------|---------------|")
    for q in questions:
        path = run_dir / f"{q['id'].lower()}.json"
        if not path.exists():
            print(f"| {q['id']} | {q['expected']} | (no file) | FAIL | | | |")
            continue
        raw = json.loads(path.read_text(encoding="utf-8"))
        reply = (raw.get("result") or "").replace("*", "").replace("`", "")
        answers = ANSWER.findall(reply)
        got = answers[-1][0].upper() if answers else "(no ANSWER line)"
        ok = got == q["expected"]
        passed += ok
        score_lines = [l for l in reply.splitlines() if re.match(r"\s*-?\s*SCORE\s*:", l)]
        if not score_lines:
            addition = "not shown"
        else:
            problems = check_score_line(score_lines[0], points)
            addition = "yes" if not problems else "no: " + "; ".join(problems)
        seconds = raw.get("duration_ms", 0) / 1000
        tokens = (raw.get("usage") or {}).get("output_tokens", "")
        print(f"| {q['id']} | {q['expected']} | {got} | {'PASS' if ok else 'FAIL'} | {addition} | {seconds:.1f} | {tokens} |")
    print(f"\nTier score: {passed}/{len(questions)}")
    return passed == len(questions)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) >= 2 and sys.argv[1] == "examples":
        sys.exit(0 if check_examples() else 1)
    if len(sys.argv) == 3 and sys.argv[1] == "run":
        sys.exit(0 if grade_run(sys.argv[2]) else 1)
    sys.exit(__doc__)
