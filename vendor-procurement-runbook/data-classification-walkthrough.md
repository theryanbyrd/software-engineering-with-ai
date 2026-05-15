# Data Classification Walkthrough

How to use the data classification matrix to determine which AI tools are approved for which data classes. The bridge between Chapter 38's procurement framework and Chapter 41's data-classification framework.

## The four data classes

Most companies use a four-tier classification. Adapt the names to your company's existing taxonomy if different:

| Class | Description | Examples |
|---|---|---|
| **C1 — Public** | Already public; no harm if exposed | Marketing copy, public docs, OSS code |
| **C2 — Internal** | Not for public; routine business | Engineering docs, code that isn't trade-secret-class, internal Slack messages |
| **C3 — Confidential** | Limited access; significant harm if exposed | Customer lists, financial data, sensitive engineering work, security architecture |
| **C4 — Restricted** | Highest sensitivity; severe harm if exposed | Customer PII, payment data, credentials, regulated data (PHI, etc.), pre-disclosure security work |

If your company uses different class labels (e.g., Confidential / Restricted / Top Secret in defense; Public / Internal / Restricted in finance), map to your taxonomy. The tier count matters less than the consistency.

## What each AI tool can be approved for

Based on the security review (see [`security-review-template.md`](security-review-template.md)), classify each AI tool by the maximum data class it's approved for:

| Tool | Max approved class | Why |
|---|---|---|
| (Tool A) | C2 | Standard SOC 2; no BAA available; no FedRAMP |
| (Tool B) | C3 | SOC 2 + ISO 27001; configurable inference region; tenant-level training opt-out |
| (Tool C) | C4 | C3 capabilities + BAA + FedRAMP Moderate + verified training opt-out + EU data residency |
| (Tool D — sovereign / on-prem) | C4 incl. ITAR / CMMC | All controls + on-prem deployment + air-gapped option |

## How to apply this in practice

### Engineer asks: "Can I use Tool X on Project Y?"

The answer depends on the data Project Y handles, not on the engineer's preference:

1. **What's the highest data class Project Y handles?** (Look at the project's data inventory; if there isn't one, that's the first finding.)
2. **What's the max approved class for Tool X?**
3. **If Tool X's max ≥ Project Y's max:** approved. Engineer can use Tool X on Project Y.
4. **If Tool X's max < Project Y's max:** not approved. Either engineer uses a higher-classified tool, or the project's data flow is restructured to reduce the data class crossing the tool boundary.

### Common scenarios

**"I want to use Cursor on our payment processing code."**
- Payment processing code touches C4 data (payment tokens, customer PII)
- Cursor's max approved class is C3 (no BAA, no FedRAMP — verify your contract)
- **Answer:** Not approved. Use the C4-approved tool instead.

**"I want to use Claude Code for this internal tooling project."**
- Internal tooling that doesn't handle customer data: C2
- Claude Code (Enterprise tier) approved through C3 minimum
- **Answer:** Approved.

**"Can I send a customer support transcript to Claude.ai for summarization?"**
- Support transcript may contain customer PII: C4
- Personal-account Claude.ai is not approved for any company data (it's a shadow AI use case)
- **Answer:** Not approved. Use the company-procured Claude.ai (or equivalent) on the appropriate tier.

**"Can I run our own benchmark suite through GPT-5 via OpenAI's API?"**
- Benchmark suite contains code samples from your codebase: C2 or C3 depending on what's in them
- OpenAI's API at the Enterprise tier may be C3-approved
- **Answer:** Depends on tier. Verify the OpenAI Enterprise contract's training opt-out and data retention. Check the benchmark suite for any C4 content.

## Building the matrix

A spreadsheet with rows = data classes, columns = approved tools, cells = approved/conditional/denied.

```
                    Claude Code   Cursor       Copilot      ChatGPT
                    Enterprise    Business     Business     Enterprise
C1 - Public         ✓             ✓            ✓            ✓
C2 - Internal       ✓             ✓            ✓            ✓
C3 - Confidential   ✓             ✓ (BYOK)     ✓            ⚠ (verify training opt-out)
C4 - Restricted     ✓ (BAA)       ✗            ✗            ✗
C4 + ITAR/CMMC      ⚠ (Bedrock    ✗            ✗            ✗
                    GovCloud)
```

`✓` = approved
`⚠` = conditional / requires verification
`✗` = not approved
`(BAA)` / `(BYOK)` = additional condition

A more comprehensive template is in `executive-strategic-kit/approved-tooling-matrix-template.xlsx`.

## When the matrix needs updating

The matrix is a living document. Update when:

- **A new vendor is approved.** Add the column.
- **An existing vendor's terms change.** Vendors update terms regularly; the matrix entry may move up or down.
- **Your data classification updates.** If a new class is introduced (e.g., adding "Highly Restricted" for pre-IPO financial data), every tool needs a new cell.
- **A new use case surfaces a gap.** "We need to use AI on this PHI workflow" surfaces that no current tool is approved for that combination.
- **Quarterly review** (recommended). Even without prompt, audit the matrix against vendor changes.

## What to do when the matrix denies a use case

A common situation: the engineer needs a capability for a data class no current tool is approved for.

The bad path: the engineer routes around the matrix. (This becomes shadow AI; see [`migration-playbooks/shadow-ai-to-approved-stack.md`](../migration-playbooks/shadow-ai-to-approved-stack.md).)

The good path:

1. **Restructure the data flow.** Can the work be done with a less-classified data subset? Often the engineer needs Tool X for analysis but only on synthetic data; production data isn't actually required.
2. **Procure a new tool.** Run the security review on a tool that does support the use case. May take 4-8 weeks.
3. **Build the capability internally.** For some sovereignty-bound work, the right answer is on-prem inference.
4. **Decline the use case.** Some work shouldn't be done with AI tooling at the current state of the market. Document why; revisit when the market changes.

## Anti-patterns

### "We trust this vendor; let's approve them for all classes"

Trust is necessary but not sufficient. The data class approval is about specific contractual and technical controls (BAA, FedRAMP, region, training opt-out). A vendor you trust generally may still lack the specific control for a specific data class.

### "Our engineers are smart; they'll know what data is sensitive"

The matrix exists because individual judgment under deadline pressure produces shadow AI. The matrix is the durable mechanism.

### "Personal-account Claude.ai for non-sensitive code is fine"

Personal accounts have no contractual relationship with your company. The vendor's terms with the personal account holder don't bind for your company's data. Personal accounts are never approved for company work, regardless of data class.

### "We can't classify everything; let's just pick one tool for everything"

The right "one tool for everything" is the highest-class-approved tool. Most companies' highest-class-approved tool is more expensive than they want for low-class work. The matrix exists to right-size cost.

## Companion artifacts

- [`security-review-template.md`](security-review-template.md) — produces the input for the matrix
- [`contract-terms-negotiation-script.md`](contract-terms-negotiation-script.md) — what to negotiate to move a vendor up a class
- `executive-strategic-kit/data-classification-matrix.xlsx` — template
- `executive-strategic-kit/approved-tooling-matrix-template.xlsx` — template
- Ch 41 — adjacent compliance context
