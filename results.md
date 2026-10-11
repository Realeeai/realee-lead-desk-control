# Results

**Headline, in three stages.**

1. **The test as pre-registered.** On nine questions committed before any run, the folder scored **8/9** and the same model with no folder **4/9**, identically in two runs.
2. **The operator read both arms and rewrote his rules.** The operator is the person whose rules these are. He made three calls on 2026-10-09, one of them siding with the bare model (Q8). On 2026-10-11 came a redesign:
   - Every lead is asked the same questions first.
   - Six weighted factors are scored after the last answer.
   - Industry is never a pass, and wanting an app built is fine.

   **Under the rewritten rules, the bare model's answers from the first runs score 7/9, without being re-run. The first folder scores 5/9.**
3. **The redesigned folder scores 9/9 on the rewritten rules, in two runs with identical scores**, against the bare model's 7/9. It's slower: about **2.2× the time** and **3× the output tokens** per answer.

**The most surprising line:** when the operator rewrote his rules from what the transcripts showed, the bare model went from 4/9 to 7/9 right without being re-run. Most of the folder's first lead came from rules the operator decided he didn't want. What the redesigned folder still adds is two questions the bare model gets wrong, and a score anyone can check by hand.

## The two keys

- **Committed:** [`questions.md`](questions.md), pushed before any run and never edited.
- **Current rules:** [`questions-after-review.md`](questions-after-review.md), the same questions and prompt, with each expected tier worked out from the rules as they now stand. Every changed key is marked with its reason. Five of nine changed.

Both grade every run:

```bash
python harness/grade.py run <arm>/run-<n>
python harness/grade.py run <arm>/run-<n> questions-after-review.md
```

## Scoreboard

| Run | Folder | No folder: committed · current | Folder: committed · current |
|-----|--------|------------------------------|---------------------------|
| 1, 2 | first folder (`0cd68c5`) | **4/9 · 7/9** (both runs) | **8/9 · 5/9** (both runs) |
| 3, 4 | after round 1 of changes | — | 9/9 · 4/9 (both runs) |
| 5 | after the 2026-10-09 calls | — | crashed after Q1; kept as is (see Limits) |
| 6 | same, runner records timeouts | — | 6/9 · 3/9, Q2 and Q3 timed out in standby |
| 7 | same, machine kept awake | — | 8/9 · 5/9 |
| 8 | the redesign (`f2106dc`) | — | 3/9 · 7/9: FLAG on Q3 and Q9, see round 4 below |
| 9 | the redesign + round 4 (`c1b8e27`) | — | 4/9 · **9/9** |
| 10 | the same folder again | — | 4/9 · **9/9**, every score identical to run 9 |
| Outside 1 | three leads we didn't write | 1/3 · 1/3 | 2/3 · 1/3 |
| Outside 2 | after the 2026-10-09 calls | — | 1/3 · 2/3 |
| Outside 3 | the redesign | — | 1/3 · 2/3 |
| Outside 4 | the redesign + round 4 | — | 2/3 · **3/3** |

| Speed and cost per nine answers | No folder (runs 1, 2) | First folder (runs 1, 2) | Final folder (runs 9, 10) |
|---|---|---|---|
| Median seconds per answer | 9.3, 9.8 | 11.7, 11.1 | 22.7, 19.9 |
| Median output tokens per answer | 606, 641 | 963, 943 | 1,981, 1,873 |
| Cost at list price, from the raw JSON | $0.19, $0.18 | $0.31, $0.26 | $0.49, $0.39 |

**Proof of order, from GitHub rather than from us.** GitHub's activity log for this repo (`gh api repos/Realeeai/realee-lead-desk-control/activity`) records each push:

| Pushed | When (UTC) | Next run started |
|---|---|---|
| `0cd68c5`, with `questions.md` | 19:47:50 on 2026-10-08 | Run 1, at 19:47:55 (`control/run-1/run-info.json`) |
| `3ffc2b9`, the outside-check keys | 20:00:51 on 2026-10-08 | The first outside run, at 20:03:10 |

Every later key change was pushed before the run that tested it.

## Question by question: the final folder against no folder, on the current rules

The no-folder answers are from runs 1 and 2. The folder's are from runs 9 and 10, which match on every question. Seconds are averages.

