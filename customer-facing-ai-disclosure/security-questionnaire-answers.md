# Security Questionnaire Answers — Comprehensive Version

The comprehensive answers to AI-related questions on enterprise customer security questionnaires. More detailed than the version in `executive-strategic-kit/security-questionnaire-answers.md` because some customers ask deeper.

## How to use this document

1. Customer sends a security questionnaire. Read it carefully.
2. Identify the AI-related questions (often in sections about "subprocessors," "data handling," "development practices," or specific "AI/ML" sections).
3. Match to the answers below. Adapt to your specifics.
4. **Get legal review on every customer-facing version.** This document is a template; the actual response goes through your standard customer-comm review.
5. Track which answers each customer received. Consistency matters; if Customer A and Customer B received different answers and they compare notes, that's a problem.

The answers below are written in a tone calibrated to enterprise customers. Adjust tone for your buyers — some customers expect more formal language; some expect plainer.

---

## Section A — Internal AI tool usage

### Q: Do you use AI tools in your software development process?

**Answer:**

> Yes. Our engineering organization uses AI-assisted development tools as part of our standard development workflow. Specifically:
>
> - **Code authoring and review assistance:** [list approved tools — e.g., Claude Code, GitHub Copilot, Cursor]. These tools are used by our engineers under explicit governance policies described below.
> - **Code analysis and testing:** AI tools assist in test generation, code review, and static analysis as part of our CI pipeline.
> - **Documentation:** AI tools assist in generating release notes, API documentation, and internal engineering documentation.
>
> Our use of AI tools is governed by an internal policy that includes data classification matrix, approved tooling list, and explicit prohibitions on certain data flows. Details available under NDA.

### Q: Which specific AI tools are approved for use on customer-related code or data?

**Answer (adapt the specific list and tiers):**

> The following AI tools are currently approved for use on customer-related code:
>
> | Tool | Tier | Approved for | Restrictions |
> |---|---|---|---|
> | Claude Code | Enterprise | Customer code (with BAA-equivalent terms) | No PII; no payment data |
> | GitHub Copilot | Business / Enterprise | Customer code (no customer data) | Inline suggestions only on approved repos |
> | [Other approved tool] | [Tier] | [Scope] | [Restrictions] |
>
> Personal-account AI tools (consumer Claude.ai, ChatGPT, etc.) are not permitted on customer code or data. We have an internal compliance program that audits this monthly.

### Q: Do these AI tool vendors train their models on your data, or by extension on our data?

**Answer:**

> No. Our contracts with AI tool vendors include explicit, contractual prohibitions on training on customer data (where "customer data" includes our code and any data that flows through it). Specifically:
>
> - The "no training on data" provision is in our Master Services Agreement with each vendor, not just in their public ToS (which may change unilaterally).
> - We have audit rights, exercised annually, to verify the prohibition is honored.
> - Tenant-level technical controls are configured to enforce the prohibition.
>
> Our procurement process for AI vendors (documented internally) requires this provision before any vendor is approved.

### Q: Where is your AI vendors' inference performed (geographic region)?

**Answer:**

> We use AI vendors with the following inference region commitments:
>
> | Vendor | Inference region(s) | Configurable |
> |---|---|---|
> | [Vendor 1] | US-East / US-West | Yes (configurable per tenant) |
> | [Vendor 2] | US, EU | Yes |
> | [Vendor 3] | US (default), EU available with Enterprise tier | Yes |
>
> If your data sovereignty requirements require specific region commitments, we can document these for your specific account upon request.

### Q: How long do AI vendors retain data submitted through their tools?

**Answer:**

> Per our contracts:
>
> - **Active data:** retained for the duration of the request (typically <60 seconds for inference); not persisted longer.
> - **Logs:** vendor-side request/response logs retained for [N] days for operational purposes; we have visibility into our usage logs.
> - **Backup/DR copies:** purged within [N] days per vendor disaster recovery cycle.
> - **On contract termination:** all data deleted from vendor systems within 30 days of cancellation, with written attestation provided within 45 days.

---

## Section B — AI-authored code in your product

