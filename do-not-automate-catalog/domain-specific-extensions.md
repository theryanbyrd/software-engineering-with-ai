# Domain-Specific Extensions

Extensions to the do-not-automate catalog for specific industries. Per Ch 33 §33.4:

> Healthcare: anything generating clinical text, prescription metadata, or care instructions is Tier 1.
>
> Financial services: anything affecting positions, balances, statements, or regulatory reporting is Tier 1.
>
> Defense / public sector: anything in a CMMC/ITAR enclave runs only on approved infrastructure and never leaves it.

This file expands those domain extensions and adds a few common verticals.

## Healthcare

The canonical industry where AI failures have severe consequences. Beyond the standard Tier 1 list:

### Tier 1 additions for healthcare

1. **Clinical text generation** — discharge summaries, care notes, patient instructions, follow-up reminders
2. **Prescription metadata** — drug names, dosages, frequencies, contraindications
3. **Care instructions** — patient education content, post-procedure instructions
4. **Clinical decision support logic** — anything that influences clinical recommendations
5. **PHI redaction or de-identification** — Tier 1 across all industries; emphasized here

### Why these are Tier 1

A misgenerated discharge summary can produce incorrect medication counts. A wrong dosage in prescription metadata can harm a patient. Care instructions that contradict the actual care produce confusion at best, harm at worst.

The AI tooling discipline isn't "AI can't help with healthcare work." The discipline is: humans (clinicians or trained healthcare engineers) lead clinical content; AI assists with implementation, drafting, and review.

### Specific patterns

- **Use AI for drafting templates** that clinicians edit; never publish AI-generated clinical content directly
- **Use AI for testing the systems** that handle clinical content; never the content itself
- **Specific HIPAA-scope BAA** with the AI vendor before any patient data flows through (per `vendor-procurement-runbook/`)

### Engineering discipline in healthcare

- All clinical-content paths under CODEOWNERS requiring clinical reviewer + senior engineer
- PHI flow paths under hard MCP boundary; agent has read-only access to specifically scoped patient data, never write
- Security-reviewer subagent with healthcare-specific patterns
- Quarterly compliance review including AI tooling usage

## Financial services

Heavy regulatory exposure; specific data integrity requirements; strong audit trail requirements.

### Tier 1 additions for financial services

1. **Position calculations** — anything that affects what's owned, owed, or at risk
2. **Balance updates** — account balances, settlement balances, custodial balances
3. **Statement generation** — anything that goes to customers or regulators
4. **Regulatory reporting** — submissions to regulators (SEC, FINRA, etc.)
5. **Trading logic** — order routing, execution, hedging
6. **Reconciliation logic** — anything that determines what's settled vs. outstanding
7. **AML / KYC logic** — anything that affects customer onboarding decisions or transaction monitoring

### Why these are Tier 1

A bug in position calculation can mean a customer's reported balance is wrong. A bug in trading logic can produce financial loss to customers, the company, or counterparties. A bug in regulatory reporting can produce regulatory exposure.

### Specific patterns

- **Reconciliation discipline** — even AI-assisted changes go through reconciliation against authoritative sources
- **Audit trail** — every change to balance / position / settlement logic generates an audit entry
- **Specific compliance addendum** with AI vendor for financial-services-specific terms

### Engineering discipline in financial services

- All position / balance / settlement paths under strict CODEOWNERS
- Specific reviewer for trading logic (not just senior engineer; specific domain expertise)
- Explicit verification against authoritative sources before deployment
- Specific monitoring for financial-data drift post-deployment

## Defense / public sector

Heavily restricted by infrastructure and compliance requirements.

### Tier 1 considerations for defense / public sector

Beyond the work-pattern tier, infrastructure constraints apply:

1. **CMMC / ITAR enclave isolation** — work in scope of these regulations runs only on approved infrastructure and never leaves it
2. **Air-gapped systems** — AI tooling that requires external API calls cannot operate against air-gapped systems
3. **FedRAMP-authorized model only** — for FedRAMP work, the AI vendor must be FedRAMP-authorized (Moderate or High depending on scope)
4. **Background investigation requirements** — depending on the work, engineers AND AI vendors may need specific investigations / clearances
5. **Cleared personnel only** for specific work surfaces

