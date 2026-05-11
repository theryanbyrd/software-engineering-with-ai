# Token Budgets by Team

The structure for setting and managing team-level token budgets. Direct application of Ch 29 §29.4 (allocation to developers/products) and §29.5 (budget guardrails and alert thresholds).

## Why team-level budgets

Per Ch 29 §29.4:

> Tag every call with team, product, and developer. Roll up daily. Publish a weekly leaderboard of cost-per-merged-PR by team — the goal is not to shame high spenders; it is to make spend visible. Most teams discover that 80% of cost comes from 20% of usage, and most of that 20% is one of: (a) Opus on routine tasks, (b) agents in retry loops, (c) one developer running unattended overnight jobs nobody approved.

Without team-level visibility, cost is a single opex line and there's no leverage to manage it. With team-level visibility, the conversation shifts to "is Team X's spend pattern healthy?" — which is actionable.

## Setting team budgets

### Initial sizing

For a team that has 6-12 months of historical AI tooling usage:

1. **Take the trailing 90-day mean monthly spend** as the baseline
2. **Add 15-20% growth allowance** for natural increase in usage
3. **Set the budget at the resulting number** rounded to a clean figure

For a team without historical data (new AI tooling adoption, new team):

1. **Start with the per-developer benchmark from Ch 29 §29.1:** $150-$250/developer/month, with 90th-percentile under $30/active-day
2. **Multiply by team size** to get a starting budget
3. **Add 20-30% buffer for ramp** (the first 60 days of adoption have higher spend per useful output)
4. **Plan to recalibrate at 90 days** based on actual usage

### Budget structure

Each team's budget has multiple components:

| Component | What it covers | Typical share of total |
|---|---|---|
| **Active development** | Engineers using AI in normal work | 60-75% |
| **Background agents** | Subagents running in CI, scheduled jobs | 10-20% |
| **Experimentation** | Engineers trying new patterns, evaluating tools | 5-10% |
| **Buffer** | Unexpected spikes within budget | 10-15% |

Tracking by component helps with attribution. A team running 40% on background agents probably has a routing problem; a team running 30% on experimentation is investing in capability.

### Per-developer soft cap

Per Ch 29 §29.5:

> Per-developer soft cap: $30/day. Pages developer at 80%, requires manager ack at 100%.

Implement this. The threshold is calibrated to the 90th percentile from Anthropic's data; engineers above it consistently are either solving very hard problems (expected, fine) or are routing inefficiently (correctable).

### Per-team monthly hard cap

Per Ch 29 §29.5:

> Per-team monthly hard cap: team budget × 1.2. Hits page the EM and platform on-call.

The 1.2× hard cap is the protection against runaway spend. If the team is consistently approaching the hard cap, the conversation is: budget recalibration or root-cause investigation, not just "increase the number."

## Communicating budgets to engineers

The discipline isn't about controlling individual engineer behavior. It's about making the cost visible enough that engineers naturally optimize.

### What engineers should know

- The team's monthly budget
- The current month's spend (visible daily)
- Their own per-day spend (visible to them)
- The team's relative position vs. other teams (showback, not chargeback at most companies)

### What engineers should NOT be told

- "Don't use Opus" without context. Opus is the right call sometimes; the model-routing rubric ([`model-routing-rubric.md`](model-routing-rubric.md)) is the discipline.
- "You're spending too much" without specific feedback. If an engineer's spend pattern is wrong, the manager has the conversation in 1:1; broadcasting it is counterproductive.
- "We're cutting budgets next month" without engagement. Cost reduction without engagement produces shadow AI usage, which is worse.

### The dashboard for engineers

Per Ch 31 §31.4, a reference dashboard. For cost specifically:

- Daily spend per engineer (their own, visible to them)
- Daily spend per team (visible to all)
- Per-PR cost attribution (per [`cost-attribution-per-pr.md`](cost-attribution-per-pr.md))
- Model-mix breakdown (% Haiku / % Sonnet / % Opus)

