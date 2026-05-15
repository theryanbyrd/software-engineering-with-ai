# Forbidden Categories — The L5 List

L5 is not a level. It's a label for things that should never happen. Per Ch 32 §32.2:

> Every major incident in the 2025–2026 catalog (Replit DB wipe, Grigorev Terraform-destroy, PocketOS production wipe, Comment-and-Control credential theft, Invariant Labs MCP cross-repo exfiltration) traces to a violation of one of these rules.

This file enumerates the forbidden categories with reasoning, real-incident references, and mechanical enforcement guidance.

## The categories

### 1. Direct write access to production databases

**What's forbidden:**
- Agent invoking `psql`, `mysql`, `mongo` shells against production
- Agent running `aws rds execute-statement` against production
- Agent making writes through any API that touches production data stores

**Why it's forbidden:**
- A single agent error can corrupt or destroy production data
- The blast radius is the entire customer base
- Recovery may be impossible (the data is gone)

**Real incidents:**
- **Replit DB wipe (2025):** an agent with database access destroyed production records. Recovery was incomplete.
- **PocketOS production wipe:** similar pattern.

**Mechanical enforcement:**
- MCP permission boundaries (per `governance/mcp-permission-config.md`)
- Bash firewall blocks production database CLIs (per `governance/hooks/`)
- Production credentials are NOT in any environment the agent can reach
- All production access goes through human-mediated paths

### 2. Direct read access to production secrets

**What's forbidden:**
- Agent reading production API keys, tokens, certificates
- Agent reading production environment variables that contain secrets
- Agent accessing the secrets manager or vault for production
- "Convenience" environment variables that contain production secrets in agent-accessible scopes

**Why it's forbidden:**
- Secrets exfiltrated by an agent (or via prompt injection) cannot be un-exfiltrated
- Even read-only access creates attack surface for prompt injection
- Compromise of one secret typically cascades to broader compromise

**Real incidents:**
- **Comment-and-Control credential theft:** agent with prompt-injection vulnerability extracted credentials via instructions hidden in PR comments
- **GitHub MCP cross-repo exfiltration:** agent with cross-repo permissions exposed private repo content

**Mechanical enforcement:**
- Production secrets in a vault the agent has no access to
- Development-only secrets in agent-accessible environments are different from production secrets
- Audit log of any secret access; alerts on anomalies

### 3. Schema migrations applied without human approval

**What's forbidden:**
- Agent running `alembic upgrade head`, `rails db:migrate`, `prisma migrate deploy`, or equivalent on production
- Agent running `terraform apply` against production
- Any irreversible schema change executed without a human approval gate

**Why it's forbidden:**
- Schema changes are typically irreversible (down migrations are unreliable)
- Wrong migrations can corrupt data or cause silent data loss
- The cost of recovery is high (engineering hours, customer trust)

**Real incidents:**
- **Grigorev / DataTalks.Club (Aug 2025):** Claude Code with Terraform destroyed 2.5 years of records. Per Ch 32, "Terraform `apply` is a Tier 1 forbidden action under any autonomy level."

**Mechanical enforcement:**
- Bash firewall blocks migration commands in agent contexts
- Migration tooling requires human approval gate (e.g., a Slack approval, a Jira ticket)
- CI runs migrations against staging only; production migrations are human-mediated

### 4. Code changes to auth, authz, billing, payments, permissions

**What's forbidden:**
- Auto-merge to any of these surfaces
- Agent operating without explicit human review on these files
- L4 in any path matching auth/billing/permissions

**Why it's forbidden:**
- The failure modes are severe (account takeover, financial loss, privilege escalation)
- Verification is hard; tests don't catch all subtle issues
- The cost of an incident is days of incident response plus customer trust loss

**Mechanical enforcement:**
- CODEOWNERS requires human review on auth/billing/permissions paths
- The slop-detector flags any AI-authored change to these paths with HIGH severity
- A security-reviewer subagent runs on every PR touching these paths
- Auto-merge (L4) explicitly excludes these paths

### 5. Access to keys/tokens wide enough to read private repos org-wide

**What's forbidden:**
- Agent with GitHub PAT that can read all repos in an organization
- Agent with cloud credentials that grant read access to all S3 buckets / all storage
- Any token whose blast radius is "everything in the org"

**Why it's forbidden:**
- Cross-repo or cross-org permissions multiply the impact of any compromise
- Prompt injection can leverage broad access to exfiltrate widely
- The principle of least privilege specifically forbids "convenience" broad tokens

