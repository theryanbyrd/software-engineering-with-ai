# AI Authorship Disclosure — ToS and Contract Language

Sample contract and ToS language for AI authorship disclosure. Direct implementation of Ch 31 §31.6 and Ch 41.

> **Critical:** Every word of the language below requires legal review before use. This document is a starting point for the legal-counsel conversation, not a finished product. The phrasing, the specific commitments, and the carve-outs are jurisdiction-specific and company-specific.

The templates here lean toward openness about AI usage. The reasoning, restated from the README: openness is the durable position; commitments to non-disclosure are hard to undo when public discourse and competitor disclosure shift.

## Where AI authorship disclosure shows up in customer-facing legal documents

Five typical surfaces:

1. **Master Service Agreement (MSA) / Order Form** — the contract you signed with a specific customer
2. **Data Processing Addendum (DPA)** — the data-handling terms layered onto the MSA
3. **Terms of Service (ToS)** — public-facing terms applying to all users
4. **Privacy Policy** — what you do with user data
5. **Acceptable Use Policy (AUP)** — what users can and can't do with your service

The AI authorship disclosure usually goes into the ToS and the DPA, with cross-references in the MSA and Privacy Policy as needed.

## Template language by document

### ToS — AI tooling usage in product development

A high-level disclosure suitable for public ToS:

> **Use of AI Tooling in Service Development**
>
> [Company] develops and maintains the Service using a combination of human engineering work and AI-assisted development tools. Our use of AI tools is governed by an internal policy that includes data classification, vendor security review, and review processes for AI-generated code prior to deployment.
>
> AI-assisted development is a normal part of modern software engineering and does not change the security, reliability, or performance commitments we make in this Agreement. Our standard quality, review, and testing processes apply to all code regardless of authorship.
>
> Customers with specific questions about our development practices may request additional information through the procedures in Section [X].

### ToS — AI features within the product

Distinct from development practices: this is for products that include AI capabilities the customer uses directly.

> **AI-Powered Features**
>
> Certain features of the Service use AI/ML technologies. Where such features are used:
>
> 1. **Inputs and outputs.** Inputs you provide to AI-powered features and the outputs generated may be processed by AI providers under contract with [Company]. Specific providers are listed in our [Subprocessors page / DPA].
> 2. **Training prohibitions.** Our contracts with AI providers prohibit them from training their models on customer inputs or outputs except where you have explicitly opted in.
> 3. **Accuracy.** AI-generated outputs may contain errors. The Service is not designed for use cases where AI errors would cause significant harm without independent verification by you.
> 4. **Opt-out.** You may opt out of AI-powered features at the tenant level via [feature flag / settings page]. Some Service capabilities may be limited if AI features are disabled.

### DPA — Subprocessor disclosure

The DPA already lists subprocessors. Add AI tooling vendors explicitly:

> **AI Tooling Subprocessors**
>
> The following AI tooling vendors are subprocessors used by [Company] in connection with the Service:
>
> | Subprocessor | Purpose | Customer Data Processed |
> |---|---|---|
> | [Vendor 1, e.g., Anthropic] | AI-assisted code development tools used by [Company] engineering | None directly; engineers may incorporate AI suggestions into code that processes customer data only after review |
> | [Vendor 2, e.g., OpenAI] | AI-powered Service features (where applicable) | Customer inputs to AI-powered features, processed under contractual no-training and data-handling terms |
> | [Vendor N] | [Purpose] | [Scope] |
>
> Material changes to AI tooling subprocessors will be communicated per the subprocessor change procedures in Section [X].

### DPA — AI development practices commitment

For customers who require explicit commitments:

> **AI-Assisted Code Development Practices**
>
> [Company] commits that:
>
> 1. **Approved tooling only.** AI development tools used on code that processes Customer Data are limited to tools that have completed [Company]'s vendor security review and are listed on [Company]'s approved tooling matrix.
> 2. **No customer data in training.** [Company] will not knowingly send Customer Data to AI tooling vendors in a manner that permits training on such data. AI tools used by [Company] engineering operate on application code and engineering artifacts, not on Customer Data, except where explicitly authorized.
> 3. **Review process.** All code, regardless of whether AI-assisted in authorship, is subject to [Company]'s standard code review, testing, and deployment processes prior to operating on Customer Data.
> 4. **Material changes.** Material changes to [Company]'s AI tooling practices that affect Customer Data handling will be communicated [N] days in advance.

### Privacy Policy — AI features (when applicable)

> **AI/ML Processing**
>
> When you use AI-powered features of our Service, your inputs and the outputs generated may be processed by [Company]'s AI providers as described in our [Subprocessors page / DPA]. We have contractual commitments with these providers that prohibit them from using your inputs or outputs to train their models, except where you have explicitly opted in.
>
> AI-powered features may produce outputs that are inaccurate. We do not guarantee the accuracy of AI-generated content and recommend you verify outputs before relying on them in important decisions. You may opt out of AI-powered features at any time through your account settings.

