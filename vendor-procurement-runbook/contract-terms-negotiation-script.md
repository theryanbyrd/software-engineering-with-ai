# Contract Terms Negotiation Script

Verbatim language for the contract negotiations that matter for AI tools. Per Ch 38:

> Get the incident notification SLA in the contract. Get a named security contact, not a generic support address. Verify training opt-out is enforced in your tenant, not just in policy.

The asks here are calibrated to what's typically negotiable at the Enterprise / Business tier. They are NOT calibrated to what a single-seat purchase can negotiate; for those, the standard ToS is what you get.

## Pre-negotiation setup

Before the conversation:

1. **Have the security review done.** [`security-review-template.md`](security-review-template.md). The findings drive the negotiation.
2. **Know your walk-away.** Which tier do you fall back to if this vendor won't agree to your terms? (Often the answer is "the next vendor down" — that's fine; know it.)
3. **Get legal counsel involved early.** The asks below are operational; the contract language is legal. Don't try to write the actual clauses yourself.
4. **Know what's worth ¥ vs. what isn't.** Some asks are non-negotiable for you (training opt-out, BAA if you need it). Others are nice-to-have (specific incident SLA hours). Walk in knowing.

## The five asks that matter most

For each: what to ask for, why, the verbatim opening, the typical pushback, and how to respond.

### Ask 1 — Training opt-out, contractually enforced, with audit

**What to ask for:** Explicit contract language that vendor will not train any model on your data. Stronger than vendor policy; stronger than tenant settings; in the master agreement, with audit rights.

**Why:** Vendor policies change. Tenant settings can be misconfigured. Contract language survives policy changes. Audit rights let you verify.

**Opener:**

> "Our engineering work is the company's competitive asset; we cannot have it used to train models that we don't control. We need explicit contract language committing to no training on our data, with the right to audit annually. We've seen this language in [comparable vendor]'s contract; here's what we'd want."

**Typical pushback:**

- "Our policy is no training; we don't need to put it in the contract." → "Policies change; contracts don't, without our agreement. We need it in writing."
- "We can't agree to audit rights." → "Audit can be inspection of the relevant SOC 2 controls, plus annual confirmation in writing. We don't need physical access to your infrastructure."
- "This is enterprise-tier only." → "Then we're at enterprise tier on this. What's the price?"

**The contract language to ask for (legal will adjust):**

> Vendor shall not use Customer Data, in any form, for training, fine-tuning, or otherwise improving any machine learning model, whether for Customer's benefit, the benefit of other customers, or any third party. This obligation survives termination of this Agreement. Vendor shall, at Customer's request not more than once annually, provide written confirmation of compliance with this section, including reference to the relevant SOC 2 Type II controls.

### Ask 2 — Data retention and deletion SLA

**What to ask for:** Specific time windows for data retention (active data, logs, backups) and specific commitments on deletion timeline post-cancellation, with verifiability.

**Why:** "We delete data when you cancel" without a timeline can mean 90 days or 2 years. Backup deletion is often months later than active deletion. You need to know.

**Opener:**

> "We need clarity on data retention. Three windows: active data, logs, and backups. And we need a contractually committed deletion timeline post-cancellation, with verification we can produce for our compliance."

**Typical pushback:**

- "Our standard is 30 days." → "30 days for active. What about logs? Backups? Is the 30-day clock on cancellation date or on full deletion?"
- "Backups follow our DR cycle." → "What's the maximum window? We need a number."
- "We can confirm in writing that deletion is complete." → "Can we get that within X days of cancellation, with a specific signed attestation?"

**The contract language:**

> Following termination of this Agreement, Vendor shall delete all Customer Data within thirty (30) days, including from active systems and from backups within ninety (90) days. Vendor shall provide written attestation of completion within forty-five (45) days. The attestation shall identify all systems where Customer Data was stored and confirm deletion from each.

### Ask 3 — Breach notification SLA

**What to ask for:** Specific notification window (typically 24-72 hours), specific named contact for the notification, specific information to be provided.

**Why:** GDPR requires 72-hour notification to regulators; you can't comply if your vendor takes 7 days to tell you. Specific named contact prevents notifications going to a generic support address.

**Opener:**

> "Breach notification needs a specific SLA in writing. We're regulated under [GDPR / HIPAA / SOC 2 / etc.]. We need to know within X hours. Generic 'we'll notify in a reasonable time' doesn't work for us."

**Typical pushback:**

- "We notify within reasonable time." → "Define reasonable. We need 72 hours maximum; we'd prefer 48."
- "We need to confirm before notifying." → "Acceptable, but the SLA starts from your discovery, not from your confirmation. Confirmation can take up to 24 hours, then notification within 48 of confirmation."
- "What constitutes a breach?" → "Per [your regulatory definition]. Any unauthorized access to Customer Data."

**The contract language:**

> Vendor shall notify Customer of any Security Incident affecting Customer Data within 72 hours of Vendor's discovery of the Security Incident. Notification shall be made to Customer's designated security contact (named in Schedule X) and shall include: (i) a description of the incident, (ii) the type and approximate volume of Customer Data affected, (iii) Vendor's initial response and mitigation steps, (iv) Vendor's contact for ongoing communication.

### Ask 4 — Exit terms

**What to ask for:** Specific data export commitments, specific transition support windows, specific commitments on continued service if vendor goes out of business or is acquired.

