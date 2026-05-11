# Disclosure Decision Framework

When to disclose AI tooling involvement, when not to disclose unprompted, and the trade-offs. The strategic frame the rest of the disclosure templates assume.

## The two failure modes

There are two ways to get disclosure wrong:

1. **Under-disclosure** — you don't tell customers about AI usage; they find out later (from an incident, a leaked memo, a competitor); trust collapses.
2. **Over-disclosure** — you proactively volunteer information customers didn't ask for; create concerns they didn't have; spend marketing energy explaining things instead of building.

Both happen. The frame that helps: **disclosure is durable when it matches what customers expect at the time of expectation.**

## The default lean

Per the README's editorial stance: **lean toward disclosure when in doubt.** Reasoning:

- Disclosure is hard to undo. Commitment to non-disclosure can become trapping when public discourse shifts.
- Customers respect honesty more than perfection.
- Competitors will disclose. Customers calibrate against the disclosing competitor.
- Audit trails will surface AI usage eventually. Better the disclosure language match reality.

This default lean does NOT mean "disclose everything proactively." It means "when the question is whether to share information that customers might want, default to sharing rather than withholding." The proactivity question is separate.

## The four disclosure layers

| Layer | What it discloses | When it should be in place |
|---|---|---|
| **1. Public ToS / DPA** | High-level acknowledgment of AI usage in development and product features | All companies using AI tooling at scale (most mid-size companies in 2026) |
| **2. Security questionnaire response** | Mid-detail on tooling, data handling, governance | When customers ask via questionnaire — most enterprise B2B by mid-2026 |
| **3. Live conversation under NDA** | Specific tooling, specific data flows, specific failure modes | When customers ask in meetings — varies; common with security-sensitive customers |
| **4. Public post-incident review** | Specific failure modes, including AI involvement when material | When an incident occurs that warrants a PIR |

The layered approach matters. Putting Layer 4 information into Layer 1 (public ToS) creates fragility — every detail becomes a contractual commitment. Putting Layer 1 information into Layer 4 only (no public acknowledgment, only post-incident) creates surprise — customers feel ambushed.

## When to disclose proactively

### ✅ Disclose proactively when:

1. **Required by contract or regulation.** Some industries require notification of automated tooling involvement. Just do it.
2. **The disclosure is material to a procurement decision the customer is making.** "We use AI tooling extensively" is material context for an enterprise buyer who's evaluating you.
3. **The disclosure is part of established annual or quarterly customer communication.** SOC 2 Type II audits, annual security reports, quarterly business reviews. Build it in; don't make it a special event.
4. **A specific incident's PIR includes AI authorship as material.** Per [`status-page-language.md`](status-page-language.md), some PIRs include this; some don't.
5. **A competitor's disclosure has shifted public expectation in your category.** When everyone in your industry is disclosing, non-disclosure becomes a red flag.

### ❌ Do NOT disclose proactively when:

1. **The customer hasn't asked and the disclosure isn't material.** Don't volunteer detail that creates concern. "By the way, we use AI tools" inserted into a sales call is awkward and signals you're worried about something.
2. **You haven't completed your own internal governance work yet.** Promising disclosure you can't back up is worse than waiting.
3. **The disclosure would identify a specific employee, customer, or third party.** Privacy considerations override disclosure preferences.
4. **You're in active litigation or under regulatory inquiry where disclosure could be misused.** Legal counsel decides.
5. **The disclosure is purely marketing rather than informational.** "We use AI to deliver superior products" is a marketing claim; not a disclosure.

## The "asked vs. proactive" distinction

The decision framework cleaves on whether the customer asked. Two paths:

### Customer asked

The default is disclosure proportional to the question. The four-layer framework above tells you which layer is appropriate based on the form of the question:

- Public-facing question (forum post, public comparison) → Layer 1 (ToS-level)
- Security questionnaire → Layer 2
- Live conversation → Layer 3 if NDA exists; Layer 2 otherwise
- Post-incident inquiry → Layer 4 reference

If you don't know how to answer at the right layer, default to "let me make sure we get you the right level of detail" and follow up rather than improvising.

### Customer didn't ask

The default is to consider whether the disclosure is in your customer's interest, not yours. Two questions:

1. **Would the customer want to know this if they thought to ask?** Often yes. Disclose at the layer their existing relationship suggests.
2. **Would the customer benefit from knowing this proactively?** Sometimes yes (enterprise security reviews benefit from advance notice; customers running their own AI governance benefit from knowing you've done yours). Sometimes no (a small SMB customer doesn't benefit from a long technical disclosure).

