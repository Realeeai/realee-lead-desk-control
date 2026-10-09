# rules.md — Realee Lead Desk

Logic is **ordered**. First section that produces an outcome **wins**. Every output cites **rule IDs**.

**This is the only file with numbers.** Points, the size band and the tier cut-offs live here and nowhere else. To fit the desk to your own offer, edit this file.

## 0. Output shape (always)

1. **TIER** — HOT | WARM | COLD | DISQUALIFY | FLAG
2. **SCORE** — the addition written out, then the total (see Section 2 and `reference/output-format.md`)
3. **RULES** — list of rule IDs that fired
4. **NEXT ACTION** — one imperative line for Matt
5. **ARTIFACT** — draft alert or pass (see `reference/output-format.md`)

---

## 1. Hard disqualifiers (1a–1e)

If any match → **DISQUALIFY**. Do not score; the SCORE line reads `not scored (<rule ID>)`.

| ID | Trigger |
|----|---------|
| **1a** | Solo developer / "hire me to code your app" / "build our MVP" / agency wants a white-label dev shop, with no ops pain |
| **1b** | Consumer, creator, or e-commerce DTC (no B2B ops angle) |
| **1c** | Company clearly &lt; 20 employees with no budget language and no operational scale pain |
| **1d** | Student, homework, or "learning AI" with no business context |
| **1e** | Competitor, vendor pitch, or recruiter (selling to Realee, not buying) |

---

## 2. Scoring rubric (2a–2f)

Start at 0. Add points; cite each addition. Max 10. If the total falls below 0, it is 0.

| ID | Signal | Points |
|----|--------|--------|
| **2a** | Company size credibly 50 employees or more, with no upper limit: larger is better (or 30–49 with strong pain + budget) | +2 |
| **2b** | Clear operational pain — **named** broken process, handoff, or manual workflow | +3 |
| **2b-lite** | Category evaluation only ("evaluating automation", "looking at vendors") with **no named system** | +1 |
| **2c** | Budget or investment language ("approved", "budgeted", "spend", "this quarter"). Talking to or about vendors is not budget language; that is 2b-lite | +2 |
| **2d** | Decision maker or strong influencer (Founder, C-suite, VP, or Head/Director of Ops, RevOps or Sales) | +2 |
| **2e** | Timeline ≤ 90 days or active evaluation | +1 |
| **2f** | Penalty: vague "curious about AI" with no process pain | −2 |

2b and 2b-lite never both fire.

**Show the addition.** The SCORE line lists every rule that added or removed points, with its points, then the total:
`SCORE: 2a(+2) + 2b(+3) + 2d(+2) = 7/10`. If no rule fires, write `SCORE: none = 0/10`. The total must equal the sum of the terms written. A tier is never chosen without this line, unless §1 short-circuits.

---

## 3. Tier mapping (3a–3e)

After disqualifiers and score:

| ID | Score | Tier |
|----|-------|------|
| **3a** | 8–10, **and 2a fired** | **HOT** |
| **3b** | 5–7 | **WARM** |
| **3c** | 0–4 | **COLD** |
| **3d** | DISQUALIFY from §1 | **DISQUALIFY** (not scored) |
| **3e** | 8–10 **without 2a**, size known and below the 2a floor | **WARM** (held) |

**3e — HOT needs the size band.** A small firm can add up to 8 on problem, budget, authority and timing alone. That's a real lead, but it's smaller than Realee sells to, so it gets nurture, not the founder's calendar. Cite 3e and say in the alert that it's held for size. If the size is unknown rather than small, that's FLAG (5a), not 3e.

---

## 4. Next action (4a–4d)

| Tier | ID | Next action |
|------|-----|-------------|
| HOT | **4a** | Book discovery within 48h — draft alert includes cal link placeholder |
| WARM | **4b** | Add to nurture — send value asset in 3 days, no hard pitch |
| COLD | **4c** | Park — no personal time; optional monthly check-in |
| DISQUALIFY | **4d** | Send polite pass or no reply — do not nurture |

---

## 5. FLAG gates (5a–5b)

**5a — size unknown.** If **2a** cannot be assessed AND score would be ≥5 → **FLAG**: ask one question ("How many employees at {company}?") and hold **WARM** until answered. 2a can't be assessed when there's no size hint, or when the size is a range where some values would earn 2a and some wouldn't (e.g. "11-50"). The SCORE line marks the total as provisional.

**5b — nothing to score.** If the lead names no company, no role and no problem → **FLAG**: send one line asking which company they're with and what they want fixed, and hold **COLD** until they answer. One line isn't personal time, and parking a lead you can't judge decides nothing. SCORE: `none = 0/10 (provisional, nothing to score)`.

---

## 6. Draft artifact (6a)

Always produce the internal alert block from `reference/output-format.md` for **every tier** (HOT, WARM, COLD, FLAG, DISQUALIFY).

| Tier | Draft content |
|------|----------------|
| HOT / WARM | Full alert + suggested reply line to lead |
| FLAG | Alert + the one hold question (5a: employee count; 5b: company and problem) |
| COLD | Internal alert; no suggested reply line |
| DISQUALIFY | Internal alert + polite pass wording (do not nurture) |
