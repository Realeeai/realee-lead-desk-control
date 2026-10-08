# examples.md — Realee Lead Desk

---

## Example 1 — HOT (logistics VP, budget, timeline)

**Input:**

```text
Source: website form
Name: Sarah Chen
Role: VP Operations
Company: FleetRoute (logistics SaaS, ~200 employees per LinkedIn)
Message: "We're manually onboarding enterprise customers between Salesforce and NetSuite. It's breaking every quarter. We have budget approved to fix it this quarter. Can we talk?"
```

**Output:**

- **TIER:** HOT
- **SCORE:** 9/10
- **RULES:** 2a, 2b, 2c, 2d, 2e, 3a, 4a, 6a
- **NEXT ACTION:** Book discovery within 48h — send cal link today.
- **ARTIFACT:**

```text
[Lead Alert] HOT: Sarah Chen @ FleetRoute
Score 9/10 — VP Ops, 200 emp, SF↔NetSuite onboarding pain, budget this quarter.
Action: Matt personal reply + book discovery.
Draft: "Sarah — VP Ops pain on enterprise onboarding is exactly what we build for. 15 min this week? [cal link]"
```

---

## Example 2 — DISQUALIFY (dev shop inquiry)

**Input:**

```text
LinkedIn DM: "Hey we're a 5-person dev agency, can you white-label your AI stack for us to resell?"
```

**Output:**

- **TIER:** DISQUALIFY
- **SCORE:** 3 (capped)
- **RULES:** 1a, 3d, 4d
- **NEXT ACTION:** No nurture — polite pass or ignore.
- **ARTIFACT:** Optional pass: "We focus on deployed ops systems for operating companies, not reseller/dev partnerships — best of luck."

---

## Example 3 — WARM (real pain, soft timeline)

**Input:**

```text
Email reply to cold outreach
Name: James Ortiz
Role: Director RevOps
Company: ClearPath HR (~90 employees)
"We're looking at workflow automation vendors. Not urgent — probably evaluate over the next couple months."
```

**Output:**

- **TIER:** WARM
- **SCORE:** 6/10
- **RULES:** 2a, 2b-lite, 2d, 3b, 4b, 6a
- **NEXT ACTION:** Nurture — send case study in 3 days, follow up in 14 days.
- **ARTIFACT:**

```text
[Lead Alert] WARM: James Ortiz @ ClearPath HR
Score 6/10 — RevOps, 90 emp, vendor evaluation mode (2b-lite), 60–90d horizon.
Action: nurture sequence, no Matt calendar yet.
```

---

## Example 4 — FLAG (size unknown, otherwise strong)

**Input:**

```text
Referral from client: "Talk to Maria at Apex Industrial — she runs ops and hates their manual quoting process. Very interested."
```

**Output:**

- **TIER:** FLAG (hold WARM)
- **SCORE:** 5 (provisional)
- **RULES:** 2b, 2d, 5a
- **NEXT ACTION:** Ask referrer: "How many employees at Apex?" before tiering.
- **ARTIFACT:** FLAG question only; do not book until size confirmed.
