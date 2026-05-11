# Renewal Discipline — What to Re-Verify on Every Renewal

Per Ch 38:

> Read the current ToS and DPA. Re-read on every renewal — vendors change terms.

This file is the structured re-verification work. Run 60 days before contract renewal.

## The cadence

| Time before renewal | Action |
|---|---|
| 60 days | Renewal review starts; this checklist runs |
| 45 days | Negotiation conversations begin if anything has changed |
| 30 days | Renewed contract terms agreed; legal reviews |
| 14 days | Final terms signed |
| Renewal date | New contract takes effect |

If you don't start at 60 days, you're negotiating under deadline pressure, which produces concessions you'll regret.

## Section 1 — What might have changed

These are the things vendors change at renewal — sometimes silently, sometimes with announcement.

### Pricing

- [ ] Compare current pricing to standard pricing on vendor's site
- [ ] Check for new tiers, packaging changes
- [ ] Check for new add-ons (often where the cost increase lives)
- [ ] Verify the lock from the original negotiation still applies

### Terms of Service

- [ ] Diff the current ToS against the version in your signed contract
- [ ] Pay specific attention to: data handling, training opt-out, sub-processors, dispute resolution, governing law
- [ ] Note: most vendors' ToS update silently. The MSA or addendum may override the public ToS, but verify.

### Data Processing Agreement

- [ ] Check sub-processor list for additions
- [ ] Verify region commitments are unchanged
- [ ] Check breach notification SLA is unchanged

### Training opt-out

- [ ] Verify your tenant setting is still set to opt-out
- [ ] Verify the contractual language is still in your signed addendum (some vendors try to silently move this to the ToS, where it can be changed unilaterally)
- [ ] If the vendor has changed posture publicly (announced new training models, new features that train on data), investigate harder

### Models and capabilities

- [ ] Check what models are available now vs. when you signed
- [ ] Verify your model pinning still works (your integrations haven't been silently routed to new models)
- [ ] Check tokenizer changes for cost impact (the Claude Opus 4.7 example: "~35% more tokens for the same input vs. Opus 4.6")
- [ ] Check rate limits and quotas

### Compliance and certifications

- [ ] SOC 2 Type II — current report available?
- [ ] ISO 27001 — current certificate?
- [ ] FedRAMP / HIPAA / etc. — still in good standing?
- [ ] Any new findings or audit issues disclosed?

### Vendor health

- [ ] Recent funding / acquisitions / leadership changes?
- [ ] Customer churn signals?
- [ ] Public security incidents in the past 12 months?

## Section 2 — What you've learned

These are the things YOU should re-verify based on a year of actual use.

### Did the vendor honor the contract?

- [ ] Breach notifications: did any happen? Did they notify within the SLA?
- [ ] Audit log export: still works?
- [ ] Support response: meets the SLA?
- [ ] Named security contact: still responsive?

### Did the tool earn its keep?

- [ ] Adoption: which teams are actually using it; for what?
- [ ] Cost: is the spend in line with what was budgeted?
- [ ] Productivity: per the six-metric dashboard (Ch 31 §31.1), is there evidence of value?
- [ ] Specific incidents: any AI-related incidents traced to this tool? (cross-reference with [`incident-postmortem-templates/`](../incident-postmortem-templates/))

### Has your need changed?

- [ ] Are there new use cases that this tool covers / doesn't cover?
- [ ] Are there data classes that have moved (e.g., new compliance scope)?
- [ ] Has the team's workflow shifted in ways the tool now serves better or worse?

## Section 3 — What the market has done

The market for AI tools moves fast. Renewal is when you check the alternatives.

### Competitor landscape

- [ ] What new vendors have entered the space?
- [ ] What capabilities exist now that didn't exist when you signed?
- [ ] Are competitor prices materially different now?
- [ ] Is your benchmark (`benchmarks/`) telling you another tool would do better?

### Specific moves to consider

- [ ] Should you negotiate a better deal based on competitive offers?
- [ ] Should you actually switch? (Run [`migration-playbooks/`](../migration-playbooks/) if yes.)
- [ ] Should you cancel? (If the tool isn't earning its keep, cancellation is a real option.)

## Section 4 — The renewal decision

Based on the above, one of four outcomes:

### Renew as-is

- [ ] All terms unchanged or improved
- [ ] Tool is earning its keep
- [ ] No better alternative
- [ ] Renew with the same terms

### Renew with renegotiation

- [ ] Some terms have shifted; renegotiate to restore or improve
- [ ] Cost optimization (different tier, fewer seats, different add-ons)
- [ ] Add or strengthen specific protections (training opt-out language, exit terms)

### Renew with reduced scope

- [ ] Tool is earning its keep but the scope is wrong
- [ ] Reduce seats, restrict use cases, drop unused add-ons
- [ ] Renew the smaller contract

### Don't renew

- [ ] Tool isn't earning its keep
- [ ] Better alternative has emerged
- [ ] Run [`migration-playbooks/`](../migration-playbooks/) for the migration off
- [ ] Communicate to affected teams 60 days before contract end

## Section 5 — The renewal conversation

If renewing, the conversation:

> "We're approaching renewal on [date]. We'd like to discuss [specific items]: [pricing / specific term / specific feature / etc.]. Our usage over the past year has been [summary]. Based on our review, we're considering [renew as-is / renew with changes / consider alternatives]. What's the path forward?"

The vendor's account exec wants the renewal. They have flexibility they may not volunteer. Use it.

If pricing is the main issue:
- Get a competitive quote from a comparable vendor (even if you don't intend to switch)
- Use the quote as anchor in the renewal conversation
- "Vendor X is offering similar capabilities at $Y. We'd like to renew but we need pricing in this range."

If terms are the main issue:
- Reference the specific terms that have shifted
- Reference your security review's continued requirements
- "When we signed, [training opt-out / specific term] was committed. We need that to continue."

## Section 6 — After renewal

- [ ] File the renewed contract
- [ ] Update the security review with the new terms
- [ ] Update the approved tooling matrix if anything changed
- [ ] Set the next renewal calendar reminder (60 days before next renewal date)
- [ ] Communicate any changes to affected teams

## What this discipline will NOT do

- Will not save you if you skip it. Vendors who change terms without notification rely on customer inattention.
- Will not work as a one-time event. The discipline is the cadence.
- Will not work without engaged procurement and security. Engineering can't do this alone.

## Companion artifacts

- [`security-review-template.md`](security-review-template.md) — re-run the relevant sections at renewal
- [`contract-terms-negotiation-script.md`](contract-terms-negotiation-script.md) — for renegotiation
- [`procurement-checklist.md`](procurement-checklist.md) — re-verify the gates
- [`migration-playbooks/`](../migration-playbooks/) — if not renewing
- Ch 38 — source
