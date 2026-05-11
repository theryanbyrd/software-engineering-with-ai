# Cost Discipline Runbook — Operational AI Tooling Cost Management

The operational discipline for managing AI tooling cost. Direct implementation of Chapter 29 of [_Software Engineering with AI: A Practical Handbook for the Claude Code Era_](https://www.linkedin.com/in/ryanbyrd) by Ryan Byrd, with cross-references to Ch 31 §31.1 (the six metrics) and Ch 31 §31.4 (executive dashboard).

The book's framing:

> AI tokens are NOT cheap. You can easily spend thousands of unbudgeted dollars per day. Treat AI as an investment or plan for staff reductions if budgets must be maintained absolutely. Track token spend using OpenTelemetry and allocate to developers and products for timely reporting and decision support.
>
> — Ch 29 opening warning

This folder is the runbook for the discipline: token budgets per team, anomaly detection, model routing, cost attribution, and the monthly review structure.

## What's in here

| File | Purpose |
|---|---|
| [`token-budgets-by-team.md`](token-budgets-by-team.md) | The structure for setting and managing team-level token budgets |
| [`model-routing-rubric.md`](model-routing-rubric.md) | When to use Haiku vs Sonnet vs Opus — with cost and capability tradeoffs |
| [`anomaly-detection-workflow.md`](anomaly-detection-workflow.md) | Detection thresholds, alerting, and triage when costs spike |
| [`cost-attribution-per-pr.md`](cost-attribution-per-pr.md) | How to attribute token spend to specific PRs, engineers, and teams |
| [`monthly-cost-review-structure.md`](monthly-cost-review-structure.md) | The monthly meeting that surfaces patterns before they become problems |
| [`cost-blowup-incident-runbook.md`](cost-blowup-incident-runbook.md) | What to do when a cost incident is happening right now |
| [`leadership-conversation-on-cost.md`](leadership-conversation-on-cost.md) | The honest cost-vs-value conversation with finance and executive leadership |

## The book's stance

Per Ch 29:

> Anthropic's own published Claude Code documentation: average $13/developer/active-day, $150–$250/developer/month, with 90th-percentile under $30/active-day. Read those numbers carefully — that means 10% of developers spend over $30/day, which annualizes to $7,000+ per developer per year on tokens alone.
>
> Cursor, on its compute-based plan, has produced single-day individual bills in the $1,400–$7,000 range. One Hacker News-documented case: a $7,000 annual subscription depleted in a single day.

The numbers are real. Without discipline, AI tooling becomes a runaway opex line. With discipline, it's an investment with measurable returns.

The discipline isn't about cutting cost. It's about making cost visible, attributing it, routing intelligently, catching anomalies, and reviewing patterns before they become problems.

## Who this is for

- **Engineering managers** running team-level cost responsibility
- **Platform team** owning the cost dashboard and alerting (per `platform-team-charter/charter.md`)
- **VPs of Engineering / CTOs** running the leadership conversation
- **Finance / FP&A** partnering on the chargeback / showback structure
- **Senior engineers** who need to understand model selection and routing

## Read first

- Ch 29 — the source chapter (executive token cost warning)
- Ch 31 §31.1 — the six metrics (one of which is token spend per developer)
- Ch 31 §31.4 — the reference executive dashboard
- `vendor-procurement-runbook/` — adjacent (the vendor side of cost)
- `platform-team-charter/budget-and-headcount-framing.md` — adjacent (platform team's role in cost discipline)

## What this runbook WILL do

- Make cost visible per developer, per team, per PR
- Provide model-routing guidance that engineers can apply
- Surface anomalies before they're catastrophic
- Build the monthly review discipline that catches patterns
- Give the team language to push back on incoherent leadership demands ("pay for tokens AND freeze hiring AND deliver 2x throughput")

## What this runbook will NOT do

- Will not eliminate cost. AI tooling is a real expense.
- Will not work without instrumentation. Per Ch 29 §29.3, OpenTelemetry GenAI semantic conventions are the standard; if you don't have them, the discipline can't run.
- Will not work in cultures where leadership demands aggressive cost reduction without engagement on the tradeoffs. The leadership-conversation file is for those situations.
- Will not protect against vendor terms changes (per `vendor-procurement-runbook/renewal-discipline.md`). Vendors change pricing; this runbook is for managing the cost given the pricing.

## How this folder fits with adjacent material

| Need | Where to look |
|---|---|
| The vendor side of cost (negotiation, renewal) | `vendor-procurement-runbook/` |
| The platform team's role in cost dashboards | `platform-team-charter/success-metrics.md` |
| The metrics framework that includes token spend | `executive-dashboard/` (if exists) or Ch 31 §31.1 directly |
| The "telemetry has to exist" prerequisite | `governance/telemetry/` |
| The executive conversation about cost vs value | `skip-level-defense/` |

## The core idea

Cost discipline operates at three time horizons:

1. **Real-time** — anomaly detection that fires within minutes when spend goes wrong
2. **Daily** — per-developer and per-team rollups visible to managers
3. **Monthly** — pattern review that surfaces drifts and structural issues

If any horizon is missing, the cost-discipline gap shows up at the missing horizon. Real-time without daily review means anomalies are caught but patterns aren't. Daily without real-time means anomalies become $5K-$10K bills before anyone sees them. Monthly without the others means the discipline is performative.

## Companion artifacts

- `vendor-procurement-runbook/` — the procurement side
- `platform-team-charter/` — the team that builds the cost infrastructure
- `incident-postmortem-templates/` — when cost incidents have postmortems
- `governance/telemetry/` — the OpenTelemetry instrumentation that this runbook depends on
- Ch 29, Ch 31 §31.1, Ch 31 §31.4 — sources
