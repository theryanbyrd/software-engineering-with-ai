# Tier 1 — Never Autonomous, Always Human-Led

The Tier 1 catalog. Per Ch 33 §33.1:

> Tier 1 (never autonomous, always human-led)

These are the work categories where automation is forbidden — not because the agent CAN'T do them but because the failure modes are severe enough that human leadership is non-negotiable. This is the catalog's core: the items here should appear in your team's CLAUDE.md / AGENTS.md as explicit "never do" entries.

## The Tier 1 list (verbatim from Ch 33)

1. **Authentication and session code.**
2. **Authorization and RBAC code.**
3. **Billing, payments, refund, dunning.**
4. **Cryptographic key generation, rotation, escrow.**
5. **PII redaction or anonymization logic.**
6. **Data deletion, retention, GDPR-right-to-be-forgotten flows.**
7. **Production database schema migrations.**
8. **Production data backfills affecting more than a defined row threshold.**
9. **Anything that touches the customer of record without a transaction log.**

This list is the floor. Add to it; don't subtract.

## Why each item is here

### Authentication and session code

**Why:** account takeover. Subtle bugs in auth code (timing attacks, missing validation, session fixation) cascade into security incidents that affect every user. Per Ch 32 §32.2, auth changes are an L5-adjacent capability.

**The failure mode:** an AI-authored change to `validate_session()` removes a check that's been there for 5 years. Tests pass (no test exercised that path). Two weeks later, the customer support team gets reports of users seeing other users' accounts.

**How human-led works:** the human writes the code; the agent assists with reading, suggesting, and reviewing. Even at L0/L1 autonomy in `agent-autonomy-levels/`, every line is reviewed by a human and a security-reviewer subagent.

### Authorization and RBAC code

**Why:** privilege escalation. The most common security incidents in B2B SaaS are authz bugs — a tenant accessing data of another tenant; an unauthenticated path that should require auth.

**The failure mode:** an AI-authored permission check change passes tests; in production, a specific edge case (e.g., a paused subscription) bypasses the check. Customer's competitor sees their data.

**How human-led works:** authz changes go through a security-reviewer subagent in addition to human review. Per `agent-autonomy-levels/forbidden-categories.md`, authz code can't be at auto-merge regardless of tier.

### Billing, payments, refund, dunning

**Why:** financial harm. Bugs cost real money — undercharging customers; double-charging customers; refunds going to the wrong account.

**The failure mode:** an AI-authored refactor of the refund logic changes the order in which idempotency keys are generated. Some refunds get processed twice; some don't get processed at all. Customer support fields complaints; finance reconciles for weeks.

**How human-led works:** billing engineers write the code with senior peer review. AI assists with reading, test generation, edge-case enumeration. The deployed code is human-authored.

### Cryptographic key generation, rotation, escrow

**Why:** keys are the foundation of trust. A bug in key handling breaks everything that depends on the key — and reverting is often not possible (the wrong key was already used to sign data).

**The failure mode:** an AI-authored "improvement" to the key rotation logic introduces a subtle race condition. New keys are generated correctly but the old key is sometimes deleted before all systems have rotated. Some users can't authenticate; recovery requires manual intervention.

**How human-led works:** key handling is written by engineers with cryptographic experience. Code review includes a cryptography-aware reviewer. Changes are tested in isolated environments before staging.

### PII redaction or anonymization logic

**Why:** data exposure has regulatory and trust consequences. A bug that lets PII leak through redaction is a SEV-1 with potential fines.

**The failure mode:** an AI-authored regex update for PII redaction is "more permissive" — designed to catch more PII patterns. The new regex actually matches less; some PII slips through. Customer logs contain names and phone numbers; downstream systems index them; a customer notices and reports.

**How human-led works:** PII redaction logic is written by privacy-aware engineers; reviewed by privacy lead; tested against a fixture that includes diverse PII patterns; mutation-tested.

### Data deletion, retention, GDPR right-to-be-forgotten flows

**Why:** regulatory exposure. Failed deletion under GDPR or similar carries fines and trust loss. "Mostly worked" isn't acceptable.

**The failure mode:** an AI-authored change to the deletion job adds a "performance optimization" that batches deletions. The batching logic has a bug at boundary conditions; some records survive deletion. A customer GDPR request fails the verification step; the company has to disclose.

**How human-led works:** deletion logic is written by engineers familiar with the regulatory requirements. Code review includes a compliance-aware reviewer. Tests verify deletion is complete (not just that the deletion code ran).

### Production database schema migrations

**Why:** typically irreversible. Per `agent-autonomy-levels/forbidden-categories.md`, schema migrations applied without human approval are forbidden. Bad migrations cause data loss; recovery may require restoring from backup with downtime.

**The failure mode:** an AI-authored migration drops a column that's still referenced in a stored procedure no one remembers. Production breaks; customers see errors; the rollback requires a maintenance window.

**How human-led works:** migrations are written by engineers, reviewed by a senior, tested against staging with production-shaped data, and deployed through human-mediated approval.