### Why this matters

The infrastructure constraints are non-negotiable. An engineer using a non-FedRAMP-authorized AI tool on FedRAMP-scoped code is a compliance violation regardless of the actual technical risk.

### Specific patterns

- **On-prem or sovereign-cloud deployment** of AI tools when the work requires it
- **Network egress controls** preventing AI tools from reaching external endpoints when the work is enclave-scoped
- **Certifications appropriate to the work scope**

### Engineering discipline in defense / public sector

- Approved tooling matrix per `vendor-procurement-runbook/data-classification-walkthrough.md` extended for cleared work
- Hard MCP boundaries between cleared and uncleared work
- Specific certifications for engineers working on cleared codebases

## Other regulated industries

### Insurance

- Underwriting decisions and risk-rating logic — Tier 1
- Claim adjudication logic — Tier 1
- Policy generation that includes coverage terms — Tier 1
- Customer-facing premium calculations — Tier 1

### Pharmaceuticals (manufacturing, distribution)

- Batch records and tracking — Tier 1
- GxP-scoped systems — Tier 1
- Clinical trial data systems — Tier 1
- Regulatory submission systems — Tier 1

### Critical infrastructure (utilities, transportation, etc.)

- Control systems and SCADA-adjacent code — Tier 1
- Safety-critical logic — Tier 1
- Anything that affects physical operation — Tier 1

### Education (especially K-12 and special education)

- Student data systems with FERPA scope — Tier 1
- Special education accommodations and IEP systems — Tier 1
- Student grading and assessment systems — Tier 1

### Legal (law firms, legal-tech)

- Document drafting where the document is what gets filed — Tier 1
- Privilege review and redaction — Tier 1
- Conflict-of-interest checking — Tier 1

## How to add domain-specific extensions

If your industry isn't represented above:

1. **Identify the failure modes specific to your domain.** What can go wrong that wouldn't go wrong in a generic SaaS company?
2. **Map failure modes to work categories.** What code, when it has bugs, produces these failure modes?
3. **Add work categories to Tier 1, 2, or 3 based on severity and reversibility.**
4. **Document the reasoning.** Engineers will push back; the reasoning is the durable artifact.
5. **Bring to catalog governance review** (per [`catalog-governance.md`](catalog-governance.md)) for formal addition.

## What domain extensions don't do

### They don't replace the base catalog

The base Tier 1/2/3 still applies. Domain extensions add to it; they don't override.

### They don't substitute for compliance expertise

The catalog is the engineering discipline. Specific compliance requirements (HIPAA's specific requirements, PCI-DSS's specific requirements) need compliance-specific expertise. The catalog is necessary but not sufficient.

### They don't grandfather existing systems

If your codebase has legacy systems that weren't built with the catalog discipline, the catalog applies going forward. Existing systems may need migration (per `legacy-codebase-onboarding/`); the catalog protects what gets built next.

### They don't protect against vendor terms

If your AI tool vendor's terms aren't compatible with your domain's compliance (e.g., no BAA for HIPAA), the catalog can't fix that. Per `vendor-procurement-runbook/security-review-template.md`, vendor terms need review before adoption.

## Companion artifacts

- [`tier-1-never-autonomous.md`](tier-1-never-autonomous.md) — base catalog
- [`tier-2-mandatory-human-gate.md`](tier-2-mandatory-human-gate.md) — base catalog
- [`tier-3-light-human-gate.md`](tier-3-light-human-gate.md) — base catalog
- [`catalog-governance.md`](catalog-governance.md) — how to maintain extensions
- `vendor-procurement-runbook/data-classification-walkthrough.md` — adjacent
- `customer-facing-ai-disclosure/` — adjacent (the customer-facing version of these protections)
- Ch 33 §33.4, Ch 34 — sources
