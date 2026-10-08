# Outside check

Judges test a question the entrant didn't write. This folder is a dry run of that test, kept apart from the scored set.

| File | What it is |
|------|------------|
| `lead-writer-prompt.txt` | The exact prompt given to a blank Claude session (same harness flags and one-line system prompt as the control arm) |
| `lead-writer.json` | That session's raw output |
| `outside-questions.md` | The three leads byte for byte, with expected tiers worked out from the rules and committed before either arm ran |

Run it like the main set:

```bash
python harness/run_arms.py control 1 outside-check/outside-questions.md
python harness/run_arms.py treatment 1 outside-check/outside-questions.md
python harness/grade.py run control/outside-questions-run-1 outside-check/outside-questions.md
```

**One discarded attempt, disclosed.** The first lead-writer call used the same prompt without the "Realee (realee.ai)" and "made-up domains" wording. It gave the leads' destination a real company's web domain: the domain of the email address Claude Code puts in its preamble for the signed-in account. That domain belongs to an unrelated business, so the output couldn't be published, and we deleted it before any commit. The prompt was changed to name Realee's own domain, and the second call is the one kept here. The same preamble reaches both arms in every run. A scan of every run file for that account's email and domain found nothing.