**Real incidents:**
- **Invariant Labs MCP cross-repo exfiltration:** agent with broad GitHub access exfiltrated content across repos via injected instructions

**Mechanical enforcement:**
- Tokens scoped to specific repos / specific buckets only
- Per-task tokens generated at task start, expired at task end
- No "long-lived broad-scope" tokens in agent-accessible environments

### 6. Tool configurations where untrusted text reaches production credentials

**What's forbidden:**
- Agent with both `read_pr_comments` and `production_database_access` in the same tool surface
- Agent with both web fetch and production credential access
- Agent with email reading + production access
- Any configuration where prompt injection from untrusted input can reach production

**Why it's forbidden:**
- Prompt injection is real and unpreventable in current models
- The defense is keeping untrusted input out of the same runtime as production credentials
- This pattern is the root cause of every major prompt-injection incident in 2025-2026

**Mechanical enforcement:**
- MCP permission separation: tools that read untrusted input run in a separate context from tools that have production access
- Audit any new tool surface for this combination
- The prompt-injection test suite (per `prompt-injection-test-suite/`) tests these combinations explicitly

---

## What "forbidden" means in practice

**Forbidden means mechanically prevented, not just culturally discouraged.**

The discipline:

1. **Document the forbidden list** in the team's published autonomy ladder ([`autonomy-ladder.md`](autonomy-ladder.md))
2. **Configure mechanical enforcement** — hooks, MCP boundaries, IAM scopes
3. **Audit quarterly** — verify the configurations still enforce the rules; check if any new tools have created bypass paths
4. **Review post-incident** — every incident postmortem (per `incident-postmortem-templates/`) checks whether a forbidden category was violated; if yes, that's a major finding

## Common loopholes to watch for

### "It's just for debugging"

A forbidden category is unlocked temporarily for debugging or incident response. The unlock isn't logged; the unlock isn't undone.

**Mitigation:** debugging access requires explicit time-boxed grant; logged; auto-revoked; reviewed.

### "It's a non-prod environment"

A "staging" or "non-prod" environment that contains real customer data, real credentials, or real production-equivalent state. The forbidden categories apply because the data is real.

**Mitigation:** non-prod environments contain only synthetic/sanitized data. If real data is needed, the environment is treated as production.

### "The agent only suggests; the human approves"

Agent has access to forbidden surfaces but "only suggests, never executes." This is L0 framing; the agent's access still produces injection risk.

**Mitigation:** L0 means literally read-only access; if the agent can suggest a `terraform apply`, the agent has the credentials to do it.

### "We trust this engineer"

A senior engineer is trusted to bypass the forbidden categories because "they know what they're doing." The bypass is informal; the next engineer copies it.

**Mitigation:** the forbidden categories apply to all engineers and all agents. Trust isn't an exception; the rules are mechanical, not judgment-based.

### "It's a one-time exception"

A specific task requires bypassing a forbidden category. The bypass is documented as one-time. It happens again next quarter; then routinely.

**Mitigation:** if a one-time exception is needed, it requires explicit escalation, logging, and mandatory review; second occurrence requires reconsideration of whether the category is still forbidden or if a permanent path is needed.

## What does NOT belong on this list

The forbidden categories are about agent capability, not engineering practice:

- "AI-authored code in security-sensitive paths" — not forbidden; requires human review (L1)
- "AI-assisted refactoring of legacy code" — not forbidden; requires characterization first (per `legacy-codebase-onboarding/`)
- "AI-written documentation about auth" — not forbidden; standard L4 candidate

The forbidden list is about specific capabilities that produce catastrophic blast radius. Routine sensitive work runs at L1; the forbidden list is for capabilities that can't operate at any level.

## What this list will NOT do

- Will not protect against zero-day capabilities. New AI tools may create new forbidden categories; this list is current as of 2026.
- Will not work without mechanical enforcement. Cultural discipline alone is insufficient.
- Will not eliminate prompt injection. The forbidden list reduces blast radius; the prompt-injection test suite is the complementary discipline.

## Companion artifacts

- [`autonomy-ladder.md`](autonomy-ladder.md) — the levels (L5 is forbidden)
- `governance/mcp-permission-config.md` — MCP enforcement
- `governance/hooks/` — bash firewall and other mechanical enforcement
- `prompt-injection-test-suite/` — adjacent discipline
- `incident-postmortem-templates/` — when a forbidden category is violated
- Ch 32 §32.2 — source