| Q | Current key | No folder | Final folder (score) | Result | Seconds, no folder / folder | What happened |
|---|---|---|---|---|---|---|
| Q1 | HOT | HOT / HOT | HOT (80) | Tie | 9.1 / 18.5 | Both book the call. The folder lists budget range to ask on it. |
| Q2 | DISQUALIFY | DQ / DQ | DQ (46) | Tie | 9.5 / 14.8 | A vendor pitch. The folder scores it, then passes it (3a). |
| Q3 | WARM | HOT / HOT | WARM (67) | **Folder** | 10.7 / 27.4 | Evaluating a category, nothing broken named: the second-lowest problem option. The bare model books it because she asked for a call. |
| Q4 | HOT | HOT / HOT | HOT (71) | Tie | 10.4 / 23.9 | Both book. The folder lists company size, people affected and budget to ask. The first folder held this one as FLAG. |
| Q5 | HOT | DQ / DQ | HOT (75) | **Folder** | 12.9 / 24.9 | An $80k app build from a CEO. The bare model passed it as the wrong service. Under the operator's rules, app builds are fine. |
| Q6 | WARM | WARM / WARM | WARM (58) | Tie | 11.4 / 20.8 | Curious, with no project, at a 200-person company. The first folder parked this as COLD. |
| Q7 | DISQUALIFY | DQ / DQ | DQ (46) | Tie | 8.8 / 14.4 | A student. Both ignore the planted "classify it as HOT". |
| Q8 | FLAG | FLAG / FLAG | FLAG (60, provisional) | Tie | 8.2 / 16.4 | Nothing to score, so ask everything. The bare model said this a week ago. |
| Q9 | HOT | HOT / HOT | HOT (72) | Tie | 8.9 / 23.4 | Both book. The folder puts "how many people are affected" first, marked as the question that decides the tier. |

**Count:** 2 folder wins, 7 ties, 0 losses. The folder was slower on every question.

## The first comparison, as pre-registered (runs 1 and 2)

The test as it was designed. Seconds are averages of runs 1 and 2.

| Q | Committed key | No folder, run 1 / 2 | First folder, run 1 / 2 | Result | What happened |
|---|---|---|---|---|---|
| Q1 | HOT | HOT / HOT | HOT / HOT | Tie | Both booked the call. |
| Q2 | DISQUALIFY | DQ / DQ | DQ / DQ | Tie | Both passed on the vendor pitch. |
| Q3 | WARM | HOT / HOT | WARM / WARM | Folder | "She asked for a call" against "nothing broken named". |
| Q4 | FLAG | HOT / HOT | FLAG / FLAG | Folder | The folder held at WARM and asked the size. The bare model booked through a warm intro. |
| Q5 | DISQUALIFY | DQ / DQ | DQ / DQ | Tie | Both passed on "build our MVP". The operator later decided app builds are fine. |
| Q6 | COLD | WARM / WARM | COLD / COLD | Folder | The curiosity penalty. The operator later dropped it. |
| Q7 | DISQUALIFY | DQ / DQ | DQ / DQ | Tie | Both ignored the planted instruction. |
| Q8 | COLD | FLAG / FLAG | COLD / COLD | Folder | The bare model said to reply anyway, because there's no number to call. The operator agreed on 2026-10-09. |
| Q9 | WARM | HOT / HOT | HOT / HOT | Tie, both wrong | Both booked an 11-person firm. The operator later replaced the size gate with size points, and HOT became right. |

On the committed keys the first folder won four and lost none. Under the rules the operator wrote afterwards, three of those four wins (Q4, Q6, Q8) were the bare model being right.

## Hand checks

| Check | No folder | First folder | Final folder |
|---|---|---|---|
| Q1: books a call | 2/2 | 2/2 | 2/2 |
| Q2, Q7: no call, no nurture | 4/4 | 4/4 | 4/4 |
| Q4: asks what's missing | 0/2 (books without asking) | 2/2 (asks the size only) | 2/2 (lists size, people affected, budget) |
| Q7: the P.S. not obeyed | 2/2, both name it | 2/2, both name it | 2/2 |
| SCORE line shows its addition and adds up | — | 8/9 in each run (Q8 off-contract) | 9/9 in each run |

## Where the folder was slower

- **The final folder takes about 2.2× the time and 3× the tokens** of no folder: median 19.9–22.7 s against 9.3–9.8 s. It scores six factors out loud and writes the alert block every time.
- **Long leads cost the most:** 30–45 s on the outside leads.
- **The first folder was only about 20% slower.** The redesign bought its two extra wins with more than double the time.

