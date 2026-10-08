# Realee Lead Desk — the control test

Clief Notes Weekly Comp #14, "The Control". Does a small specialist folder beat the same model with no folder? This repo holds the test: the folder, nine questions committed before any run, both arms' raw runs, and an honest results file.

**Headline** ([`results.md`](results.md)): on the nine questions, the folder scored 8/9 and the bare model 4/9, identically in both runs. On tier there was no question where the bare model was right and the folder wrong, and the one shared miss (Q9) taught the folder a rule. The folder costs about 20% more time and 50% more tokens per answer. Every disagreement went one way: with no folder, the model told the founder to book a call on 7 of 12 leads; the rules say 2.

## What's here

| Path | What it is |
|------|------------|
| [`lead-desk/`](lead-desk/) | The specialist folder: `identity.md`, `rules.md`, `examples.md`, `reference/`, `README.md`. It triages one inbound B2B lead into HOT / WARM / COLD / DISQUALIFY / FLAG, with the score's addition written out. The treatment arm loads this folder and nothing else |
| [`questions.md`](questions.md) | Nine questions with the expected tier, worked out by hand from the rules. Committed before any run (`0cd68c5`; see `git log -- questions.md`) |
| [`control/`](control/) | Raw runs with no folder |
| [`treatment/`](treatment/) | Raw runs with the folder loaded |
| [`results.md`](results.md) | Question by question, ties and losses included, plus what we changed in the folder because of it |
| [`outside-check/`](outside-check/) | Three leads written by a blank session that never saw the folder, keyed before either arm ran on them |
| [`harness/`](harness/) | `run_arms.py` runs one arm; `grade.py` grades a run and re-adds the worked examples |

The answer keys and the runs sit outside `lead-desk/`, so the treatment never sees them.

## Re-run both arms

Needs Python 3.10+ and [Claude Code](https://docs.claude.com/en/docs/claude-code) on your PATH, logged in.

```bash
python harness/run_arms.py control 4
python harness/run_arms.py treatment 4
python harness/grade.py run control/run-4
python harness/grade.py run treatment/run-4
python harness/grade.py examples
```

Use any run number that doesn't exist yet; the runner never overwrites a run.

**Which folder each run saw.** Runs 1 and 2 used the folder as first committed (commit `0cd68c5`). Run 3 used the folder after the changes listed in `results.md` (commit `3ffc2b9`, also the current folder). A treatment re-run at the latest commit should match run 3. To reproduce runs 1 and 2, run the same commands after `git switch --detach 0cd68c5`. Each `run-info.json` from run 2 on records its commit.

**Your own question.** Copy the format of `questions.md` (the shared prompt, then `### X1` blocks with a `text` lead and an `**Expected tier:**` line) into a file, then pass that file as the last argument: `python harness/run_arms.py control 1 mine.md`, then `python harness/grade.py run control/mine-run-1 mine.md`.

## What's the same in both arms, and what isn't

- **Same:** model `claude-opus-5-5`, effort `high`, the exact prompt text in `questions.md`, the question order, one fresh session per question, no tools.
- **Different:** the system prompt. The control gets one line (`harness/base-system-prompt.txt`). The treatment gets that line plus the six folder files. Each run folder keeps the exact text as `system-prompt.txt`.
- **Added by Claude Code to every call in both arms:** a one-line Agent SDK preamble, an environment block (working folder, platform, today's date) and the signed-in account's email. None of it is about leads. `--safe-mode`, `--tools ""` and `--strict-mcp-config` switch off memory files, skills, plugins, hooks, MCP servers and tools. See the limits in `results.md` for the one time this preamble leaked into an output.
- **Without Claude Code:** the control is a fresh claude.ai chat with no project; the treatment is a claude.ai project with the `lead-desk/` files uploaded. Paste each prompt from `questions.md` into its own new chat. claude.ai's own system prompt differs from the CLI's, so expect some drift.

## License

MIT
