# AI Vendor Security Review Template

The structured security review every AI vendor goes through before procurement. Run this BEFORE the contract conversation, not after — the security findings inform the negotiation.

> Anything where the answer is "we don't disclose that" is a finding.
>
> — Ch 38

The review takes 4-8 hours of focused time across security, engineering, and legal. Don't shortcut it. The cost of catching a problem at procurement is much lower than the cost of catching it after deployment.

## How to use this template

1. Copy this file. Rename to `vendor-name-security-review-YYYY-MM-DD.md`.
2. Fill in the vendor info section.
3. Send the questionnaire (Section 3) to the vendor's solutions / security team. Allow 5-10 business days for response.
4. While awaiting response, run the public-information research (Section 2).
5. When the response comes back, review with security lead.
6. Score each finding (Section 4). Make the procurement recommendation (Section 5).

---

## Section 1 — Vendor info

| Field | Value |
|---|---|
| Vendor name | |
| Product name | |
| Product version / tier | (e.g., Enterprise, Business, Pro) |
| Reviewer | @handle |
| Review date | YYYY-MM-DD |
| Target deployment | (number of seats, expected token volume, departments) |
| Estimated annual cost | $___ |
| Replacing what (if anything) | |
| Procurement deadline | YYYY-MM-DD |

---

## Section 2 — Public-information research

Complete these before sending the questionnaire. The vendor's public posture tells you a lot.

### Trust center / security page

- [ ] Vendor publishes a trust center or security page
- [ ] Trust center is current (last updated within 6 months)
- [ ] SOC 2 Type II report is downloadable (after NDA)
- [ ] ISO 27001 certificate is published

If the vendor doesn't publish any of this: major finding. Either they're early-stage (which is its own risk) or they're hiding something.

### Public security incidents

Search for the vendor name + "breach" / "incident" / "leak" / "vulnerability" over the past 24 months.

- [ ] Any reported incidents in the past 24 months
- [ ] If yes: vendor disclosed publicly, with timeline
- [ ] If yes: post-incident remediation documented

Search results: [paste relevant findings]

### Trust signals

- [ ] FedRAMP authorization (if relevant)
- [ ] HIPAA BAA available (if relevant)
- [ ] PCI DSS attestation (if relevant)
- [ ] StateRAMP / IL5 (if relevant for your sector)
- [ ] Specific industry compliance (FINRA, CMMC, ITAR, etc.)

### Vendor health

- [ ] Funding stage and runway (recent layoffs?)
- [ ] Customer churn signals (recent customers cancelling publicly)
- [ ] Leadership stability (recent C-suite changes?)
- [ ] Product roadmap volatility (frequent pivots?)

These aren't security per se but they predict whether the vendor will exist in 18 months.

---

## Section 3 — Vendor questionnaire

Send this to the vendor's security or solutions team. Expect 5-10 business days for response. Anything they don't answer is a finding.

### Data handling

1. Does customer code or data train your models?
   - **If yes:** under what conditions? Default opt-in or opt-out? Can we opt out at the tenant level?
   - **If no:** how is this enforced technically? What audit trail confirms?
   - **Verbatim contract language?** [paste their answer]

2. Where is inference performed?
   - Region / country?
   - Configurable per tenant?
   - What does "inference" include — completion, embedding, fine-tuning?

3. What is your data retention policy?
   - For request/response data?
   - For training data (if applicable)?
   - For backup / disaster recovery copies?
   - Contractual SLA on data deletion after cancellation?

4. Do you sub-process customer data?
   - List of sub-processors?
   - Notification SLA on sub-processor changes?
   - Customer right to object to sub-processor changes?

5. What customer data is logged?
   - Request payloads (full or sampled)?
   - Response payloads?
   - Metadata only?
   - Retention on logs?

### Model and inference

6. What models can we use? Specifically named, with version strings.

7. What is your model and tokenizer change policy?
   - Versioned APIs that allow pinning?
   - Notification window before changes?
   - Tokenizer changes documented?

8. Can we run on our own keys / infrastructure?
   - BYOK (bring your own key)?
   - On-prem partner deployments (Bedrock, Vertex, Azure)?
   - Self-hosted model option?

9. What is the inference SLA?
   - Latency p50, p95, p99
   - Availability target
   - Credit policy on SLA breach

### Security and compliance

10. Have you been audited (SOC 2 Type II, ISO 27001, etc.)?
    - Audit reports available under NDA?
    - Date of most recent audit?
    - Any open findings?

11. Can we sign a BAA (HIPAA Business Associate Agreement)?
    - On which tier?
    - Covers what specific data flows?

12. Is FedRAMP authorization available?
    - Authorization level (Moderate, High)?
    - Direct or via cloud provider?

13. What logging / audit is exposed?
    - Audit log of who-accessed-what?
    - Exportable to our SIEM?
    - Retention?

