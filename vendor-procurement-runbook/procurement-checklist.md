# Procurement Checklist — 21 Items Before Signing

The final gate before signing an AI vendor contract. Run this once the security review is complete and the contract negotiation has produced final terms.

If you can't get a "yes" on at least 17 of 21 items, do not sign. Resolve the gaps first.

## Section 1 — Pre-conditions (4 items)

- [ ] **Security review is complete** — [`security-review-template.md`](security-review-template.md) has been filled out, all CRITICAL findings resolved, all HIGH findings have documented mitigation.
- [ ] **Data classification is determined** — [`data-classification-walkthrough.md`](data-classification-walkthrough.md). The maximum data class this vendor is approved for is documented.
- [ ] **Use cases are scoped** — specifically which teams, which workflows, which data this tool will be used for. Not "broadly." Specifically.
- [ ] **Replacement plan exists** — if this is replacing an existing tool, the migration playbook is identified ([`migration-playbooks/`](../migration-playbooks/)).

## Section 2 — Contract terms (7 items)

- [ ] **Training opt-out** is in the contract with the language from [`contract-terms-negotiation-script.md`](contract-terms-negotiation-script.md) Ask 1.
- [ ] **Data retention and deletion SLA** is specific and committed (Ask 2).
- [ ] **Breach notification SLA** is specific (typically 72 hours or less) and routes to a named security contact (Ask 3).
- [ ] **Exit terms** include data export, transition support, acquisition continuity (Ask 4).
- [ ] **Model and tokenizer change notification** is committed with at least 30-day lead time on material changes (Ask 5).
- [ ] **BAA / specific compliance addendum** is signed if your data class requires it (HIPAA, FedRAMP, etc.).
- [ ] **DPA (Data Processing Agreement)** is signed if you're under GDPR / similar.

## Section 3 — Verification (4 items)

- [ ] **Tenant-level settings verified** — training opt-out, region pinning, audit logging are all confirmed in your tenant, not just claimed in policy.
- [ ] **Audit log export is tested** — you've verified you can pull audit logs into your SIEM.
- [ ] **SSO is configured and tested** — engineers can log in via SSO; admin controls work.
- [ ] **Test workflow runs** — at least one real-shaped workflow has been completed in the procured environment to verify it works as expected.

## Section 4 — Operational readiness (3 items)

- [ ] **Approved tooling matrix updated** — the new tool is added with the agreed data class scope.
- [ ] **Onboarding plan exists** — how engineers get access, what training they need, what the first month looks like.
- [ ] **Renewal calendar reminder set** — 60 days before contract renewal date.

## Section 5 — Financial (3 items)

- [ ] **Pricing locked for contract term** — and the renewal escalator (if any) is documented.
- [ ] **CFO has acknowledged the spend** — annual cost is approved and budgeted.
- [ ] **Cost monitoring is in place** — usage will be tracked monthly; budget alerts configured.

---

## Scoring

- **21 yes:** Sign.
- **17-20 yes:** Sign if the gaps are minor. Document why each gap is acceptable.
- **13-16 yes:** Don't sign. Resolve the gaps first.
- **<13 yes:** Don't sign. Vendor isn't ready or your readiness isn't there.

## When to override the checklist

Almost never. The checklist exists because each item caused a real problem at a real company. Skipping items is fine for short pilot agreements (2-4 week proof of concept with limited scope and data). Skipping for a production contract means you'll meet the same problem the checklist was designed to prevent.

If you must override, document why specifically. The audit trail matters when (not if) the gap surfaces in 12-18 months.

## After signing

- [ ] File the signed contract in your contract management system
- [ ] File the security review in your security records
- [ ] Update the approved tooling matrix
- [ ] Communicate to affected teams
- [ ] Set the renewal calendar reminder
- [ ] Schedule the 90-day post-signing review (verify the tool is being used as scoped)

## Companion artifacts

- [`security-review-template.md`](security-review-template.md)
- [`data-classification-walkthrough.md`](data-classification-walkthrough.md)
- [`contract-terms-negotiation-script.md`](contract-terms-negotiation-script.md)
- [`things-vendors-wont-put-in-writing.md`](things-vendors-wont-put-in-writing.md)
- [`renewal-discipline.md`](renewal-discipline.md)
- Ch 38 — source
