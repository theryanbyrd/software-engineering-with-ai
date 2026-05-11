# T1-add-logging-to-handler

**Tier:** T1
**Estimated time for senior engineer:** 10-15 minutes
**Surfaces tested:** observability conventions, structured logging, no-PII discipline

## Adaptation guide

Pick a handler in your codebase. Confirm your team has documented logging conventions in CLAUDE.md or `docs/observability.md`. The task tests whether the agent matches your conventions rather than inventing new ones.

For teams using OTel, use OTel terminology in the rubric. For teams using structured JSON logging, use that. Match your stack.

## Setup

- A handler exists with no logging (or only a print statement)
- Team's logging conventions are documented
- The handler processes data that includes PII (an email or user ID)

## The task (give to the agent verbatim)

> Add structured logging to the `process_subscription_change` handler in `services/billing/subscription.py`. The handler should log: receipt of the request, success or failure of each stage, and the final outcome. Follow the team's existing logging conventions. Do not log PII.

## Pass criterion

Logs are emitted at start, success/failure of stages, and final outcome. No PII appears in logs. Conventions match existing handlers.

## Rubric — score 1 point each (max 8)

- [ ] Agent first read another handler in the same module to find existing logging conventions
- [ ] Logging library matches the codebase (no `print`, no `console.log` if the team uses a logger)
- [ ] Log format matches existing structure (JSON fields, key naming, level conventions)
- [ ] Log statements include a request/correlation ID where the codebase has one
- [ ] At least three log points: entry, mid-flow stage, exit
- [ ] No PII (email, full name, user-supplied free text) in log output
- [ ] User ID is logged as the team's convention dictates (often hashed or in a specific field)
- [ ] No new logger imports or configuration changes; uses the existing setup

## Common failure modes (informational)

- **Adds a new logger config.** Common with younger codebases. The agent should use what's there.
- **Logs the full request object.** Often contains email, payment token, etc. The PII rule check should catch this.
- **Inconsistent log levels.** Mixes DEBUG / INFO / WARN without clear pattern. Penalize if the codebase has a clear pattern the agent didn't follow.
