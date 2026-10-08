# Realee Lead Desk

A portable folder operator for Claude Projects. First entered in Clief Notes Comp #8 (The Wildcard); revised for Comp #14 (The Control). The repo root explains the Comp #14 test.

**Paste an inbound lead → get a tier, a score with the addition shown, a next action, and a draft alert — not a summary essay.**

Built for solo founders and small GTM teams selling B2B services who waste afternoons re-qualifying the same inbound shapes: read the message, guess company size, decide whether to book a call, nurture, or pass.

## Philosophy (why a folder, not a chatbot)

This is a **workflow**, not a one-off output. The rubric lives in `rules.md` so when models improve, classification and routing get better without rebuilding integrations. You productionize your ICP judgment once; the runtime changes.

Methodology: [Interpretable Context Methodology](https://arxiv.org/html/2603.16021v2) — folder structure as agent architecture.

## How to use

1. Drop this folder into a Claude Project (**Project knowledge → upload the files**).
2. To fit it to your offer, edit **`rules.md`**. It is the only file with numbers (size band, points, tier cut-offs).
3. Paste any inbound lead (form fields, email, LinkedIn DM, call notes).
4. Expect: **TIER**, **SCORE** (the addition written out), **RULES**, **NEXT ACTION**, **DRAFT ALERT**.

## Try in 60 seconds

Paste these three — each should land on a **different tier**:

1. `VP Ops, 180-employee logistics SaaS, "we're drowning in manual onboarding between Salesforce and NetSuite, budget approved this quarter"` → **HOT** (10/10)
2. `Founder, 12-person agency, "curious about AI, no timeline"` → **DISQUALIFY** (1c: under 20 people, no budget, no scale pain)
3. `Director RevOps, 90 employees, "evaluating workflow automation, call in 2 weeks"` → **WARM** (6/10: 2b-lite, not full 2b — no named broken system)

## Folder map

| File | Job |
|------|-----|
| `identity.md` | Who Lead Desk is and what it refuses |
| `rules.md` | Short-circuit decision tree + scoring. **The only file with numbers** |
| `examples.md` | Worked classifications; every SCORE line adds up |
| `reference/icp.md` | Who Realee sells to, in words |
| `reference/output-format.md` | The output block and the SCORE line format |

## FLAG: ask before booking

If the company size is missing and the rest of the lead already scores 5 or more, Lead Desk holds the lead at WARM and asks for the headcount, one question, before anyone books time (rule 5a). If the size is known and below the band, a high score is held at WARM instead (rule 3e).

## License

MIT — use, fork, adapt the rubric for your ICP.
