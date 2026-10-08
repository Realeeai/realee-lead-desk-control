# Client brief — Realee inbound lead triage

**Client:** Matt Hernandez, founder — Realee AI (B2B AI systems for ops/sales automation) and The Forge (delivery shop).

**Problem:** Every week I get inbound from the website, LinkedIn, referrals, and cold-reply threads. Each one takes 10–20 minutes of context switching: read the message, guess company size, wonder if they're a developer shopping for tools or an ops leader with budget, then decide whether I should book a call, add them to nurture, or politely pass. I built Trigger.dev automation for this, but half the leads arrive as messy paste-ins during a live day — and the automation doesn't help me *decide* in the moment. I still end up asking generic chatbots "is this a good lead?" and getting essays instead of a call I can trust.

**What I've tried:** A scoring rubric in our growth-ops directive, Instantly + Sheets, and ad-hoc Claude chats. They either need API wiring or return "here are some factors to consider."

**What I need:** A folder-based operator that reads one inbound blob (form dump, email, DM, call notes) and returns **one tier** (HOT / WARM / COLD / DISQUALIFY), a **numeric score with cited rules**, a **one-line next action**, and a **draft alert email** I can forward to hello@realee.ai — without asking me what to do.

**Success:** Three test leads I haven't shown it before produce three different tiers, and I would act on the HOT output within five minutes without re-reading the rubric.
