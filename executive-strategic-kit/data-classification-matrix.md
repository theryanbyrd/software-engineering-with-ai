# Data Classification × AI Tool Permissions Matrix

Companion to *Software Engineering with AI* by Ryan Byrd · Ch 34

**Owner:** VP Engineering · **Co-signed:** CISO · **Last reviewed:** _[DATE — UPDATE]_

Markdown source (replaces `data-classification-matrix.xlsx`). Both engineers and agents read this file; keeping it in a spreadsheet hid it from the agents that need to enforce the rules.

## Matrix

Legend: ✓ Allowed · ⚠ With caution / review · ✗ Blocked

| Classification | Examples | Default LLM (Sonnet/Haiku) | Frontier model (Opus) | Local LLM only | Cursor/IDE inline | Notes |
|---|---|---|---|---|---|---|
| **Public** | Marketing copy, public docs, open-source code | ✓ Allowed | ✓ Allowed | ✓ Allowed | ✓ Allowed | No restriction. AI can read and write freely. |
| **Internal** | Internal docs, build configs, non-production code | ✓ Allowed | ✓ Allowed | ✓ Allowed | ✓ Allowed | Standard development. Default for most code. |
| **Confidential** | Pre-release roadmap, financial projections, salary data | ✓ With BAA | ✓ With BAA | ✓ Allowed | ⚠ With caution | Vendor must have BAA/DPA. No personal accounts. |
| **Customer data (general)** | Customer-uploaded content, support tickets, account metadata | ✓ With BAA + DPA | ⚠ Requires review | ✓ Allowed | ✗ Blocked | Pre-commit hooks block known patterns. Document any approved exception. |
| **Customer PII** | Names, emails, addresses, payment info | ✗ Blocked | ✗ Blocked | ✓ Allowed (vetted) | ✗ Blocked | Never sent to vendors. Egress controls enforce. |
| **PHI (HIPAA)** | Protected health information | ✗ Blocked | ✗ Blocked | ✓ Allowed (vetted) | ✗ Blocked | BAA required for any system that touches PHI. Most AI tools cannot. |
| **Regulated (PCI/SOX/etc.)** | Card data, regulated financial records | ✗ Blocked | ✗ Blocked | ✓ Allowed (vetted) | ✗ Blocked | Compliance-scoped systems only. Specific approvals required. |
| **Production credentials** | API keys, passwords, signing keys, prod env vars | ✗ Blocked | ✗ Blocked | ✗ Blocked | ✗ Blocked | Never. Hooks enforce. No exceptions. |

## How to use this matrix

| Use | What to do |
|---|---|
| Engineering training | All engineers must read this matrix as part of onboarding. Re-read annually. |
| Technical enforcement | Hooks in `.claude/hooks/protected-paths.sh` enforce file-level restrictions. Cost gateway logs all calls with classification metadata. |
| Customer questions | When a customer asks "what data do you send to AI vendors," this matrix is the answer. Sharable under NDA. |
| Updates | Update on every new vendor, new contract term, new data class added to the business. CISO signs off on changes. |
| Default behavior | When in doubt, classify higher. The cost of over-restricting is small. The cost of under-restricting can be career-ending. |