## Negotiated additions for enterprise customers

Some enterprise customers will request specific commitments beyond the standard ToS/DPA. The most common requests, and our recommended posture:

### Request: "Don't use AI tools at all on our code"

**Posture:** Decline as a general rule; consider in specific high-sensitivity cases.

> "We use AI development tools as part of our standard process across all customers. We do not maintain a separate development pipeline that excludes AI tools. We can discuss specific data-handling commitments — for example, the prohibitions on training on Customer Data, the approved tooling matrix, the review processes — but we cannot operate a separate AI-free engineering pipeline for individual customers."

In rare cases (specific regulated environments, pre-IPO sensitivity, M&A-adjacent confidentiality) you may consider a carve-out. Be cautious; the operational complexity is significant.

### Request: "Tell us specifically when AI tooling was involved in code that affects us"

**Posture:** Generally decline as a per-incident commitment; offer in aggregate.

> "Our internal records track which code is AI-assisted in authorship; we do not provide per-incident or per-feature attribution to customers. We do publish post-incident reviews that disclose AI authorship where relevant. We can discuss aggregate metrics — for example, the percentage of changes that involve AI assistance — under NDA."

The reason: per-feature attribution is operationally infeasible at scale and creates customer-side expectations you can't reliably meet. Aggregate metrics are honest and stable.

### Request: "Provide us with the audit trail of AI tooling usage on our code"

**Posture:** Decline; this is internal data.

> "Our internal records on AI tooling usage are operational and not customer-facing. We can describe the governance discipline in writing, including the data classification matrix, the approved tooling list, and the review processes. The audit trail itself is internal and is reviewed by our compliance team and external auditors as part of our SOC 2 Type II audit."

### Request: "Notify us within [N] hours of any incident involving AI-authored code"

**Posture:** Decline as a separate commitment; align with existing breach/incident notification commitments.

> "Our incident notification commitments under Section [X] of the DPA apply to all incidents regardless of code authorship. We do not maintain a separate notification track for AI-authored code, because the framing introduces a false distinction — code is reviewed and tested regardless of authorship. If an incident affecting your data occurs, you are notified per our standard incident notification commitments."

### Request: "Indemnify us for any harm caused by AI-authored code"

**Posture:** Decline; existing indemnification covers all code.

> "Our indemnification under Section [X] covers all code we author and ship, regardless of whether AI tools were used in the authoring. We do not maintain a separate indemnification regime for AI-assisted code because the standard indemnification already covers it."

## What NOT to put in the contract

- **Specific tool names.** "We use Claude Code" in the ToS or DPA creates a binding commitment; if you switch vendors, you've broken the contract. Use category language: "AI development tools."
- **Productivity claims.** "Our engineering is N% more productive due to AI tooling" is a marketing claim; it has no place in a contract.
- **Specific token volumes or costs.** Operational data; not contractual.
- **Promises about specific AI capabilities.** "Our AI-powered features will achieve X accuracy" is dangerous; AI accuracy varies and contractual accuracy commitments are very hard to meet.
- **Definitions of "AI" or "AI-authored" that may not hold up over time.** The category is moving fast; contract definitions should be functional, not technical.
- **References to specific vendor's policies.** "Per Anthropic's terms..." pins you to a specific vendor's terms which may change.

## What to track internally for this language to be defensible

If you're committing to language like "AI tools used by us are approved per our internal policy," the language is defensible only if the internal policy actually exists and is followed. Specifically:

- The approved tooling matrix exists and is current
- The data classification policy exists and is communicated
- The internal review process for AI-assisted code is real (not just on paper)
- The audit trail exists and is reviewable
- The customer-facing language matches what you actually do

Auditors, regulators, and litigation will eventually probe this. The contract language must align with reality.

## Companion artifacts

- [`security-questionnaire-answers.md`](security-questionnaire-answers.md) — for the questionnaire-side of disclosure
- [`status-page-language.md`](status-page-language.md) — for incident-related disclosure
- [`disclosure-decision-framework.md`](disclosure-decision-framework.md) — when to disclose what
- [`customer-conversation-scripts.md`](customer-conversation-scripts.md) — for the live conversation
- `vendor-procurement-runbook/contract-terms-negotiation-script.md` — the vendor-side counterpart
- `exec-kit/data-classification-matrix.xlsx` — the internal data classification this contract language references
- Ch 31 §31.6, Ch 41 — sources

## Reminder

Every word of this template requires legal review before use. The structure and the postures are calibrated; the specific phrasing for your jurisdiction, your customer, your industry is what your counsel determines.
