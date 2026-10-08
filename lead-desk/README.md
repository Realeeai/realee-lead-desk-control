# Realee Lead Desk

**ICM Comp #8 Wildcard submission** — portable folder operator for competition and Claude Projects.

**Paste an inbound lead → get a tier, score, next action, and draft alert — not a summary essay.**

Built for solo founders and small GTM teams selling B2B services who waste afternoons re-qualifying the same inbound shapes.

## Philosophy (why a folder, not a chatbot)

This is a **workflow**, not a one-off output. The rubric lives in `rules.md` and `reference/` so when models improve, classification and routing get better without rebuilding integrations. You productionize your ICP judgment once; the runtime changes.

Methodology: [Interpretable Context Methodology](https://arxiv.org/html/2603.16021v2) — folder structure as agent architecture.

## How to use

1. Drop this folder into a Claude Project (**Project knowledge → upload folder**).
2. Skim `reference/icp.md` once — edit company size band and disqualifiers for your offer.
3. Paste any inbound lead (form fields, email, LinkedIn DM, call notes).
4. Expect: **TIER**, **SCORE**, **RULES CITED**, **NEXT ACTION**, **DRAFT ALERT**.

## Try in 60 seconds

Paste these three — each should land on a **different tier**:

1. `VP Ops, 180-employee logistics SaaS, "we're drowning in manual onboarding between Salesforce and NetSuite, budget approved this quarter"` → **HOT**
2. `Founder, 12-person agency, "curious about AI, no timeline"` → **COLD or DISQUALIFY**
3. `Director RevOps, 90 employees, "evaluating workflow automation, call in 2 weeks"` → **WARM** (2b-lite, not full 2b — no named broken system)

## Folder map

| File | Job |
|------|-----|
| `brief.md` | The client problem this solves |
| `identity.md` | Who Lead Desk is and what it refuses |
| `rules.md` | Short-circuit decision tree + scoring |
| `examples.md` | Worked classifications |
| `reference/` | ICP, rubric, disqualifiers, output shape |

## License

MIT — use, fork, adapt the rubric for your ICP.
