# Outside check — key after the operator's review

Same leads and prompt as [`outside-questions.md`](outside-questions.md), which stays exactly as committed before any run on it. The keys below follow the rules as they now stand, after the operator's two rounds of changes (2026-10-09 and the 2026-10-11 redesign, both described in [`questions-after-review.md`](../questions-after-review.md)). Each changed key is marked. Grade with `python harness/grade.py run <run folder> outside-check/outside-questions-after-review.md`.

After the 2026-10-09 calls these leads are no longer held out: those calls were made after seeing them.

## The prompt both arms get

The same text as in `questions.md`:

```text
I run Realee, a small firm that builds AI workflow automation for B2B operating companies. Triage this inbound lead for me.

Pick one tier:
- HOT: book a call now
- WARM: nurture, no call yet
- COLD: park, low priority
- DISQUALIFY: pass, don't nurture
- FLAG: one missing fact would change the tier, so ask that one question first

End your reply with this line, filled in:
ANSWER: TIER=<HOT|WARM|COLD|DISQUALIFY|FLAG> | NEXT=<one short next action>

Lead:
{lead}
```

## Leads

### O1 — Freight brokerage owner, invoice matching, size given as a bracket

```text
Source: Website contact form (realee.ai/contact), submitted Mon Oct 5, 2026, 9:47 PM

Name: Dana Kowalczyk
Company: Kowalczyk & Reyes Freight Brokerage
Email: dana@kr-freightbrokers.com
Phone: (614) 555-0182
Company size: 11-50
Role: Owner / Operations

What are you hoping to automate?
We get 150-200 carrier invoices a week. They come in as PDF attachments, sometimes photos of paper from drivers. Two people on my team open each one, match it to the load in our TMS (we use Ascend), check the rate against the rate con, then key it into QuickBooks Online. It's eating about 30 hrs a week combined, and mistakes are costing us. Last month we double paid a carrier $4,200 and haven't gotten it back.

I want something that reads the invoice, matches it to the load, flags anything that doesn't match the rate con, and pushes the clean ones to QBO for approval. Is that something you do? What does it cost roughly? I don't want to spend 6 months on this. We're slow in Jan so I'd like it running before then.

How did you hear about us? Saw your post in the TMS users Facebook group
```

- **Expected tier:** WARM
- **Under the current rules:** P5(+25) carrier invoices matched and keyed by hand, 30 hours a week and a $4,200 double payment + B?3(+12) asked the price, no budget given + S2(+8) "11-50" counts as the lower option + A1(+3) two people + R5(+10) owner + T4(+8) before January = 66 → WARM (5b). The exact headcount goes under ASK NEXT.
- **Note:** On 2026-10-09 this key was FLAG (a size range straddling the floor triggered the headcount question). Under the redesign the headcount is still asked, under ASK NEXT, and the lead is scored.

### O2 — VP RevOps, 380 people, CRM hygiene hurting the forecast

```text
Source: LinkedIn InMail to Realee company page, received Tue Oct 6, 2026

From: Priya Natarajan
Headline: VP, Revenue Operations at Lumenfold | ex-Corvane | RevOps, GTM Systems

Hi there, a friend at another portfolio company mentioned you set up some agent workflows for their SDR team and it went well.

Context: we're ~380 people, Series C, Salesforce + Outreach + Gong + a mess of spreadsheets. Our AEs spend way too much time on pre-call research and post-call CRM hygiene. Next steps, MEDDICC fields, all of it is inconsistently filled out and it's killing our forecast accuracy. Leadership wants a fix before our FY27 planning in December.

We looked at a couple of the off-the-shelf "AI SDR" tools and they felt like toys, or they wanted to own our whole stack. I'm more interested in something that plugs into what we already have.

Couple of questions before I loop in my team:
- Do you work with Salesforce custom objects, or only standard?
- How do you handle security review? Our infosec team will want SOC 2 and a DPA before anything touches Gong transcripts.
- Is this a project fee or ongoing?

Open to a 30 min call next week if it's a fit. Thursday or Friday afternoons work best.

Priya
```

- **Expected tier:** HOT
- **Under the current rules:** P4(+20) or P5(+25) AEs' CRM fields inconsistently filled, hurting forecast accuracy + B?3(+12) + S4(+16) about 380 + A?3(+9) + R5(+10) VP + T4(+8) before December planning = 75 or 80 → HOT (5a) either way.

### O3 — Enterprise build-vs-buy check, no budget yet

```text
Source: Email to hello@realee.ai, received Wed Oct 7, 2026, 7:12 AM
From: Gregory Ashby-Vance <g.ashbyvance@meridale-industrial.com>
Subject: Intro / process automation - exploratory

Hello,

I lead the Digital Enablement function within Shared Services at Meridale Industrial Group (approx. 2,300 employees across 4 sites, NA and Mexico). I came across Realee through a webinar recording on agentic document workflows and wanted to reach out.

We're in early stages of evaluating options for automating parts of our procure-to-pay and supplier onboarding processes. To be transparent, we have an internal team that has built some proofs of concept on Azure, and we're also in conversations with one of the larger SIs as part of a broader transformation program. Our CFO has asked us to "pressure test" the build-vs-buy question before year-end, so I'm speaking with a small number of specialist firms to understand the landscape.

If possible, it would be helpful to receive the following ahead of any conversation:
- Reference architecture / technical overview of how your solutions are deployed
- Typical pricing structure and indicative ranges for an engagement of this type
- 2-3 case studies, ideally manufacturing or shared services
- Your approach to model selection and data residency (our Mexico entity has some constraints)

I'd also be happy to have an informal call to compare notes. I should mention we don't yet have an approved budget line for this. That would be determined in the Q1 planning cycle depending on the outcome of the evaluation.

Kind regards,

Gregory Ashby-Vance
Director, Digital Enablement, Global Business Services
Meridale Industrial Group
```

- **Expected tier:** WARM
- **Under the current rules:** P2(+10) evaluating options, no broken step described + B?3(+12) no approved budget yet + S5(+20) about 2,300 + A?3(+9) + R4(+8) director + T4(+8) build-vs-buy decision before year end = 67 → WARM (5b).
- **Changed after review** (committed key: COLD): no upper size limit (2026-10-09), so 2,300 people now score the top size option.
