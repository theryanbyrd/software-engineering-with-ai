# Routing Policy Update Process

How to update the team's routing rubric after eval results. The rubric (`cost-discipline-runbook/model-routing-rubric.md`) is the operational artifact engineers use day-to-day; updating it has a process beyond editing a markdown file.

## When this process runs

Triggered by:
- Quarterly model lineup review decision (per [`quarterly-model-lineup-review.md`](quarterly-model-lineup-review.md))
- Mid-cycle review (per the triggers in that file)
- Specific cost incident or capability gap

Most updates are minor (adjusting thresholds, adding a model for a specific work type). Major updates (primary model switch) are quarterly events at most.

## The update process

### Step 1 — Document the decision

Before changing anything, document:
- What's changing
- Why (with reference to specific benchmark data)
- When (rollout date)
- Who (decision owner; whoever's accountable for the success of the change)

This document is the authoritative reference for what was decided. If the team later asks "why did we make this change," this is the answer.

### Step 2 — Update the routing rubric

Edit `cost-discipline-runbook/model-routing-rubric.md` to reflect the new policy:

- Default model for routine work (if changing)
- Escalation paths (Sonnet → Opus thresholds)
- Demotion paths (when to use Haiku)
- Subagent model assignments
- Skill model assignments

Each change has rationale tied to the benchmark data.

### Step 3 — Update tooling configuration

The rubric is the documentation; the tooling enforces it. Update:

- **LLM gateway configuration**: default model, routing rules, fallback rules
- **Skill frontmatter**: each skill's `recommended_model` field
- **Subagent definitions**: each subagent's model assignment
- **CI / CD configuration**: any model assignment in pipelines
- **IDE plugin defaults**: if your team configures default model at the IDE level

This is where most engineers experience the change. If tooling isn't updated, the rubric is decorative.

### Step 4 — Update CLAUDE.md / AGENTS.md

If the change affects how engineers should think about model selection, update CLAUDE.md and AGENTS.md:

- Specific model recommendations for specific work types
- Any nuances about the new model (e.g., Opus 4.7 tokenizer caveat per Ch 26 §26.3)
- Migration notes if engineers need to adjust their workflows

### Step 5 — Communicate

Two layers of communication:

#### Layer 1 — Announcement

Before the change takes effect:
- All-hands or team-channel announcement
- What's changing, when, why
- What engineers need to do (often: nothing; the tooling handles it)
- Where to read more (link to the rubric, the decision document, relevant chapter)

#### Layer 2 — In-product

The change shows up in their day-to-day:
- IDE plugin shows new default model
- LLM gateway routes their requests differently
- Skill invocations use different models

If the in-product experience is surprising (engineers see different behavior they didn't expect), Layer 1 communication wasn't enough.

### Step 6 — Monitor

After the change:

- **Per-PR cost data** (per `cost-discipline-runbook/cost-attribution-per-pr.md`) — does cost match expectations?
- **Defect rate by AI authorship** — does quality match expectations?
- **Engineer feedback** — surface in retros; specific signals (the new model is hallucinating in X way; the routing isn't catching Y work)

For 30 days after the change, the platform team monitors actively. If anomalies surface, mid-course corrections.

### Step 7 — Document the rollback plan

Before the change takes effect, the rollback plan is documented:
- What's the trigger for reverting? (specific cost threshold; specific defect rate; specific engineer-reported failure mode)
- What's the process? (reverse the tooling configuration; communicate; learn from what went wrong)
- Who decides? (decision owner from Step 1)

Most updates don't need rollback. Having the plan reduces the cost of needing it.

## Common update patterns

### Pattern 1 — Primary model switch

Largest update. All steps apply; communication is org-wide.

Timeline: 4-8 weeks from decision to change taking effect (allows for gradual rollout if warranted).

### Pattern 2 — Add specialized model to lineup

A new model is added for a specific work type while primary stays the same.

Timeline: 2-4 weeks. Tooling updates focus on routing (the new model is invoked for specific patterns).

### Pattern 3 — Adjust routing thresholds

The rubric's thresholds for escalation/demotion change. E.g., Opus is now used for migrations of any size, where it used to be only for >X-line migrations.

Timeline: 1-2 weeks. Tooling change is small.

### Pattern 4 — Pricing-driven routing change

A model's pricing changed; routing math is updated. No capability change.

Timeline: 1 week. Communication is "we're updating routing because pricing changed; here's the new math."

### Pattern 5 — Deprecation-driven migration

The current primary is being deprecated; team must migrate.

Timeline: driven by vendor's deprecation date. Plan to migrate 4-8 weeks before the date.

## Anti-patterns

### Updating the rubric without updating tooling

The rubric says one thing; the tooling does another. Engineers experience the tooling, not the rubric. The rubric becomes decorative.

Mitigation: tooling change is part of the update process. If it's not done, the update isn't done.

### Updating tooling without updating the rubric

The tooling does the new thing; the rubric still describes the old. Engineers get confused.

Mitigation: rubric and tooling stay in sync. Versioning helps — both have a version stamp.

### Updates without monitoring

The change ships; nobody watches what happens. Anomalies (cost spike, quality drop) aren't caught until the monthly review.

Mitigation: 30-day active monitoring period after major changes. Per `cost-discipline-runbook/anomaly-detection-workflow.md`, alerts should fire on spike conditions.

### Communication via tooling change

Engineers learn about the update by experiencing the tooling change. They feel managed-around.

Mitigation: announcement before the change. The announcement is short but explicit.

### Rollback plan made up after the fact

Something goes wrong; the team scrambles to figure out how to revert. The improvised rollback has its own problems.

Mitigation: rollback plan documented before the change. Even if never used, having it reduces cost of needing it.

## What this process will NOT do

- Will not eliminate update friction. Each update has real overhead; the process minimizes the overhead.
- Will not work without leadership backing. If updates take 6 weeks because every step requires sign-off, the team will route around the process.
- Will not catch every issue. Some issues only emerge in production at scale.
- Will not work if the rubric isn't authoritative. If engineers don't trust the rubric, they ignore it.

## Companion artifacts

- [`when-to-switch-primary-model.md`](when-to-switch-primary-model.md) — what triggers updates
- [`quarterly-model-lineup-review.md`](quarterly-model-lineup-review.md) — when updates are decided
- `cost-discipline-runbook/model-routing-rubric.md` — what gets updated
- `cost-discipline-runbook/cost-attribution-per-pr.md` — monitoring data
- Ch 26 §26.1, §26.5 — sources
