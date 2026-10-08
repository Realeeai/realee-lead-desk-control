# Output format

Every run returns this block (markdown):

```text
---
TIER: [HOT|WARM|COLD|DISQUALIFY|FLAG]
SCORE: [the addition] = [total]/10
RULES: [comma-separated rule IDs]
NEXT ACTION: [one line]
---

LEAD: {Name} | {Company} | {Role}
SOURCE: {if known}
PAIN: {1-2 sentences}

RATIONALE: {why these rules fired}

--- DRAFT ALERT ---
Subject: [Lead Alert] {TIER}: {Name} from {Company}

{2-4 sentences for Matt or hello@realee.ai}

Suggested line to lead (HOT/WARM only):
"{paste-ready reply}"

FLAG tier: include the hold question from rules.md §5a in the draft body (no suggested reply until answered).

DISQUALIFY tier: include polite pass wording in the draft body.
```

## The SCORE line (show the addition)

Write each rule that changed the score, its points in brackets, joined by `+`, then `=` and the total. Point values come from `rules.md` §2 only.

| Case | SCORE line |
|------|------------|
| Normal | `SCORE: 2a(+2) + 2b(+3) + 2c(+2) = 7/10` |
| Penalty | `SCORE: 2a(+2) + 2d(+2) + 2f(-2) = 2/10` |
| Below zero | `SCORE: 2f(-2) = 0/10 (floor)` |
| FLAG | `SCORE: 2b(+3) + 2d(+2) = 5/10 (provisional, 2a unknown)` |
| DISQUALIFY | `SCORE: not scored (1a)` |

The total must equal the sum of the terms written. If it doesn't, the run is wrong, whatever the tier.

## Sheet row (optional paste to CRM/Sheets)

| Field | Value |
|-------|-------|
| Name | |
| Email | |
| Company | |
| Role | |
| Source | |
| Score | |
| Tier | |
| Pain | |
| Rationale | |
