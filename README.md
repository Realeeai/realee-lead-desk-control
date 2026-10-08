# Realee Lead Desk — the control test

Clief Notes Weekly Comp #14, "The Control". Does a small specialist folder beat the same model with no folder? This repo holds the test: the folder, nine questions committed before any run, both arms' raw runs, and an honest results file.

**Headline:** see [`results.md`](results.md).

## What's here

| Path | What it is |
|------|------------|
| [`lead-desk/`](lead-desk/) | The specialist folder: `identity.md`, `rules.md`, `examples.md`, `reference/`, `README.md`. It triages one inbound B2B lead into HOT / WARM / COLD / DISQUALIFY / FLAG with the score's addition written out. The treatment arm loads this folder and nothing else |
| [`questions.md`](questions.md) | Nine questions with the expected tier, worked out by hand from the rules. Committed before any run: `git log -- questions.md` |
| [`control/`](control/) | Raw runs with no folder |
| [`treatment/`](treatment/) | Raw runs with the folder loaded |
| [`results.md`](results.md) | Question by question, ties and losses included, plus what we changed in the folder because of it |
| [`harness/`](harness/) | `run_arms.py` runs one arm; `grade.py` grades a run and re-adds the worked examples |

The answer key (`questions.md`) and the runs sit outside `lead-desk/`, so the treatment never sees them.

## Re-run both arms

Needs Python 3.10+ and [Claude Code](https://docs.claude.com/en/docs/claude-code) on your PATH, logged in.

```bash
python harness/run_arms.py control 3
python harness/run_arms.py treatment 3
python harness/grade.py run control/run-3
python harness/grade.py run treatment/run-3
python harness/grade.py examples
```

Use any run number that doesn't exist yet; the runner never overwrites a run.

## What's the same in both arms, and what isn't

- **Same:** model `claude-opus-5-5`, effort `high`, the exact prompt text in `questions.md`, the question order, one fresh session per question, no tools.
- **Different:** the system prompt. The control gets one line (`harness/base-system-prompt.txt`). The treatment gets that line plus the six folder files. Each run folder keeps the exact text as `system-prompt.txt`.
- **Added by Claude Code to every call in both arms:** a one-line Agent SDK preamble, an environment block (working folder, platform, today's date) and the signed-in account's email. None of it is about leads. `--safe-mode`, `--tools ""` and `--strict-mcp-config` switch off memory files, skills, plugins, hooks, MCP servers and tools.
- **Without Claude Code:** the control is a fresh claude.ai chat with no project; the treatment is a claude.ai project with the `lead-desk/` files uploaded. Paste each prompt from `questions.md` into its own new chat. claude.ai's own system prompt differs from the CLI's, so expect some drift.

## License

MIT
