# rules.md — Realee Lead Desk

Logic is **ordered**. First section that produces an outcome **wins**. Every output cites **rule IDs**.

## 0. Output shape (always)

1. **TIER** — HOT | WARM | COLD | DISQUALIFY | FLAG
2. **SCORE** — integer 0–10 (see Section 2)
3. **RULES** — list of rule IDs that fired
4. **NEXT ACTION** — one imperative line for Matt
5. **ARTIFACT** — draft alert or pass (see `reference/output-format.md`)

---

## 1. Hard disqualifiers (1a–1e)

If any match → **DISQUALIFY**, score capped at 3, skip scoring bonuses.

| ID | Trigger |
|----|---------|
| **1a** | Solo developer / "hire me to code your app" / agency wants white-label dev shop with no ops pain |
| **1b** | Consumer, creator, or e-commerce DTC (no B2B ops angle) |
| **1c** | Company clearly &lt; 20 employees with no budget language and no operational scale pain |
| **1d** | Student, homework, or "learning AI" with no business context |
| **1e** | Competitor, vendor pitch, or recruiter (selling to Realee, not buying) |

---

## 2. Scoring rubric (2a–2f)

Start at 0. Add points; cite each addition. Max 10.

| ID | Signal | Points |
|----|--------|--------|
| **2a** | Company size credibly 50–500 employees (or 30–49 with strong pain + budget) | +2 |
| **2b** | Clear operational pain — **named** broken process, handoff, or manual workflow | +3 |
| **2b-lite** | Category evaluation only ("evaluating automation", "looking at vendors") with **no named system** | +1 |
| **2c** | Budget or investment language ("approved", "spend", "vendor", "this quarter") | +2 |
| **2d** | Decision maker or strong influencer (Founder, C-suite, VP Ops/RevOps/Sales) | +2 |
| **2e** | Timeline ≤ 90 days or active evaluation | +1 |
| **2f** | Penalty: vague "curious about AI" with no process pain | −2 (min score 0) |

---

## 3. Tier mapping (3a–3d)

After disqualifiers and score:

| ID | Score | Tier |
|----|-------|------|
| **3a** | 8–10 | **HOT** |
| **3b** | 5–7 | **WARM** |
| **3c** | 0–4 | **COLD** |
| **3d** | DISQUALIFY from §1 | **DISQUALIFY** (ignore score) |

---

## 4. Next action (4a–4d)

| Tier | ID | Next action |
|------|-----|-------------|
| HOT | **4a** | Book discovery within 48h — draft alert includes cal link placeholder |
| WARM | **4b** | Add to nurture — send value asset in 3 days, no hard pitch |
| COLD | **4c** | Park — no personal time; optional monthly check-in |
| DISQUALIFY | **4d** | Send polite pass or no reply — do not nurture |

---

## 5. FLAG gate (5a)

If **2a** cannot be assessed (no company size hint) AND score would be ≥5 → **FLAG**: ask one question ("How many employees at {company}?") and hold **WARM** until answered.

---

## 6. Draft artifact (6a)

Always produce the internal alert block from `reference/output-format.md` for **every tier** (HOT, WARM, COLD, FLAG, DISQUALIFY).

| Tier | Draft content |
|------|----------------|
| HOT / WARM | Full alert + suggested reply line to lead |
| FLAG | Alert + the one hold question from §5a (employee count) |
| COLD | Internal alert; no suggested reply line |
| DISQUALIFY | Internal alert + polite pass wording (do not nurture) |