**Why:** AI vendors are early-stage. Some will exit the market. You need to know your data is portable, your service continues during transition, and your migration off is supported.

**Opener:**

> "Exit terms matter for AI vendors specifically. We need three things: a data export capability we can verify, transition support if we're migrating off, and continuity commitments in case of acquisition or business closure."

**Typical pushback:**

- "We don't anticipate going out of business." → "Neither do we anticipate it. The clause exists for the unlikely scenario."
- "Our standard ToS covers acquisition." → "Define how. We want to see the language. If the new owner can change terms unilaterally, that's not covered."
- "Transition support requires a separate engagement." → "Acceptable, but the rate must be locked in advance and the support obligation must exist."

**The contract language:**

> Upon termination, Vendor shall: (a) provide Customer with the ability to export all Customer Data in a documented, machine-readable format within 30 days; (b) provide reasonable transition support at the rate specified in Schedule Y for up to 90 days post-termination, with a maximum of N hours; (c) in the event of Vendor's acquisition, the acquiring party shall assume all obligations of this Agreement without modification for a minimum of 12 months. Customer may terminate without penalty if Vendor is acquired by an entity Customer reasonably objects to.

### Ask 5 — Model and tokenizer change notification

**What to ask for:** Notification before any change to the underlying model, model version, or tokenizer that materially affects pricing, latency, or output quality.

**Why:** Per the chapter (and example: "Claude Opus 4.7 tokenizer changes can use ~35% more tokens for the same input vs. Opus 4.6"), unannounced model changes can cost you 30%+ overnight. You need lead time to plan and to negotiate.

**Opener:**

> "Model and tokenizer changes can materially affect our economics. We need notification before any change that significantly affects pricing, latency, or output quality, with enough lead time to plan."

**Typical pushback:**

- "Models improve continuously; we can't notify on every change." → "Not every change. Material changes — version bumps, tokenizer changes, capability changes."
- "Our changelog covers it." → "Changelog entries can ship the day of the change. We need 30-day notice on material changes."
- "What's 'material'?" → "Pricing change, tokenizer change, version bump (e.g., Sonnet 4.6 → 4.7), or any change that affects integration points (API shape, response format, rate limits)."

**The contract language:**

> Vendor shall provide Customer with at least thirty (30) days' written notice prior to any Material Change to the Service. "Material Change" includes: (i) changes to pricing, (ii) changes to the underlying model or model version, (iii) changes to the tokenizer, (iv) changes to API shape or response format that may require integration changes, (v) changes to rate limits, (vi) changes to data handling practices. Customer may terminate without penalty if a Material Change adversely affects Customer's use of the Service.

## Other asks worth fighting for

### Asks that are usually winnable

- Named security contact (not a generic ticket queue)
- Audit log exportable to your SIEM
- Sub-processor list and notification of changes
- Specific SLA on response to security questionnaire (if you're customer-facing)
- BAA at Enterprise tier (if you process PHI)

### Asks that require Enterprise tier or larger commitments

- Inference region pinning to a specific country
- BYOK (bring your own key)
- Dedicated tenant infrastructure
- Custom DPA terms beyond standard
- Non-standard data retention windows

### Asks that vendors often refuse but are worth trying

- Specific commitment that no human reviewers see your data without explicit incident-related authorization
- Right to terminate without penalty if vendor's training-on-data policy changes
- Specific commitment to not respond to government data requests without first notifying you (subject to legal restrictions)
- Pricing lock for the contract term

## What to do if the vendor refuses critical asks

The asks aren't all equal. If the vendor refuses:

- **Training opt-out (Ask 1):** non-negotiable for most companies. If the vendor won't put it in writing, walk.
- **Breach notification SLA (Ask 3):** non-negotiable if you're regulated. Walk if needed.
- **Data deletion (Ask 2):** non-negotiable for GDPR / HIPAA / similar. Walk if needed.
- **Exit terms (Ask 4):** strongly preferred but sometimes acceptable to compromise (e.g., 30-day transition support instead of 90).
- **Model change notification (Ask 5):** preferred but compromise possible (e.g., 14 days instead of 30 for less-material changes).

The walk-away is real. Vendors negotiate harder when they believe you'll walk. They negotiate less hard when they believe you've already committed internally.

## Sequence of conversations

A typical procurement negotiation has 3-5 conversations:

1. **Opening conversation.** Vendor presents standard terms. You raise the security review findings and your asks. Vendor's account exec promises to look into it.
2. **Vendor response.** Vendor returns with what they can and can't do. This is when you find out their actual flexibility.
3. **Counter-proposal.** You push back on specific items. Legal counsel writes the clauses.
4. **Final terms.** Vendor agrees or doesn't. If they don't, this is when you walk.

Plan for 4-8 weeks for an Enterprise procurement. Compressed timelines produce concessions you'll regret.

## What this script will NOT do

- Will not work as a one-time script. The negotiation is iterative.
- Will not work without legal counsel writing actual contract language.
- Will not work for single-seat purchases. The standard ToS is what you get.
- Will not work in regulated procurement (gov / defense) without specialized legal expertise.

## Companion artifacts

- [`security-review-template.md`](security-review-template.md) — the input
- [`things-vendors-wont-put-in-writing.md`](things-vendors-wont-put-in-writing.md) — the verbal-only asks
- [`procurement-checklist.md`](procurement-checklist.md) — the final gate
- Ch 38 — source