### Q: What percentage of code shipped to your product is AI-authored or AI-assisted?

**Answer (calibrate honestly to your data):**

> We track this via PR labeling per the convention:
>
> - `ai:none` — entirely human-written
> - `ai:assisted` — significant AI authorship, reviewed in detail
> - `ai:authored` — primarily AI-generated, double-reviewed
> - `ai:agent` — produced by an autonomous agent run
>
> Approximate distribution as of [most recent quarter]:
>
> - `ai:none`: [N]%
> - `ai:assisted`: [N]%
> - `ai:authored`: [N]%
> - `ai:agent`: [N]%
>
> Important note: every PR, regardless of authorship classification, goes through human review by a qualified engineer before merging to main. AI authorship does not bypass review.

### Q: How do you ensure AI-authored code meets your quality and security standards?

**Answer:**

> We have a multi-layer quality and security discipline that applies to all code, with specific additional layers for AI-authored work:
>
> 1. **Two-tier review.** Every PR is reviewed by an automated AI reviewer subagent AND by a human engineer. The AI reviewer is a floor; the human is the ceiling. AI-only review never approves a merge to production.
> 2. **Slop-signature detection.** Automated heuristics flag the seven most common AI failure patterns: tests mocking implementation, deleted edge cases, silent error swallowing, weakened validation, removed security checks, unnecessary new abstractions, diff bloat / pattern divergence.
> 3. **Specialized subagent review.** Security-sensitive paths (authentication, authorization, payment handling, data ingress/egress) are reviewed by a dedicated security-reviewer subagent in addition to standard review.
> 4. **Quality metrics.** We track six quality metrics monthly: code maturity score, features-to-bugs ratio, lead time, story points delivered, predictability, and AI-tool token usage. Quality decay signals trigger remediation.
> 5. **Post-incident learning.** Every incident with AI-related root cause has a structured postmortem categorizing the failure (context / constraint / verification / planning) with a specific harness change as the action item.

### Q: What's your incident rate for AI-authored vs. human-authored code?

**Answer (calibrate honestly):**

> We track defect rates by AI authorship classification. Current data:
>
> - Defects per merged PR by classification (last 90 days):
>   - `ai:none`: [rate]
>   - `ai:assisted`: [rate]
>   - `ai:authored`: [rate]
>
> [If your rates are similar:] The defect rates across classifications are within statistical noise of each other. We do not see meaningful quality difference attributable to AI authorship.
>
> [If your rates differ:] We see [N]% higher defect rate on `ai:authored` code than `ai:none`. This is consistent with industry data showing AI-using teams have wider distribution; we are actively investing in harness improvements to close the gap.

### Q: Who is liable for bugs in AI-authored code that affect your customers?

**Answer:**

> [Company] is fully liable for the code we ship, regardless of authorship. AI tools are a productivity input to our engineering process; they do not transfer liability. Our engineers review and approve all code before it ships; our incident response, customer communications, and remediation processes treat AI-authored bugs with the same gravity as human-authored bugs.
>
> Our customer SLAs and warranties apply to the code, not to the authorship method.

---

## Section C — Customer data handling in AI tools

### Q: Does customer data ever flow through AI tools?

**Answer:**

> [Calibrate to your actual practice. Common honest answers:]
>
> **Option A — No, never:**
>
> > No. Customer data is processed only in our production systems. Our development environments use synthetic / sanitized data for AI-tool-assisted development. We have technical controls (data classification matrix, automated DLP) to prevent customer data from flowing to AI tools.
>
> **Option B — Yes, in specific controlled flows:**
>
> > Customer data flows through specific AI-powered features within our product (e.g., [list features]). For these features:
> > - The AI vendor has contractual no-training commitments for our data
> > - Customer data is processed in [region] only
> > - Data flows are logged and auditable
> > - Customers can opt out of AI-powered features per their preferences
>
> > Customer data does NOT flow through AI tools used for code development. Development uses synthetic / sanitized data only.
>
> **Option C — Yes, in development for specific debugging:**
>
> > In limited specific circumstances (e.g., debugging a customer-reported issue), customer data may flow through AI tools. When this happens:
> > - It requires explicit authorization from the customer (per support ticket)
> > - It is logged
> > - The data is purged from any AI vendor logs within [N] days
> > - The flow is restricted to vendors with appropriate contractual protections

