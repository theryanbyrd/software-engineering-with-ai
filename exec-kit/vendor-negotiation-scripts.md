# Vendor Negotiation Scripts

Three conversations every VP of Engineering should be ready to have with their AI tooling vendors. Use these as starting drafts; the specifics will depend on your relationship and leverage.

**Owner:** VP of Engineering, in coordination with Procurement / Finance.

**Cadence:** As needed — usually annually at renewal, plus whenever vendor terms materially change.

---

## Script 1 — The "we're seriously evaluating an alternative" conversation

**Use when:** Renewal is in 60-120 days. You have at least one credible alternative on the shortlist. You want better commercial terms, contractual guarantees, or services bundled in.

**Trigger:** Schedule the call yourself — don't wait for the vendor's CSM to reach out for renewal. Doing this 60-120 days out gives you leverage that disappears at 30 days.

### Opening

> "Thanks for making time. I want to be direct because I respect your time and ours: we're seriously evaluating [specific alternative — name it] to replace [current vendor] for the team's [specific scope: 'agentic coding tasks' or 'IDE assistant for the platform team' or whatever]. Our team has [N seats] across [scope]. I haven't made a decision yet, and I'd genuinely prefer to renew with you if the terms work for us. Before we go further, I want to understand what the conversation looks like if we wanted to consolidate on you for the next 24 months."

### What to ask for

- **Multi-year discount.** 10-25% off list is realistic for a 24-month commitment with a meaningful seat count. 30%+ is achievable if you have demonstrated alternatives and they have demonstrated competition.
- **Included professional services.** Half-day workshop, harness setup support, custom skill creation, sample CLAUDE.md derived from your codebase. Usually free if you ask.
- **Favorable training-data terms.** Explicit no-training clause in writing, with notice obligation if terms change.
- **BAA at no extra cost.** If you have any healthcare, finance, or regulated-data exposure, this matters.
- **Named CSM and technical contact.** With escalation path. Most vendors have these but don't surface them by default.
- **Audit log and SCIM access included.** Should be table stakes; sometimes isn't.
- **Price hold.** Even without a discount, locking your current rate for the term protects you against price increases.

### What to push back on if offered

- "We'll add 5% if you sign a 3-year." Too long. The market is moving too fast; 24 months is your max.
- "Discount in exchange for case study." Acceptable if the case study is voluntary and you control the content. Not acceptable if it's mandatory or if they get to use your name in marketing without per-instance approval.
- "We'll waive setup fees." Setup fees on AI tooling are usually fictional. This isn't a concession.

### Closing

> "Send me the formal proposal by [date]. If the terms work, we'll renew. If they don't, we'll move forward with [alternative]. Either way, no hard feelings — we've appreciated working with you."

This is the polite version of "give me your best offer." Vendors respect it more than vague hand-wringing.

---

## Script 2 — The "April 2026 happened, what's the renewal look like" conversation

**Use when:** A vendor has changed terms in a way that affected your trust — training opt-in changed, pricing model changed, a feature you depended on was deprecated. You're renewing despite the friction; you want guarantees that the next surprise doesn't happen.

**Specific triggers:**
- GitHub Copilot's April 2026 default opt-in for training (forced existing customers to manually re-confirm opt-out)
- Cursor's mid-2026 transition to compute-based pricing
- Several AI vendors' deprecations of API endpoints with <60 day notice
- Any model-version EOL that broke your harness

### Opening

> "Want to talk about renewal. When [vendor] changed [training opt-in / pricing / API terms / specific change] in [month], that hit our trust in your roadmap. We're renewing — we like the product — but for the next term I need specific contractual guarantees that the next change doesn't catch us off guard the same way."

### What to ask for