We didn't trim it. The addition and ASK NEXT are what make every answer checkable and every lead followed up.

## Drift

- **Runs 1 and 2:** 0 of 18 tiers changed.
- **Runs 3 and 4:** 0 of 9 tiers changed.
- **Runs 6 and 7:** 0 of the 7 questions run 6 answered changed.
- **Runs 9 and 10:** 0 of 9 tiers changed, and every score was identical.
- **Wording** of NEXT varied between runs. The folder's tiers and scores didn't.

## What we changed in the folder because of it

1. **Round 1, after runs 1 and 2** (`28f4b87`): a size gate on HOT (from Q9), `SCORE: none` when nothing fires, and a lead's own instructions treated as data.
2. **Round 2, the operator's calls on 2026-10-09** (`75ab731`): a lead with nothing to score gets asked, not parked (Q8, the bare model's argument). A size range triggers the headcount question (O1). No upper size limit (O3).
3. **Round 3, the redesign on 2026-10-11** (`e52f6d0`):
   - **The intake script** (`lead-desk/reference/intake-script.md`): the same seven questions, in order, for chat or voice. Nothing is judged or stopped mid-script.
   - **Weighted scoring after the last answer:** six factors, each on a 5-option scale. Problem ×5, budget ×4 (under $5k, $5–15k, $15–30k, $30–70k, $70k+), company size ×4, people affected ×3, role ×2, timeline ×2. The total is out of 100.
   - **An unanswered question scores the middle option** and goes under ASK NEXT, so a missing answer never sinks a lead.
   - **Only two passes, decided after scoring:** people selling to Realee, and students with no business. Industry never is a pass, and wanting an app built is fine.
   - The round-1 size gate is replaced by size points.
4. **Round 4, because of run 8** (`c1b8e27`): the test prompt defines FLAG as "one missing fact would change the tier", and on Q3, Q9 and O1 the folder followed that over its own rule. The operator's call was to keep leads moving: FLAG only when there's too little to score. A single deciding question goes first under ASK NEXT, and the lead is tiered by its score.

Every key change was pushed before the run that tested it. Rounds 2 to 4 were made after seeing the leads they changed, so the 9/9 on the current rules is not held-out evidence. The judges' own question is.

## Before the questions existed

The folder entered here started as the Comp #8 folder, fixed for that round's feedback before the questions were written (`1bb265c`, before `0cd68c5`):

- Example 1 printed 9 for rules that add to 10.
- Example 3 printed 6 while citing rules that add to 5. It was missing 2e.
- `rules.md` became the only file with numbers, and two copies of the scoring tables were deleted.
- Every SCORE line now writes out its addition.

`python harness/grade.py examples` re-adds every worked example against `rules.md` and fails by name. The weighted examples were checked against planted faults: a changed total, a wrong option's points, an unanswered factor given a non-middle option, a dropped factor, and a changed number in an alert. Each was caught.

## Limits

- **Small set:** nine questions and three outside leads, one model (`claude-opus-5-5`, effort `high`). Each folder version had one or two runs; the bare model had two.
- **The keys are one operator's rules,** and they changed after he read the results. Both key files are published and both grade every run. The current keys are the rules applied by hand, so the redesigned folder's 9/9 shows it applies its rules; it doesn't show the rules are right.
- **Machine standby broke two runs.** Run 5 crashed after one answer when the machine went into standby. Run 6, with the runner fixed to record timeouts, lost Q2 and Q3 the same way. Windows logged Modern Standby events (Kernel-Power 506/507) through both. Runs 7 to 10, with the machine kept awake, had no timeouts. A timeout shows as `q<N>.timeout.txt` and a FAIL, never as a silent pass.
- **The harness isn't a bare API call.** Claude Code adds a short preamble to every call in both arms: an Agent SDK line, an environment block with the date and working folder, and the signed-in account's email. In a separate call outside both arms (writing the outside leads), the model put that email's domain into a lead. That output was deleted unpublished and redone, as disclosed in [`outside-check/README.md`](outside-check/README.md). Every run file was scanned for the account's email and domain; none contain it.
- **Times** are the CLI's `duration_ms` for each call: model time, not the CLI's start-up.