### Q: If a customer requests deletion of their data, does that delete from AI vendor systems?

**Answer:**

> Yes, but with timing nuance. Customer data deletion requests trigger:
>
> 1. Deletion from our active production systems within [N hours/days per your DPA].
> 2. Deletion from our backups per our standard backup retention cycle (typically 30-90 days).
> 3. For data that flowed through AI vendor systems: the data is not retained in vendor active systems past the request lifecycle (typically <60 seconds). Vendor logs containing customer data references are deleted per the vendor's retention policy ([typically 30-90 days]).
>
> Note: AI models trained on customer data could not be "un-trained." Per our contractual no-training commitments with vendors, your data is not used in model training, so this scenario should not arise. We document this in our data deletion attestations.

---

## Section D — Vendor management

### Q: How do you select AI vendors?

**Answer:**

> Our AI vendor selection process includes:
>
> 1. **Security review** — structured review covering data handling, model isolation, audit, compliance certifications, vendor health.
> 2. **Data classification mapping** — which data classes the vendor is approved for.
> 3. **Contract negotiation** — explicit terms for training opt-out, data retention, breach notification, exit.
> 4. **Procurement gate** — 21-item checklist before signing.
> 5. **Annual renewal review** — re-verify all of the above; vendors change terms.
>
> Documentation available under NDA on request.

### Q: What happens if your AI vendor experiences a security incident?

**Answer:**

> Our AI vendor contracts include 72-hour breach notification SLAs. On notification:
>
> 1. We assess scope: which data, which customers, which time window.
> 2. We notify affected customers per our standard breach notification policy.
> 3. We work with the vendor on root cause and remediation.
> 4. We assess whether to continue with the vendor or migrate.
> 5. Postmortem and lessons-learned process applies.
>
> If your contract with us requires specific notification windows or processes for vendor incidents affecting your data, we will honor those.

### Q: How do you handle the discovery that an AI vendor has breached their contract (e.g., trained on data they shouldn't have)?

**Answer:**

> Our contracts include audit rights and provide for material breach remedies, including termination without penalty. The specific response would depend on the breach:
>
> 1. **Investigation** — determine scope and impact
> 2. **Customer notification** — if your data was implicated, you would be notified per the contractual SLA
> 3. **Vendor accountability** — pursue contractual remedies
> 4. **Migration if needed** — if the vendor relationship cannot be continued, we have documented exit / migration plans
>
> We retain the right to terminate AI vendor contracts without penalty if material breach of contract terms occurs.

---

## Section E — AI feature governance (if you ship AI features in your product)

### Q: What AI capabilities does your product include?

**Answer (calibrate to your product):**

> Our product includes the following AI-powered features:
>
> | Feature | What it does | AI vendor | Customer-data flow |
> |---|---|---|---|
> | [Feature 1] | [description] | [vendor] | [Yes/No] |
> | [Feature 2] | [description] | [vendor] | [Yes/No] |
>
> All AI-powered features can be disabled at the tenant level by your administrator.

### Q: Can users disable AI features?

**Answer:**

> Yes, AI-powered features can be disabled at the tenant level. Some features have user-level toggles for individual control. Configuration is available in your administrator console.
>
> Note: disabling AI features may affect functionality. We document the impact of each disablement so administrators can make informed decisions.

### Q: Are users informed when they're interacting with AI?

**Answer:**

> Yes, in user-facing AI interactions where the response or action originates from an AI model, we provide visual indicators (icons, labels, "AI-generated" tags). The specific design language is documented in our product design guidelines.
>
> For AI-assisted features where AI augments rather than replaces human work (e.g., AI-assisted search ranking), the AI involvement is documented in the feature description but may not be flagged on every interaction.

---

## Section F — Audit and certification

### Q: Is your use of AI tools covered in your SOC 2 / ISO 27001 / etc.?

**Answer (calibrate honestly):**

