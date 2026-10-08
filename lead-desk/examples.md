# examples.md — Realee Lead Desk

Every SCORE line below adds up. `harness/grade.py examples` (at the repo root) re-adds each one against the points in `rules.md` and fails by name if a total or a point value drifts.

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
- **SCORE:** 2a(+2) + 2b(+3) + 2c(+2) + 2d(+2) + 2e(+1) = 10/10
- **RULES:** 2a, 2b, 2c, 2d, 2e, 3a, 4a, 6a
- **NEXT ACTION:** Book discovery within 48h — send cal link today.
- **ARTIFACT:**

```text
[Lead Alert] HOT: Sarah Chen @ FleetRoute
Score 10/10 — VP Ops, 200 emp, SF↔NetSuite onboarding pain, budget this quarter.
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
- **SCORE:** not scored (1a)
- **RULES:** 1a, 3d, 4d, 6a
- **NEXT ACTION:** No nurture — polite pass or ignore.
- **ARTIFACT:**

```text
[Lead Alert] DISQUALIFY: unnamed @ 5-person dev agency
White-label / reseller ask (1a). Not a buyer of ops systems.
Action: polite pass, do not nurture.
Pass: "We focus on deployed ops systems for operating companies, not reseller/dev partnerships — best of luck."
```

---

## Example 3 — WARM (vendor evaluation, no named system)

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
- **SCORE:** 2a(+2) + 2b-lite(+1) + 2d(+2) + 2e(+1) = 6/10
- **RULES:** 2a, 2b-lite, 2d, 2e, 3b, 4b, 6a
- **NEXT ACTION:** Nurture — send case study in 3 days, follow up in 14 days.
- **ARTIFACT:**

```text
[Lead Alert] WARM: James Ortiz @ ClearPath HR
Score 6/10 — RevOps, 90 emp, vendor evaluation mode (2b-lite, not 2c), 60–90d horizon (2e).
Action: nurture sequence, no Matt calendar yet.
Suggested line: "James — happy to be on your list. Here's how a 90-person team cut its handoffs; worth a look before you shortlist."
```

---

## Example 4 — FLAG (size unknown, otherwise strong)

**Input:**

```text
Referral from client: "Talk to Maria at Apex Industrial — she runs ops and hates their manual quoting process. Very interested."
```

**Output:**

- **TIER:** FLAG (hold WARM)
- **SCORE:** 2b(+3) + 2d(+2) = 5/10 (provisional, 2a unknown)
- **RULES:** 2b, 2d, 5a, 6a
- **NEXT ACTION:** Ask the referrer: "How many employees at Apex Industrial?" before tiering.
- **ARTIFACT:**

```text
[Lead Alert] FLAG: Maria @ Apex Industrial
Provisional 5/10 — runs ops, named pain (manual quoting). Company size unknown, so 2a can't be scored.
Hold question: "How many employees at Apex Industrial?"
Action: hold at WARM; do not book until size is confirmed.
```