### Production data backfills affecting more than a defined row threshold

**Why:** data corruption is hard to reverse. A backfill that updates 10M rows incorrectly is much worse than a backfill that updates 1K rows incorrectly.

**The failure mode:** an AI-authored backfill script "optimizes" the update query in a way that doesn't preserve the WHERE clause's semantics. Instead of updating rows where `state = 'pending'`, it updates all rows. Operations team discovers when customers report unexpected state changes.

**How human-led works:** backfills are designed by engineers, reviewed for correctness, tested at small scale (1% of rows), validated, then run at full scale. The agent assists with the SQL; the engineer owns the decision.

### Anything that touches the customer of record without a transaction log

**Why:** auditability. Customer-facing changes need a record of what changed, who did it, why. AI-authored changes that bypass the log destroy the audit trail.

**The failure mode:** an AI-authored "cleanup" job updates customer records based on a pattern. The job runs to completion; no transaction log exists. A customer notices and asks "why was my plan changed?" — there's no answer.

**How human-led works:** changes that touch customer records go through systems that log who/what/when/why. AI can assist with the change; the system enforces the logging.

## What "never autonomous" means in practice

For each Tier 1 category:

- **Maximum autonomy level:** L1 (suggest only; human approves each edit). Per `agent-autonomy-levels/legacy-codebase-autonomy-rule.md` and the broader autonomy ladder, this is independent of harness maturity.
- **Required reviewers:** at least one senior engineer; for some items (auth, payments) a domain-specific reviewer (security, finance, privacy).
- **Required tests:** beyond standard tests, the team's harness should include subagent review specific to the category (security-reviewer for auth; payments-reviewer for billing).
- **Required documentation:** changes go through ADRs or design docs proportional to the change.

What this means for engineers:

- You can use AI tooling to read auth code; you cannot use it to write auth code without a human in the loop on every edit.
- You can use AI tooling to suggest tests for billing; you write the actual billing logic yourself.
- You can use AI tooling to draft a migration; the migration ships only after a senior reviews it.

## What's NOT on the Tier 1 list

The list is intentionally specific. Things that are NOT Tier 1:

- **AI-assisted refactoring of legacy code in non-Tier-1 categories.** That's the legacy onboarding program's domain (per `legacy-codebase-onboarding/`).
- **Changes to logs or monitoring.** Tier 2 — observability changes are AI-cautious but not Tier 1.
- **Internal-only scripts.** Tier 3.
- **Documentation about Tier 1 systems.** Tier 3 (the documentation isn't the auth code).

If a specific case isn't on the Tier 1 list but feels like it should be, see [`my-use-case-decision-flow.md`](my-use-case-decision-flow.md). The discipline is to NOT add items to Tier 1 informally; new additions go through the catalog governance review.

## How to enforce Tier 1 mechanically

Tier 1 is mostly procedural (review discipline) but mechanical enforcement helps. Specifically:

### CODEOWNERS

- Auth-related paths: requires security team review
- Billing / payments paths: requires payments team review + finance lead
- Migrations directory: requires senior engineer review + DBA-equivalent
- PII / privacy paths: requires privacy lead review

### Hooks

- `governance/hooks/no-force-push-on-shared-branches.sh`
- `governance/hooks/no-direct-production-db-access.sh`
- `governance/hooks/migration-requires-approval.sh`

### Subagents

- `governance/subagents/security-reviewer.yaml` — flags any change in auth-related paths
- `governance/subagents/payments-reviewer.yaml` — flags any change in billing-related paths

### MCP permission boundaries

- Agent has read-only access to production database; write access requires human approval
- Agent has no access to production secrets

## Common pushback

### "But the AI can write good auth code now"

The capability isn't the question. The question is the failure mode and the cost of being wrong. Even if the AI is correct 99% of the time, auth code at scale produces 1% failures that compound into security incidents. Human leadership is the protection.

### "We slow ourselves down with this discipline"

The discipline is targeted. Tier 1 is roughly 5-10% of engineering work in most teams. The remaining 90-95% benefits from full AI tooling. Tier 1 protection doesn't slow the rest.

### "Other companies don't have this catalog"

Some don't. Those companies typically appear in incident reports. The empirical record across 2025-2026 is consistent: companies without explicit do-not-automate discipline produce more security and compliance incidents than companies with it.

### "This catalog will become outdated"

Per [`catalog-governance.md`](catalog-governance.md), the catalog is reviewed quarterly. New domains get classified; obsolete items are removed. The catalog is living, not static.

## Companion artifacts

- [`tier-2-mandatory-human-gate.md`](tier-2-mandatory-human-gate.md) — adjacent
- [`tier-3-light-human-gate.md`](tier-3-light-human-gate.md) — adjacent
- [`my-use-case-decision-flow.md`](my-use-case-decision-flow.md) — when in doubt
- `agent-autonomy-levels/forbidden-categories.md` — adjacent (the L5 capabilities)
- `agent-autonomy-levels/task-taxonomy-rubric.md` — adjacent (mapping work to levels)
- Ch 33 §33.1 — source