> Our most recent SOC 2 Type II audit ([date]) included [an evaluation of / a description of / specific testing of] our AI tool governance, including:
>
> - The data classification matrix and approved tooling list
> - The PR authorship tagging convention
> - The two-tier review discipline
> - The vendor management process
>
> [If covered:] The auditors' findings on our AI governance are [included in the SOC 2 report / available on request under NDA].
>
> [If not yet covered:] Our next SOC 2 Type II audit ([planned date]) will include an explicit evaluation of AI tool governance. We are working with our auditors to ensure the audit scope captures it.

### Q: Have you been audited by a third party specifically for AI safety / governance?

**Answer:**

> [If yes:] Yes. [Auditor] conducted [type of review] in [date]. The report is available [under NDA / at our trust center].
>
> [If no:] We have not yet undergone a dedicated third-party AI governance audit. Our SOC 2 Type II audit covers some of the governance dimensions; we are evaluating dedicated AI audits for [planned year].

### Q: What internal audits do you conduct on AI tool usage?

**Answer:**

> Internal audits and reviews:
>
> - **Quarterly:** Approved tooling matrix review (vendor terms, certifications, our usage)
> - **Quarterly:** Data classification compliance audit (any unauthorized data flows)
> - **Monthly:** Token usage and cost review (anomaly detection)
> - **Per incident:** AI-related incident postmortem with structured categorization (Ch 39 framework)
> - **Annually:** Full AI governance review including policy currency, vendor assessments, and adoption metrics

---

## Common follow-up questions

### "Can we visit your office to review your AI governance practices?"

> "We support customer audits through our existing audit framework, which covers AI governance practices. Specifically:
>
> - Document review under NDA: yes, on request, with a 2-week notice
> - Live process walkthrough: yes, virtually, with our security team
> - On-site visit: case-by-case based on contract terms; please discuss with your account executive
>
> We're happy to facilitate the level of review your compliance program requires."

### "Will you share your CLAUDE.md / AGENTS.md / internal AI policy documents?"

> "We share governance posture documentation under NDA on request. Specific internal configuration files (CLAUDE.md, AGENTS.md, etc.) contain references to internal systems and conventions; we share representative excerpts but typically not the full files. Happy to discuss what would meet your audit needs."

### "What if we don't want our code processed by AI tools?"

> "We can accommodate. The accommodation depends on your specific data flows:
>
> - For your data that flows through our product's AI features: opt-out is available at the tenant level.
> - For our internal development practices (i.e., our engineers using AI tools to develop our product): if you require that our development team not use AI tools on code that processes your data, please discuss with your account executive. We can discuss specific arrangements; some customers have negotiated additional commitments here."

### "Can we get a discount because AI is making your engineering cheaper?"

> "AI tooling is one of many inputs to our engineering productivity. The savings (where they exist) are reinvested in product capability, security investment, and customer responsiveness. Our pricing reflects the value our product provides, not the specific cost structure of producing it."

---

## What to NOT include

Per Ch 52 §52.6's framing for skip-level conversations and per Ch 31 §31.6's PR-tagging discipline:

- **Don't quantify productivity.** Numbers in writing become commitments. "Our engineers are 30% more productive" is a marketing claim that becomes a contractual obligation.
- **Don't disclose specific token volumes or costs.** Customer-facing disclosure should be operational, not financial.
- **Don't list every model and version you use.** Vendor relationships change; lists go stale; calibrating disclosure to high-level capability is more durable.
- **Don't promise things you can't deliver.** "We guarantee no AI-authored bugs" is an unachievable promise. Stick to process commitments.
- **Don't speculate about competitors' practices.** "Unlike Vendor X, we don't..." invites a contest you don't want.

## Companion artifacts

- [`status-page-language.md`](status-page-language.md) — for incident-related disclosure
- [`ai-authorship-disclosure-tos.md`](ai-authorship-disclosure-tos.md) — contract-level language
- [`disclosure-decision-framework.md`](disclosure-decision-framework.md) — when to disclose what
- `executive-strategic-kit/security-questionnaire-answers.md` — abbreviated version
- Ch 31 §31.6, Ch 38, Ch 41 — sources
