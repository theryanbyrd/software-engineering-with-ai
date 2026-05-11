# Things Vendors Won't Put in Writing — and How to Handle

The asks vendors will agree to verbally and refuse on paper. This file is for the engineering and procurement leads who need to know which verbal commitments are durable and which aren't.

## The pattern

In an enterprise procurement conversation, the vendor's account exec will agree to many things. Some make it into the contract; some don't. The pattern is consistent enough across vendors that you can predict which asks will be paper-resistant.

The vendor's reasoning:

- Some asks would commit them to behavior they can't reliably deliver
- Some asks would set precedent for other customers
- Some asks would expose them to legal liability they can't quantify
- Some asks are technical promises the contract drafters don't understand
- Some asks are simply outside the standard contract template and adding takes too much legal cycles

The verbal commitment is not a lie. The account exec means it. But verbal commitments at signing don't bind in 18 months when the original AE has left the company, the contract is being renewed, or your team is in a dispute.

## The asks that are typically verbal-only

### "We'll prioritize your support tickets"

**What you'll hear:** "Yes, your tickets will get priority handling. You're a strategic customer."
**Why it's not in writing:** Priority is relative; defining it contractually requires defining the queue, the comparison, and the SLA — which the vendor can't do without exposing themselves.
**Risk if relied on:** Two years in, when the AE is gone and you have a real urgent ticket, your priority is whatever the support team's queue currently does.

**How to handle:**
- Get a specific named contact (acceptable in writing usually): "Our support contact for this tier is [name@vendor.com]."
- Get a specific SLA on response time, even if generic: "P1 tickets answered within 4 business hours."
- Don't rely on "priority" as a verbal commitment for actual urgent issues.

---

### "We'll work with you on custom features"

**What you'll hear:** "Yes, our roadmap is responsive to enterprise feedback. We'll prioritize your asks."
**Why it's not in writing:** Roadmap commitments are seen as a forward-looking promise the vendor can't guarantee.
**Risk if relied on:** The feature you were promised six months ago is "still on the roadmap" indefinitely.

**How to handle:**
- For features critical to your evaluation, get them in writing as deliverables with a date — even if the date is generous (12-18 months).
- For features that are nice-to-have, accept the verbal commitment but plan as if they won't ship.
- Don't sign a contract whose value depends on a feature that doesn't exist yet, unless that feature is contractually committed.

---

### "We'll grandfather your pricing"

**What you'll hear:** "We can lock your rate for the contract term."
**Why this CAN go in writing (if pushed):** Pricing locks are standard. Often the AE just doesn't volunteer it.
**Risk if relied on as verbal-only:** "We promised pricing wouldn't change" doesn't survive when the next contract has new terms.

**How to handle:**
- Insist on the pricing lock in the contract, including for renewal.
- If the vendor won't lock pricing, that's a finding — what does it mean about renewal posture?
- For contracts longer than 1 year, pricing escalator clauses (e.g., max 5% / year) are reasonable but should be in writing.

---

### "Your data is encrypted and isolated"

**What you'll hear:** "Yes, we encrypt at rest and in transit. Each customer is isolated."
**Why it's vague in writing:** Vendors don't want to commit to specific encryption algorithms or specific isolation mechanisms because both might change.
**Risk if relied on as verbal-only:** "Encrypted" might mean disk-level encryption (almost meaningless) or per-customer keys (much stronger). "Isolated" might mean logical (database column) or physical (separate database). The verbal version doesn't distinguish.

**How to handle:**
- Get specific in writing: "Encryption at rest using [algorithm]; encryption in transit using [TLS version]; per-customer encryption keys (yes/no); data isolated at [logical / physical / per-tenant infrastructure] level."
- If the vendor refuses to be specific, that's a finding. Either escalate or downgrade your data-class approval for this vendor.

---

### "Our security team is responsive"

**What you'll hear:** "Yes, we have a dedicated security team. They're responsive."
**Why it's not in writing:** Defining "responsive" with an SLA is hard.
**Risk if relied on:** When you have an actual security question 14 months in, you find out "responsive" means 5 business days.

**How to handle:**
- Get a named security contact in the contract.
- Get an SLA on security inquiries (e.g., 2 business days for non-urgent).
- For ongoing audit / compliance work, get the cadence locked: "Annual SOC 2 review; quarterly compliance check-in."

---

### "We won't access your data"

**What you'll hear:** "Our staff don't access customer data. Only for support, when authorized."
**Why it's vague in writing:** "Authorized" is doing a lot of work. The standard contract language usually allows internal access for "support, debugging, fraud prevention, security investigations, and operational purposes" — which is most of what someone might want to access for.
**Risk if relied on as verbal-only:** Your data is accessible to the vendor's staff under broad operational categories. Some staff may have access without ever needing to formally invoke "authorized" reasoning.

