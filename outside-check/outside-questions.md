# Outside check — three leads we didn't write

Not part of the scored set in `questions.md`. A blank Claude session that had never seen the folder or the questions wrote these three leads (`lead-writer-prompt.txt`, raw output `lead-writer.json`). They are pasted below byte for byte. We worked out the expected tiers from `lead-desk/rules.md` at commit 28f4b87 and committed them before either arm ran on them. The judges' own question is the real version of this test.

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
- **By the rules:** 2b(+3) carrier invoices read, matched to loads and keyed into QuickBooks by hand + 2d(+2) owner + 2e(+1) running before January = 6 → WARM (3b). 2a doesn't fire: "11-50" isn't credibly 50–500, and the 30–49 clause needs budget language, which isn't there (asking the price isn't 2c). No FLAG: 5a is for no size hint, and here there is one.
- **Arguable:** a stranger could argue FLAG, because a 50-person firm would add 2a and reach HOT. The rules say a size bracket is a size hint, so no FLAG.

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
- **By the rules:** 2a(+2) about 380 + 2b(+3) AEs' post-call CRM fields (next steps, MEDDICC) filled in inconsistently, hurting forecast accuracy + 2d(+2) VP + 2e(+1) fix wanted before December planning = 8, and 2a fired → HOT (3a). No 2c: no budget words, and asking about fees isn't budget language.

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

- **Expected tier:** COLD
- **By the rules:** 2b-lite(+1) evaluating options for procure-to-pay and supplier onboarding, no broken process described + 2d(+2) Director + 2e(+1) build-vs-buy test before year end = 4 → COLD (3c). 2a doesn't fire: about 2,300 employees is above the 50–500 band. No 2c: he says outright there's no approved budget.
- **Arguable:** a stranger could read the named processes as full 2b (+3), which makes 6 → WARM. We read them as category evaluation, because no broken step is described.