- **90-day notice on material changes.** Define "material" in the contract: pricing structure, training opt-in defaults, API deprecation, BAA terms, data residency. 90 days is the minimum for a mid-size company to react. 120+ days is better.
- **Contractual no-training commitment.** If the vendor's policy changed, get the no-training commitment into your specific contract, not relying on the published policy.
- **Pricing protection.** Lock the current rate, or cap increases at CPI, for the term.
- **Escape clause for material changes.** If the vendor changes a material term mid-contract, you have the right to exit early without penalty. This is rarely offered but often agreed to.
- **API stability commitment.** "No deprecation of currently-used endpoints with less than [N] days notice; if deprecation happens, vendor will provide migration support."
- **Written acknowledgment of the prior issue.** Sometimes useful for your own records when you have to explain to your CFO why you're renewing.

### Tone

Not aggressive. Not whiny. Specific and direct. The vendor's CSM heard the same complaint from 50 other customers — your job is to be the one who got specific contractual remedies, not the one who vented.

### Closing

> "If you can come back to me with most of those, we'll renew. If not, we'll need to discuss whether we can renew at all, given how exposed we are to the next surprise."

---

## Script 3 — The "we want a credit" conversation

**Use when:** A specific incident has cost you measurable time or money — vendor outage, model regression, breaking API change, feature removal. You don't want to cancel, but you want acknowledgment.

**Specific triggers:**
- Multi-hour vendor outage during a release
- Model regression that produced bad output for a workload until you noticed
- Feature deprecation with insufficient notice that broke your harness
- Quota error that blocked your team for half a day

### Opening

> "Want to flag something specific from [date / event]. Our team experienced [specific issue — be precise: 'the API was returning 503s for 4 hours during our scheduled migration window' or 'the model started returning malformed JSON in 12% of requests, which we tracked back to your release notes from N days ago']. The business impact for us was [estimable: 'a half-day of engineering time across 8 people, so roughly $X loaded' or 'a delayed release that affected [specific revenue or customer commitment]']."

### What to ask for

- **Credit equivalent to N% of next quarter's spend.** 5-15% is reasonable for a single incident, depending on severity.
- **Extension of current rate** for next renewal. Sometimes easier to grant than a credit.
- **Pre-paid services hours.** Workshop time, custom skill creation, etc.
- **Improvement commitment.** "We expect to see [specific change in vendor's notification or stability procedures]." Sometimes the credit isn't the point; the change is.

### What NOT to ask for

- Cash refunds. Vendors almost never give these and asking signals naivete.
- Compensation for downstream business impact. "Our customer churned because of your outage." Almost never collectible.
- Apology in writing. Pointless theater.

### Closing

> "I'm not going anywhere over this — we've been good partners. I want this acknowledged in a way that's commensurate with the impact. What can you offer?"

---

## General principles across all three

### Be specific

"Things have been frustrating" gets nothing. "On April 14, the training opt-in default changed, and three of our enterprise customers asked us about it within 48 hours, requiring 6 hours of unbudgeted security questionnaire response time across legal, security, and engineering" gets something.

### Document business impact

The vendor's account team reports up to a finance organization that needs justifications. Give them the justification. Estimable hours, estimable cost, estimable customer or revenue impact.

### Have alternatives ready

You don't need to actually move. You need to credibly threaten to. The credibility is the leverage.

### Don't burn the relationship

The CSM and AE you're talking to are individuals with quotas and bosses. Be firm but professional. Today's CSM is tomorrow's referenced VP at another vendor.

### Get it in writing

Verbal commitments from vendors don't survive renewal cycles, account changes, or company restructuring. Whatever you negotiate, get in writing — ideally in the contract, at minimum in an email exchange you save.

### Renewal is the only time the leverage is real

Asking for concessions mid-term is much harder than asking at renewal. Plan your asks for renewal windows; flag issues as they happen so you have ammunition at renewal.

---

## Customization checklist

For each script, before the call:

- [ ] Replace `[vendor]`, `[N seats]`, `[scope]`, etc. with actual specifics
- [ ] Pull the actual numbers (current spend, alternative pricing, business impact)
- [ ] Confirm with Procurement/Legal that you have authority to negotiate these terms
- [ ] If multi-year commit is on the table, confirm with Finance that the budget supports it
- [ ] Decide your walk-away terms in advance — what's the minimum you'd accept to renew?
- [ ] Practice the opening line out loud once so it lands naturally
