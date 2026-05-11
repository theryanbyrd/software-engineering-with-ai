# The Autonomy Ladder — L0 through L5

Direct expansion of Ch 32 §32.1's six levels. Use this as the team's published ladder.

## The six levels at a glance

| Level | Name | Description | Required gates |
|-------|------|-------------|----------------|
| **L0** | Read-only | Agent reads, asks questions, suggests. Cannot edit. | None |
| **L1** | Local edits with explicit approval | Agent proposes edits; human approves each. | Per-edit approval |
| **L2** | Bounded autonomous task | Agent runs defined task end-to-end on a feature branch; human reviews PR. | Plan approval; PR review |
| **L3** | Multi-task autonomy under supervision | Agent runs queue of tasks with periodic human checkpoints. | Pre-defined task whitelist; daily review |
| **L4** | Auto-merge for low-risk, narrow categories | Agent opens PR, AI reviewer approves, CI gates, auto-merge to main. | Tier-restricted (docs, tests, type fixes only); CODEOWNERS; full CI |
| **L5** | Production write-path access | **FORBIDDEN.** | **NEVER** |

---

## Detailed criteria for each level

### L0 — Read-only

**What the agent can do:**
- Read files; explore the codebase
- Answer questions about code structure, behavior, dependencies
- Propose changes verbally (in chat)
- Generate diffs that the human can copy/paste

**What the agent CANNOT do:**
- Edit any file
- Run any command that mutates state
- Open any PR