When the answer is "yes" to both, disclose proactively. When "yes" to one and "no" to the other, default to disclosure when asked. When "no" to both, don't volunteer.

## What goes in each layer

Specific calibration:

### Layer 1 — Public ToS / DPA

- Acknowledgment that AI tooling is used in development
- Acknowledgment of AI features in product (when present)
- Listed AI subprocessors in the DPA
- Reference to internal governance (specifics not in the public document)
- Standard breach / incident notification commitments (covering all incidents, AI-authored or not)

### Layer 2 — Security questionnaire response

- Specific approved tooling matrix (current state)
- Data classification rules and how they apply to AI tooling
- Vendor security review status for each AI tool
- Internal review processes for AI-authored code
- Aggregate metrics where defensible (e.g., percentage of code involving AI assistance)
- Reference to specific contractual commitments with AI vendors

### Layer 3 — Live conversation under NDA

- Specific failure modes you've encountered and how you addressed them
- Trade-offs you've made (including ones you'd reconsider)
- Internal incident metrics
- Specific commitments you'd consider for this customer

### Layer 4 — Public PIR

- AI authorship of affected code, when material per the criteria in [`status-page-language.md`](status-page-language.md)
- Specific failure mode in customer-affecting terms
- Specific gap in review/CI/harness that allowed the failure
- Specific changes being made

## Common scenarios and the framework's answer

### "Customer asks about AI in a sales call before the contract is signed"

**Answer:** Layer 2 detail. They're doing procurement; they need security questionnaire-level information. Send them the questionnaire response if they haven't received it.

### "Customer asks about specific tools you use in a renewal conversation"

**Answer:** Layer 3 detail under NDA. The renewal conversation is post-procurement; the customer is asking deeper questions. Provide the detail.

### "Customer asks during a live incident if AI was involved"

**Answer:** Layer 4 framing. The honest answer is "we don't know yet; we're investigating; the post-incident review will address authorship if it's material." Don't speculate during the incident.

### "Industry analyst asks for comment on your AI practices"

**Answer:** Layer 1 / 2 only. Industry analysts are not your customers; their questions feed into public reports. Stick to ToS-level language.

### "Press asks for comment on your AI practices"

**Answer:** Reference Layer 1 (ToS), redirect specifics to PR/comms. Don't improvise. Press conversations have different rules from customer conversations.

### "Regulator asks for documentation of your AI tooling practices"

**Answer:** Whatever the regulator requires. Layer 2-3 detail typically; sometimes Layer 4 detail. Legal counsel drives.

### "Internal employee or contractor asks about AI tooling for a private project"

**Answer:** Out of scope of this framework. That's an internal-comms conversation, not a customer-disclosure one.

## What this framework will NOT do

- Will not protect you in a regulatory environment that requires more disclosure than you've prepared for. Stay current on regulatory requirements.
- Will not work if your governance discipline doesn't match your disclosure language. The framework is downstream of having a real practice.
- Will not eliminate edge cases. Some customer questions don't fit the framework cleanly; use judgment.
- Will not handle hostile-customer scenarios. Different domain; see [`customer-conversation-scripts.md`](customer-conversation-scripts.md) §8.

## When to revisit the framework

Annually, at minimum. Triggers for off-cycle revisit:

- A new AI capability or tool category emerges (the disclosure layer for it might be different)
- Industry disclosure norms shift
- A regulatory change creates new disclosure requirements
- Your own incident or near-miss surfaces a gap in the disclosure framework

The framework should evolve. Pin it to a specific version (e.g., "Disclosure Framework v2026.q3") and update with explicit version bumps so that contract language and customer commitments can reference a specific version.

## Companion artifacts

- [`security-questionnaire-answers.md`](security-questionnaire-answers.md) — Layer 2 detail
- [`status-page-language.md`](status-page-language.md) — Layer 4 detail
- [`ai-authorship-disclosure-tos.md`](ai-authorship-disclosure-tos.md) — Layer 1 detail
- [`customer-conversation-scripts.md`](customer-conversation-scripts.md) — Layer 3 conversations
- `exec-kit/` — internal artifacts the disclosure references
- Ch 31 §31.6, Ch 41 — sources

## Reminder

This framework is a tool for thinking about disclosure decisions; it is not a substitute for legal counsel, your security/compliance leadership, or your CEO's judgment in specific cases. The patterns are durable; the specific decisions are contextual.
