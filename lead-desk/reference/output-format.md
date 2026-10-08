# Output format

Every run returns this block (markdown):

```text
---
TIER: [HOT|WARM|COLD|DISQUALIFY|FLAG]
SCORE: [0-10]/10
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