**How to handle:**
- Get the access categories enumerated in writing.
- Get audit log requirements: every access logged, available to you on request.
- Get specific commitment that customer-data access by support staff requires customer ticket / approval (where feasible).

---

### "We'll honor your tenant settings"

**What you'll hear:** "Your training opt-out / region preference / privacy settings are honored. They take effect immediately."
**Why it's vague in writing:** Vendors don't want to commit to immediate technical enforcement; some settings cascade through systems gradually.
**Risk if relied on as verbal-only:** "Training opt-out" might be honored in policy but not in technical isolation; new employees onboarding to vendor systems might not have the policy enforced.

**How to handle:**
- Get the technical enforcement mechanism documented in writing: how is the setting enforced; what's the audit; what happens on violation?
- For training opt-out specifically: contractual language with audit rights (see [`contract-terms-negotiation-script.md`](contract-terms-negotiation-script.md) Ask 1).
- For region pinning: specific guarantee in writing of which regions are used; notification on changes.

---

### "We'll notify you before changes"

**What you'll hear:** "Yes, we'll notify customers before any material changes."
**Why it's vague in writing:** "Material" and "before" are squishy.
**Risk if relied on as verbal-only:** Notification might be a blog post the day of the change.

**How to handle:**
- Get specific lead times in writing: 30 days for material changes, defined.
- Get the notification mechanism specified: email to a named contact, not a blog post.
- See [`contract-terms-negotiation-script.md`](contract-terms-negotiation-script.md) Ask 5.

---

### "We're committed to this product"

**What you'll hear:** "We're investing heavily in this product. It's a strategic priority."
**Why it's not in writing:** Vendors can't commit to product investment in contract terms; their strategy might change.
**Risk if relied on:** The product is end-of-lifed in 18 months and you've built infrastructure on it.

**How to handle:**
- Get exit terms that work even if the product is end-of-lifed (see Ask 4 in the negotiation script).
- Get sunset notice in writing: "If product is end-of-lifed, customer receives 18 months notice and migration support."
- Don't bet your roadmap on a vendor's strategic intentions; bet it on your contract.

---

### "We don't sell to your competitors" (or some variant)

**What you'll hear:** "Yes, we serve [your industry] but [reasons why your situation is different]."
**Why it's not in writing:** Anti-competitive provisions are legally tricky and vendors avoid them.
**Risk if relied on:** Your competitor signs the same vendor next quarter.

**How to handle:**
- Don't ask for exclusivity from horizontal-platform vendors. It's never going to happen.
- For specialized vendors (e.g., a specific industry-vertical AI tool), exclusivity in your sub-segment is occasionally negotiable for very large contracts.
- Generally: assume competitors can use the same tools. Differentiation comes from your harness, not your tool selection.

---

## What to do with the verbal-only asks

### Test commitment by asking for paper

When the AE makes a verbal commitment, the test: "Can we get that in writing?"

- If "yes, easy" → ask for it. Sometimes it just wasn't volunteered.
- If "let me check with legal" → wait for the answer. Often they come back with partial language; partial is better than none.
- If "no, but you have my word" → assume the verbal commitment doesn't bind. Treat the contract as the floor.
- If "we don't put that in writing for anyone" → red flag. Either it's a standard practice that won't be supported, or it's something they don't want a paper trail on.

### Get the AE's commitments in email

If something can't go in the contract but the AE is committing to it, get it in email:

> "Just to confirm what we discussed: [specific commitment]. Is this consistent with how [vendor] approaches [topic]?"

Email isn't a contract. But:
- It documents the conversation
- It surfaces if the AE was overcommitting
- It helps your future self (or the AE's successor) understand what was agreed

### Plan for the verbal-only ask to fail

For each verbal-only commitment you're relying on:

- What's plan B if it fails?
- What's the cost of plan B?
- Is the cost acceptable?

If plan B is cost-acceptable, the verbal-only ask is fine to rely on. If plan B is catastrophic, don't rely on the verbal-only.

### Renew the conversation at every renewal

At every contract renewal, the AE may have changed. Re-test the verbal commitments:

> "Last year we discussed [topic]. Can you confirm that's still the company's posture?"

If the new AE doesn't recognize the commitment, you have your answer.

## What this guide will NOT do

- Will not turn unwilling vendors into willing ones. Some asks are simply not on the table.
- Will not protect against bad-faith vendors. The discipline assumes you're working with a vendor who means well; protection against malicious vendors is a different domain.
- Will not work without legal counsel reviewing the actual contract.

## Companion artifacts

- [`security-review-template.md`](security-review-template.md) — the upstream review
- [`contract-terms-negotiation-script.md`](contract-terms-negotiation-script.md) — what TO get in writing
- [`procurement-checklist.md`](procurement-checklist.md) — the final gate
- Ch 38 — source
