# Security Policy

## Reporting a vulnerability

Email security@<your-company>.com. Do not open a public issue. We aim to respond
within 2 business days.

## AI tooling disclosure

This repository is worked on with AI-assisted development tools (Claude Code and
similar). All AI-assisted changes go through the same review, `verify`, and
security gates as human-written code. AI tooling is used under enterprise vendor
terms with explicit no-training clauses, reviewed quarterly.

## Data classification and AI tool access

Engineers must know the classification of any data before pointing a tool at it.
The matrix below maps each data class to what AI tooling may touch it. Customer
data and regulated data never leave vendors lacking a BAA / DPA, and
`.claude/hooks/legacy-protected-paths.sh` enforces additional path restrictions.

| Data class    | Examples                                  | AI tooling allowed                          |
|---------------|-------------------------------------------|---------------------------------------------|
| Public        | Open docs, marketing copy                 | Any approved tool                           |
| Internal      | Source code, internal runbooks            | Approved no-training tools only             |
| Confidential  | Secrets, keys, infra credentials          | None — never paste into any tool            |
| Customer/PII  | Customer records, PII, PHI                | None without BAA/DPA; prefer redaction      |
| Regulated     | Data under SOC 2 / HIPAA / PCI scope      | None outside the approved, contracted path  |

PII and PHI are treated as customer data. When in doubt, classify up.

## AI incident response

Security incidents involving AI-authored code follow `docs/incident-response.md`,
which adds provenance, scope-drift, and harness-gap questions to the standard RCA.
