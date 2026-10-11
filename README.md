# Realee Lead Desk — the control test

Clief Notes Weekly Comp #14, "The Control". Does a small specialist folder beat the same model with no folder? This repo holds the test: the folder, nine questions committed before any run, both arms' raw runs, and an honest results file.

**Headline** ([`results.md`](results.md)): on the nine questions committed before any run, the folder scored 8/9 and the bare model 4/9, identically in two runs. Then the operator read both arms and rewrote his rules: ask every lead the same questions, then score six weighted factors, and never pass a lead for its industry. Under the rewritten rules, the bare model's original answers score 7/9 without being re-run, and the first folder 5/9. The redesigned folder scores 9/9 on the rewritten rules, twice with identical scores, at about 2.2× the time per answer. Most of the folder's first lead came from rules the operator decided he didn't want.

## What's here

| Path | What it is |
|------|------------|
| [`lead-desk/`](lead-desk/) | The specialist folder: `identity.md`, `rules.md`, `examples.md`, `reference/` (including the intake script) and `README.md`. It asks every lead the same questions, then scores six weighted factors out of 100 into HOT / WARM / COLD / DISQUALIFY / FLAG, with the addition written out and the unanswered questions listed. The treatment arm loads this folder and nothing else |
| [`questions.md`](questions.md) | Nine questions with the expected tier, worked out by hand from the rules. Committed before any run (`0cd68c5`; see `git log -- questions.md`) and never edited |
| [`questions-after-review.md`](questions-after-review.md) | The same questions and prompt, keyed to the rules as they now stand, after the operator's two rounds of changes. Each changed key is marked with its reason. Both key files grade every run |
| [`control/`](control/) | Raw runs with no folder |
| [`treatment/`](treatment/) | Raw runs with the folder loaded |
| [`results.md`](results.md) | Question by question, ties and losses included, plus what we changed in the folder because of it |
| [`outside-check/`](outside-check/) | Three leads written by a blank session that never saw the folder, keyed before either arm ran on them |
| [`harness/`](harness/) | `run_arms.py` runs one arm; `grade.py` grades a run and re-adds the worked examples |

The answer keys and the runs sit outside `lead-desk/`, so the treatment never sees them.

## Re-run both arms

Needs Python 3.10+ and [Claude Code](https://docs.claude.com/en/docs/claude-code) on your PATH, logged in.

```bash
python harness/run_arms.py control 11
python harness/run_arms.py treatment 11
python harness/grade.py run control/run-11 questions-after-review.md
python harness/grade.py run treatment/run-11 questions-after-review.md
python harness/grade.py examples
```

Use any run number that doesn't exist yet; the runner never overwrites a run.

**Which folder each run saw.** Runs 1 and 2 used the folder as first committed (commit `0cd68c5`). Runs 3–7 used versions after the first two rounds of changes. Run 8 used the redesign. Runs 9 and 10 used the current folder. A treatment re-run at the latest commit should match runs 9 and 10; grade it with `questions-after-review.md`. To reproduce runs 1 and 2, `git switch --detach 0cd68c5` first, then run the same commands but grade without the last argument (`python harness/grade.py run treatment/run-11`); that commit has only the committed key. Each `run-info.json` from run 2 on records its commit.

**Your own question.** Copy the format of `questions.md` (the shared prompt, then `### X1` blocks with a `text` lead and an `**Expected tier:**` line) into a file, then pass that file as the last argument: `python harness/run_arms.py control 1 mine.md`, then `python harness/grade.py run control/mine-run-1 mine.md`.

## What's the same in both arms, and what isn't

- **Same:** model `claude-opus-5-5`, effort `high`, the exact prompt text in `questions.md`, the question order, one fresh session per question, no tools.
- **Different:** the system prompt. The control gets one line (`harness/base-system-prompt.txt`). The treatment gets that line plus the folder files: seven since the redesign (the intake script was added), six before. Each run folder keeps the exact text as `system-prompt.txt`.
- **Added by Claude Code to every call in both arms:** a one-line Agent SDK preamble, an environment block (working folder, platform, today's date) and the signed-in account's email. None of it is about leads. `--safe-mode`, `--tools ""` and `--strict-mcp-config` switch off memory files, skills, plugins, hooks, MCP servers and tools. See the limits in `results.md` for the one time this preamble leaked into an output.
- **Without Claude Code:** the control is a fresh claude.ai chat with no project; the treatment is a claude.ai project with the `lead-desk/` files uploaded. Paste each prompt from `questions.md` into its own new chat. claude.ai's own system prompt differs from the CLI's, so expect some drift.

## License

MIT