**Required harness:**
- None beyond agent permissions configured to read-only
- Useful but not required: CLAUDE.md, AGENTS.md (improve agent's responses but L0 still works without)

**When L0 is the right level:**
- Newly arrived engineer in their first 1-2 weeks (per `legacy-codebase-onboarding/30-60-90-day-plan.md`)
- Brand new codebase the agent has never seen
- Brownfield code at MVH Level 0 (per `starter-kits/legacy-bridge/MVH_LEVELS.md`)
- High-stakes exploration where any agent edit would be premature

**Common failure mode:** Engineers skip L0 and go straight to L1+. The agent's first edits are confidently wrong because the agent hasn't read enough yet. Two weeks of L0 prevents weeks of slop later.

---

### L1 — Local edits with explicit approval

**What the agent can do:**
- Edit files (typically one at a time)
- Run read-only commands (verify, tests, lint)
- Propose multi-file changes that human approves before each one

**What the agent CANNOT do:**
- Open a PR autonomously
- Make changes the human hasn't seen
- Run state-mutating commands without approval

**Required harness:**
- CLAUDE.md and/or AGENTS.md at the repo level
- A `verify` command that runs locally (lint + typecheck + tests)
- Pre-commit hooks (the bash firewall, slop-detector — see `governance/hooks/`)

**Required discipline:**
- The engineer reads every diff before approving
- The engineer does not approve in batches; each edit is reviewed

**When L1 is the right level:**
- New engineer's first 30-90 days on a codebase
- Legacy codebase modules at MVH Level 1 (per Ch 11 §11.6)
- High-blast-radius changes where every edit warrants review
- Any work in AI-dangerous categories (per [`task-taxonomy-rubric.md`](task-taxonomy-rubric.md))

**Common failure mode:** The engineer approves edits without reading them carefully. The "L1 ceremony" becomes rubber-stamping. If you're approving without reading, you're operating at L2 with extra friction.

---

### L2 — Bounded autonomous task

**What the agent can do:**
- Run a defined task end-to-end on a feature branch
- Make multi-file changes
- Run commands the agent decides are needed (within the bash firewall)
- Open a PR when the task is complete

**What the agent CANNOT do:**
- Self-merge the PR (human review is required)
- Touch files outside the task's scope
- Make changes outside the agent's pre-defined task

**Required harness:**
- Everything from L1 plus:
- A bash firewall (per `starter-kits/agent-friendly/governance/`)
- PR templates that surface AI authorship classification (per Ch 31 §31.6)
- Slop-detector hook running on PRs

**Required discipline:**
- The engineer writes a plan before launching the agent (per Ch 19 — agent-ready specs)
- The engineer reviews the PR substantively, not in 5 minutes
- The engineer catches the seven slop signatures (Ch 22 §22.2)

**Required history:**
- 30+ AI-assisted PRs reviewed at L1 without slop incidents

**When L2 is the right level:**
- Mature codebase with harness in place
- Engineer with L1 experience
- AI-friendly tasks (per [`task-taxonomy-rubric.md`](task-taxonomy-rubric.md))
- Legacy codebase modules at MVH Level 2-3 with seasoned owner

**Common failure mode:** The engineer doesn't review the PR carefully because "it's bounded" — but bounded doesn't mean correct. The seven slop signatures still apply at L2.

---

### L3 — Multi-task autonomy under supervision

**What the agent can do:**
- Run a queue of tasks across files / modules
- Open multiple PRs in sequence
- Self-direct between tasks within the queue

**What the agent CANNOT do:**
- Run tasks outside the pre-defined whitelist
- Self-merge any PR
- Modify the task queue itself

**Required harness:**
- Everything from L2 plus:
- Subagent infrastructure (security-reviewer, performance-reviewer)
- Automated review checkpoints
- Per-task time budgets and cost ceilings

**Required discipline:**
- Daily review of agent activity
- Weekly retrospective on L3 task outcomes
- Pre-defined task whitelist that's narrow and reviewed

**Required history:**
- Subagent roster in production
- 90 days of clean L2 operation
- Demonstrated ability to recognize when L3 should be paused

**When L3 is the right level:**
- Mature team with mature harness
- Engineer with L2 certification (per [`certification-gates.md`](certification-gates.md))
- Whitelist of well-understood task types (e.g., adding type annotations, generating test scaffolds, updating documentation across modules)

**Common failure mode:** The whitelist gets broader over time. "Adding type annotations" becomes "adding type annotations and small refactors and dependency bumps." The expansion is creep; the failure modes diverge from what the harness was tuned for.

---

### L4 — Auto-merge for low-risk, narrow categories

**What the agent can do:**
- Open a PR
- Have an AI reviewer approve it (subagent)
- Pass through CI
- Auto-merge to main

**What the agent CANNOT do:**
- Operate outside the tier-restricted whitelist (docs, tests, type fixes only)
- Bypass CODEOWNERS or CI
- Touch any AI-dangerous category (per [`forbidden-categories.md`](forbidden-categories.md))

**Required harness:**
- Everything from L3 plus:
- CODEOWNERS rigorously enforced
- Full CI suite that gates auto-merge
- Automated rollback exercised within the last 30 days
- Tier-restricted whitelist (DOCS / TESTS / TYPES only)

**Required discipline:**
- Zero auto-merge incidents in 90 days
- Rollback mechanism tested within last 30 days
- Continuous monitoring of post-merge behavior

**Required history:**
- 90 days of L3 operation without auto-merge incidents
- Proven rollback capability
- AI reviewer subagent has track record of catching issues

**When L4 is the right level:**
- High-volume low-risk work where human review is the bottleneck
- Specifically: documentation updates, test additions, type annotations
- NEVER: feature work, refactors, dependency upgrades, anything customer-facing

**Common failure mode:** Whitelist expansion. The team starts with "docs only," then adds "and tests," then "and small refactors." Each expansion looks reasonable; the cumulative expansion is incident-prone.

---

### L5 — Production write-path access — FORBIDDEN

L5 is not a level. It's a label for things that should never happen.

See [`forbidden-categories.md`](forbidden-categories.md) for the comprehensive list. The summary:

- Direct write access to production databases
- Direct read access to production secrets (including via "convenience" env vars)
- Schema migrations applied without human approval
- Code changes to auth, authz, billing, payments, permissions without human review
- Access to keys/tokens wide enough to read private repos org-wide
- Tool configurations where untrusted input can reach production credentials

These are not "current best practice." They are non-negotiable. Per Ch 32:

> Every major incident in the 2025–2026 catalog (Replit DB wipe, Grigorev Terraform-destroy, PocketOS production wipe, Comment-and-Control credential theft, Invariant Labs MCP cross-repo exfiltration) traces to a violation of one of these rules.

---

## How to publish the ladder

The team's published ladder should be:

1. **Visible.** A specific URL, file in the repo, or wiki page that engineers can find in <30 seconds.
2. **Specific.** Names the team's current level for each work category, not generic descriptions.
3. **Versioned.** Has a date and a change log when level changes happen.
4. **Tied to certifications** (per Ch 44 and [`certification-gates.md`](certification-gates.md)).

A typical published ladder looks like:

```
# [Team Name] Autonomy Ladder

Last updated: 2026-MM-DD
Version: 4

## Current state

| Work category | Current level | Last raised | Next review |
|---|---|---|---|
| Documentation | L4 | 2026-Q1 | 2026-Q4 |
| Tests | L3 | 2026-Q2 | 2026-Q4 |
| Type annotations | L3 | 2026-Q2 | 2026-Q4 |
| Bug fixes (T1) | L2 | 2026-Q1 | 2026-Q3 |
| Feature work (T2) | L2 | 2025-Q3 | 2026-Q3 |
| Refactors (T2) | L2 | 2025-Q4 | 2026-Q3 |
| Auth / billing | L1 | n/a — capped | review only on incident |
| Database migrations | L1 | n/a — capped | review only on incident |

## Currently FORBIDDEN

[List from `forbidden-categories.md`]

## Required certifications

[Link to `certification-gates.md`]
```

## What this ladder will NOT do

- Will not work without leadership backing. The ladder is a discipline; without it, drift wins.
- Will not work as a one-time exercise. Quarterly review is the discipline.
- Will not eliminate judgment. The rubric helps; engineers still make calls.

## Companion artifacts

- [`task-taxonomy-rubric.md`](task-taxonomy-rubric.md) — what work runs at which level
- [`raising-and-lowering-autonomy.md`](raising-and-lowering-autonomy.md) — moving levels
- [`forbidden-categories.md`](forbidden-categories.md) — the L5 list
- [`legacy-codebase-autonomy-rule.md`](legacy-codebase-autonomy-rule.md) — the brownfield ceiling
- Ch 32, Ch 44 — sources