14. What is your incident notification SLA?
    - For breaches?
    - For service disruptions?
    - For changes that affect security posture?

### Governance and access

15. What admin controls do org administrators have?
    - User provisioning (SCIM)?
    - SSO required (SAML, OIDC)?
    - Role-based access?
    - Tenant-level configuration locks?

16. What is your access control for support staff?
    - Can vendor staff see customer data?
    - Under what circumstances?
    - Logged?

### Operational

17. What is your data deletion SLA?
    - On account cancellation?
    - On individual record request (GDPR)?
    - Verifiable how?

18. What is your business continuity / disaster recovery posture?
    - RTO / RPO?
    - Geographic redundancy?
    - Last DR test?

19. What is your supply chain security posture?
    - Code signing?
    - Dependency vulnerability scanning?
    - SBOM available?

### Specific to AI

20. What is your prompt injection mitigation?
    - System-prompt isolation?
    - Tool / MCP permission boundaries?
    - Detection for injection attempts?

21. What logging exists around agent actions?
    - Tool calls?
    - File modifications?
    - Code execution?

22. How do you handle data leakage via training?
    - If we accidentally send sensitive data, is it durably in the model?
    - What's the deletion path?

---

## Section 4 — Findings

Score each finding by severity:

- **CRITICAL** — would block procurement; must be resolved before signing
- **HIGH** — would block procurement at scale; can pilot with mitigation
- **MEDIUM** — known risk; document and accept or mitigate
- **LOW** — note only; doesn't block

| # | Finding | Severity | Source (question #) | Mitigation | Resolution |
|---|---|---|---|---|---|
| 1 | (e.g., Vendor cannot provide BAA on this tier) | HIGH | 11 | Restrict to data classes that don't require BAA | Pending vendor response on Enterprise tier |
| 2 | (e.g., Inference region not configurable) | MEDIUM | 2 | Acceptable for non-EU data; restrict EU tenant if/when applicable | Accepted |
| ... | | | | | |

---

## Section 5 — Recommendation

### Approve

- [ ] Approve for all data classes
- [ ] Approve for [specific data classes only]
- [ ] Approve for pilot only (limited scope, time-boxed)

### Conditions

- [ ] (specific conditions that must be met before deployment)

### Decline

- [ ] Decline due to [specific findings]

### Defer

- [ ] Defer pending [specific items vendor must address]
- Re-review date: YYYY-MM-DD

### Reasoning

> 2-3 paragraphs explaining the recommendation. Cite specific findings. Address why findings of HIGH or CRITICAL severity (if any) are mitigated or why the vendor is being declined.

---

## Section 6 — Sign-off

- [ ] Engineering sign-off: @handle on YYYY-MM-DD
- [ ] Security sign-off: @handle on YYYY-MM-DD
- [ ] Legal sign-off: @handle on YYYY-MM-DD (review of vendor's standard ToS, DPA, BAA)
- [ ] Procurement sign-off: @handle on YYYY-MM-DD (commercial terms reviewed)

If any sign-off is held, the procurement does not proceed.

---

## Common red flags

If you see these, treat as automatic findings:

- **"We don't disclose that."** Per Ch 38 — finding.
- **"It's in our trust center."** Verify what's actually there. Often the trust center is a marketing page.
- **"That's a custom enterprise feature."** Means the vendor wants to upsell. May or may not be available.
- **"We're working on that."** Means it doesn't exist. Treat as not-existing for procurement purposes.
- **"Our SOC 2 covers that."** Verify in the actual SOC 2 report. SOC 2 covers what the vendor's controls cover, which may not be what you need.
- **"We can't put that in writing but we promise."** See [`things-vendors-wont-put-in-writing.md`](things-vendors-wont-put-in-writing.md).

## Common green flags

- The vendor's security team is responsive (replies within 2-3 business days)
- The vendor publishes their sub-processor list publicly
- The vendor has a public bug bounty program
- The vendor's terms include explicit "no training on customer data" language at the tier you're buying
- The vendor has been audited recently and findings are documented

## After the review

- File the completed review in your security records
- Add the vendor to the approved tooling matrix with the agreed data classes
- Set the renewal calendar reminder (see [`renewal-discipline.md`](renewal-discipline.md))
- If declined: document why; review again at next request

## Companion artifacts

- [`data-classification-walkthrough.md`](data-classification-walkthrough.md) — what data classes apply
- [`contract-terms-negotiation-script.md`](contract-terms-negotiation-script.md) — language to negotiate
- [`things-vendors-wont-put-in-writing.md`](things-vendors-wont-put-in-writing.md) — verbal-only asks
- `executive-strategic-kit/security-questionnaire-answers.md` — the inverse: when customers send YOU questionnaires
- Ch 38 — source
