# Canonical Security Questionnaire Answers

**Use when:** A customer's security or procurement team sends a questionnaire that includes AI-related questions. From mid-2025 onward, this is roughly half of all enterprise security questionnaires.

**Why this exists:** Sales and CS will ping you ad-hoc with these questions. Without canonical answers, you end up writing the same answer four different ways across four customer engagements, and the answers slowly drift in inconsistent directions. This document is the single source of truth.

**Owner:** VP of Engineering, with CISO co-sign.

**Review cadence:** Quarterly, or whenever vendor terms materially change.

**Last reviewed:** [DATE — update on every change]

---

## Q1: Do you use AI in code generation?

> Yes. Our engineering team uses AI-assisted development tools as part of standard practice. All AI-assisted code goes through the same review, testing, and security processes as human-written code. AI tool usage is governed by an internal approved-tooling matrix maintained by Engineering and counter-signed by our CISO. The matrix is updated quarterly and is available for review under NDA.

## Q2: Which AI models or tools do you use?

> Our default coding assistant is **[Claude Code, Anthropic]**. For inline IDE completions we use **[GitHub Copilot Business / Cursor / your choice]**. For agentic workflows on internal tooling we use **[Claude Code]**. We do not use unapproved AI tools on customer-touching code; this is enforced through both policy and tooling controls (a cost gateway that logs all AI calls, and pre-commit hooks that block exfiltration of customer-classified data to unapproved endpoints).

> A full list of approved tools, with version constraints and approved use cases, is available under NDA.

## Q3: Do AI vendors train on your code?

> No. All vendors on our approved list operate under contracts that explicitly prohibit training on our code or our customers' data. Specifically:

> - **Anthropic (Claude Code, Claude API):** Enterprise contract with explicit no-training clause for inputs and outputs. Anthropic's published policy aligns with our contract terms.
> - **GitHub (Copilot Business / Enterprise):** Organization-level training opt-out is enabled. Copilot Business specifically excludes customer code from training data per GitHub's published terms.
> - **[Other vendors]:** [list with relevant terms]

> We review these terms quarterly and re-confirm them whenever a vendor announces material changes (we maintain a vendor-changes log internally).

## Q4: Where is AI-processed code stored, and where is inference run?

> Inference for our default coding assistant runs in [Anthropic's US-region infrastructure / AWS Bedrock in us-east-1 / specify your actual deployment]. For customers who require specific data residency, our Enterprise contracts with these vendors support inference in:

> - US (default)
> - EU (available via [vendor's EU region])
> - UK (available via [vendor's UK region])
> - Other regions: [list as supported by your vendors]

> For regulated workloads (PHI, customer-classified data), we route through [enclave / AWS PrivateLink / your specific compliance configuration]. Code is not retained by AI vendors beyond the duration required for inference; vendor logs are retained per the vendors' standard policies, which we have reviewed and accepted.

## Q5: What happens to code that includes our data?

> Customer data, including code that processes customer data, is handled per our published data classification policy. Customer-classified data is not sent to AI vendors that do not have a BAA / DPA / equivalent contractual protection in place. This is enforced both by training (engineers are trained on the policy) and by tooling (pre-commit hooks and the AI gateway block known patterns of customer data being sent to unapproved endpoints).

> If a specific class of your data has additional handling requirements (e.g., HIPAA-regulated, PCI scope, GDPR data subject restrictions), we accommodate those requirements in our standard processing agreement; please reference the relevant clauses in your DPA.

## Q6: Do you have an AI incident response plan?

> Yes. Our incident response plan includes specific procedures for AI-caused issues, covering:

> - **Prompt injection:** detection, containment, eradication procedures.
> - **Secret leakage through AI tooling:** automated detection on egress; manual review of context windows in postmortems.
> - **AI-authored code defects in production:** standard incident response, with the addition of an "AI authorship" review during postmortem to update prompts, skills, or guards.

> We can share the executive summary of our IR plan under NDA. We test these procedures via tabletop exercises at least annually.

## Q7: Has any AI-related incident affected customer data?

> [Honest answer required.]

> **If no:** "We have had no AI-related incidents that affected customer data. We track all incidents in our internal system; this can be confirmed via our SOC 2 Type II report."

> **If yes:** "Yes, on [DATE] we had an incident in which [brief description without unnecessary detail]. Customer data affected: [scope]. Notification was made to affected customers within [time]. Remediation: [what was done]. The incident report is available under NDA. The procedural changes implemented as a result are: [list]."

> Do not understate or downplay. The customer's CISO will discover the truth eventually; honest disclosure builds trust and is usually contractually required anyway.

## Q8: How do you handle AI-generated code in your SDLC?

> AI-assisted code is treated identically to human-authored code from a process perspective: it goes through the same code review, the same automated tests, the same security scanning, the same staged deployment, and the same incident response.

> We additionally tag PRs by AI authorship category (none / assisted / authored / agent-generated) for our internal metrics. This allows us to monitor quality and security indicators broken down by AI involvement, and to detect any drift over time.

## Q9: What controls prevent AI from accessing production systems?

> AI tooling does not have direct access to production systems. Specifically:

> - **No production credentials in AI agent context.** Hooks block environment variables and credential files from being included in agent runs.
> - **No production write access from agents.** Agents operate at autonomy level L0-L2 (read-only or single-file edits with review) on production-adjacent code; L3+ requires human approval per change.
> - **Network egress controls.** AI agents run in environments where egress is restricted to approved AI vendor endpoints and internal tooling.
> - **Audit logging.** All AI tool invocations are logged with developer, repo, and content classification.

## Q10: Do you have a Bill of Materials for AI components?

> [If yes:] We maintain an AI Bill of Materials (AIBOM) tracking models, versions, vendors, and contractual terms. Available under NDA.

> [If no:] We are working toward a formal AIBOM in [timeline]. Currently we maintain an Approved Tooling Matrix that lists all AI tools, vendors, contract terms, and approved use cases.

---

## Customization checklist

Before sharing with a customer:

- [ ] Replace `[DATE]` with actual review date
- [ ] Replace `[Claude Code, Anthropic]` etc. with your actual approved tools
- [ ] Replace `[Anthropic's US-region infrastructure / AWS Bedrock in us-east-1]` with actual deployment
- [ ] Confirm no-training clauses match the vendor terms you actually have signed
- [ ] Update Q7 honestly based on your actual incident history
- [ ] Confirm Q10 matches whatever AIBOM status you're actually at
- [ ] Have your CISO read the final version

## What to do when the customer asks for more detail

These answers are designed to be sharable as-is to a security review. When the customer asks for more detail:

1. **Offer an NDA conversation.** "Happy to walk through specifics under NDA on a 30-min call."
2. **Bring your CISO.** Most customer CISOs prefer to talk to your CISO. Make that easy.
3. **Share the actual policy documents under NDA.** Your data classification matrix, IR runbook, vendor terms summary.

## What NOT to do

- Don't say "we don't use AI." This is rarely true and the customer's CISO knows it.
- Don't refuse to discuss specifics. Refusal signals you're hiding something.
- Don't promise capabilities you don't have ("we have a complete AIBOM!" when you don't).
- Don't list every vendor in writing if some of those contracts have NDA terms.

## Related artifacts

- `../approved-tooling-matrix-template.xlsx` — internal version with full vendor terms
- `../data-classification-matrix.xlsx` — what data goes where
- `../vendor-negotiation-scripts.md` — for getting better terms next renewal