## Setting team budgets at scale

For a 100-engineer organization with 10 teams:

| Team type | Token budget per engineer per month |
|---|---|
| Heavy AI users (mostly greenfield, new features) | $250-400 |
| Mixed (combination of greenfield and brownfield) | $150-250 |
| Brownfield-heavy (legacy modernization) | $100-200 |
| Platform team | $300-500 (heavy harness work) |
| Specialized (security, compliance) | $50-150 (lighter usage) |

These are illustrative. Calibrate against your actual data after 90 days.

## Recalibration cadence

### Monthly

Per the monthly cost review (per [`monthly-cost-review-structure.md`](monthly-cost-review-structure.md)):
- Review actual spend vs budget per team
- Identify teams persistently over budget (root cause: model misuse, agent loops, scope creep)
- Identify teams persistently under budget (root cause: under-adoption, blocked teams)
- Adjust budgets if patterns suggest sustained shifts

### Quarterly

Comprehensive recalibration:
- Full audit of team budgets vs actual
- Adjustment for team scope changes (team grew, team's surface changed)
- Adjustment for vendor cost changes (model pricing, contract changes per `vendor-procurement-runbook/`)
- Adjustment for tokenizer changes (per Ch 29 §29.6: "Opus 4.7's new tokenizer can add up to 35% effective cost vs Opus 4.6")

### Annually

Annual budget setting:
- Set budgets aligned with company budget cycle
- Tie budgets to expected outcomes (per the leverage math in `platform-team-charter/budget-and-headcount-framing.md`)
- Engagement with finance on chargeback / showback structure

## Anti-patterns

### Setting budgets without instrumentation

The team has no visibility into actual usage but sets a budget number. The budget is theatrical; nobody knows if it's being met.

Mitigation: instrumentation first (per Ch 29 §29.3), budgets second.

### Treating budget as cap

The team treats the budget as a hard limit and refuses to go over. This produces shadow AI usage (engineers using personal accounts, free tiers) — which is worse than visible spend.

Mitigation: budgets are targets with hard caps at 1.2×. Going over the budget is a conversation, not a cliff.

### Per-developer caps without per-developer support

A developer hits their daily cap and is locked out. They can't continue working. The company's productivity goes down to save $30.

Mitigation: per-developer caps are soft; the manager ack at 100% is a check, not a stop. The conversation is about pattern, not about the day.

### Team budgets without team accountability

The budget exists but the EM doesn't review it. Spend runs over; nobody notices. The next quarter's budget is set assuming the over-spend was real demand.

Mitigation: monthly review with the EM is the discipline. Without the review, the budget drifts.

### Budgets that don't change despite usage shift

The team adopts a new tool, takes on new scope, or shifts to legacy work. The budget stays the same. The team is either over- or under-budgeted; the discipline is broken.

Mitigation: quarterly recalibration. Don't fix budgets in stone.

## What this structure will NOT do

- Will not work without telemetry. Per Ch 29 §29.3, the OpenTelemetry GenAI standard is the prerequisite.
- Will not eliminate the leadership conversation. Cost is a leadership conversation; budgets are an operational tool.
- Will not work in cultures where engineers route around the budget. Cultural alignment is upstream.
- Will not prevent every cost incident. The anomaly detection ([`anomaly-detection-workflow.md`](anomaly-detection-workflow.md)) is the protection against the spike that exceeds the hard cap.

## Companion artifacts

- [`model-routing-rubric.md`](model-routing-rubric.md) — what engineers do day-to-day
- [`anomaly-detection-workflow.md`](anomaly-detection-workflow.md) — the protection layer
- [`cost-attribution-per-pr.md`](cost-attribution-per-pr.md) — the visibility unit
- [`monthly-cost-review-structure.md`](monthly-cost-review-structure.md) — the cadence
- Ch 29 §29.4-§29.5 — sources
