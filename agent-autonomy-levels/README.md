# Agent Autonomy Levels — L0 through L5 Framework

The autonomy ceiling framework. Direct implementation of Chapter 32 of [_Software Engineering with AI: A Practical Handbook for the Claude Code Era_](https://www.linkedin.com/in/ryanbyrd) by Ryan Byrd, with cross-references to Chapter 11 §11.6 (the legacy autonomy ceiling) and Chapter 44 (certifications gate autonomy).

The book's framing:

> The single most useful governance artifact you can publish is an explicit autonomy ladder. Without one, autonomy drifts upward by accident — a senior engineer tunes their permission mode looser, a junior copies it, the team norm shifts, and six months later you have agents merging to main with no human gate.
>
> — Ch 32 opening

This folder turns the ladder into operational practice: rubric for what work runs at which level, the conversation about raising and lowering autonomy, the certification path, and the cross-reference to the legacy-codebase rule.

## What's in here

| File | Purpose |
|---|---|
| [`autonomy-ladder.md`](autonomy-ladder.md) | The L0-L5 ladder with detailed criteria for each level |
| [`task-taxonomy-rubric.md`](task-taxonomy-rubric.md) | The decision rubric: which work runs at which autonomy level |
| [`raising-and-lowering-autonomy.md`](raising-and-lowering-autonomy.md) | The conversation and discipline for moving levels up or down |
| [`forbidden-categories.md`](forbidden-categories.md) | The L5 / never-allowed categories with reasoning and incident references |
| [`legacy-codebase-autonomy-rule.md`](legacy-codebase-autonomy-rule.md) | The "L1/L2 only for first six months in legacy" rule from Ch 11 §11.6, with the path to higher autonomy |
| [`autonomy-drift-monitoring.md`](autonomy-drift-monitoring.md) | How to detect upward drift and what to do about it |
| [`certification-gates.md`](certification-gates.md) | Per Ch 44, certifications gate autonomy access |

## The book's core stance

Per Ch 32:

> Trust is co-constructed — the model, the user, and the harness all change. Codify autonomy explicitly instead of letting it drift upward by accident.

Three things follow:

1. **L5 is forbidden, not aspirational.** It's a label for things that should never happen, not a level to grow toward.
2. **The team's autonomy level is the harness's level, not the most capable individual's.** A team operates at the level its discipline has earned, not at the level its best engineer wishes for.
3. **Drift is real and asymmetric.** Auto-approve rates climb 20% → 40%+ over 750 sessions per Anthropic's Feb 2026 paper. Without explicit discipline, drift wins.

## Who this is for

- **Engineering managers** setting autonomy norms for their teams
- **Tech leads** calibrating which tasks run at which level
- **VPs of Engineering / CTOs** publishing the org's autonomy ladder
- **Platform team** (per `platform-team-charter/`) implementing the ladder mechanically
- **Senior engineers** who need to push back on autonomy creep

## Read first

- Ch 32 — the source chapter (the six levels, forbidden categories, promotion criteria)
- Ch 11 §11.6 — the legacy codebase autonomy ceiling
- Ch 44 — certifications gate autonomy
- `legacy-codebase-onboarding/` — adjacent (the broader brownfield program)
- `incident-postmortem-templates/harness-deficiency-checklist.md` — autonomy downgrade as one of the seven harness mechanisms

## What this framework WILL do

- Make autonomy levels explicit and reviewable
- Surface drift before it produces incidents
- Give engineers and managers shared language for "this work is at L1, not L3"
- Provide certification gates that prevent informal drift
- Distinguish AI-friendly work (L2-L4 candidate) from AI-cautious (L1-L2) from AI-dangerous (L0-L1, human leads)

## What this framework will NOT do

- Will not work without harness in place. L1+ requires CLAUDE.md, AGENTS.md, verify, hooks. L2+ requires PR review discipline. L3+ requires subagents.
- Will not work in cultures where "we're moving fast" overrides discipline. Autonomy creep is faster than discipline; without leadership backing, the ladder is decorative.
- Will not protect against the forbidden categories. L5 work that bypasses the ladder is a different kind of failure.
- Will not eliminate judgment. Some tasks sit between AI-friendly and AI-cautious; the rubric helps but doesn't decide.

## The core idea

Autonomy is not a model property; it is a team-and-harness property. A specific task running at a specific level requires:

1. **The harness** — the mechanical infrastructure that catches errors
2. **The discipline** — the team's review practice
3. **The history** — incident-free operation at the prior level
4. **The category** — the work itself is appropriate for that level

If any of the four is missing, the level isn't earned, regardless of how capable the model is or how much the team wants to move faster.

## Companion artifacts

- `legacy-codebase-onboarding/` — adjacent program for inheriting brownfield
- `governance/` — the mechanical infrastructure (hooks, MCP boundaries) that enforces autonomy levels
- `incident-postmortem-templates/` — incidents that may trigger autonomy downgrades
- `platform-team-charter/` — the team that builds and maintains the autonomy infrastructure
- `promotion-and-leveling-rubric/` — engineer leveling, separate from autonomy leveling
- Ch 11 §11.6, Ch 32, Ch 44 — sources
