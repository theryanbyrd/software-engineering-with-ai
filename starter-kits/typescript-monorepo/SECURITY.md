# Security Policy

## Reporting a vulnerability

Email security@<your-company>.com. Do not open a public issue. We aim to respond within 2 business days.

## AI tooling disclosure

This repository's engineering team uses AI-assisted development tools as part of standard practice. All AI-assisted code goes through the same review, testing, and security processes as human-written code.

### Tools in use

- Default coding assistant: Claude Code (Anthropic)
- Inline completion: GitHub Copilot Business
- (Update this section to match your team's actual approved tooling matrix)

### Vendor terms

All AI vendors used by this team operate under contracts that prohibit training on our code. Specifically:

- **Claude Code (Anthropic):** Enterprise terms with explicit no-training clause.
- **GitHub Copilot Business:** Training opt-out enabled per organization policy.

We review these terms quarterly.

### Customer data and AI

Customer-classified data is not sent to vendors that do not have a BAA / DPA / equivalent in place. Engineers are trained on the data classification policy and `.claude/hooks/protected-paths.sh` enforces additional restrictions on paths containing customer data.

### AI incident response

This repository's incident response procedures include AI-aware steps for: prompt injection, secret leakage through agent context, and AI-authored code defects in production. The full runbook is in `docs/runbooks/ai-incident-response.md`.
