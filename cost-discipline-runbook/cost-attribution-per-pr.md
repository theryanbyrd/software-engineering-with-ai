# Cost Attribution per PR

How to attribute token spend to specific PRs, engineers, and teams. Per Ch 29 §29.4:

> Tag every call with team, product, and developer. Roll up daily. Publish a weekly leaderboard of cost-per-merged-PR by team — the goal is not to shame high spenders; it is to make spend visible.

This file is the operational structure for per-PR attribution.

## Why per-PR attribution matters

Without per-PR cost data:
- "We spent $X on AI tooling this month" is the only number; can't act on it
- High-cost work and low-cost work are aggregated; patterns can't be seen
- Engineers don't know what their work costs in tokens

With per-PR cost data:
- Cost-per-merged-PR by team becomes a metric (per Ch 31 §31.1's six metrics)
- High-cost PRs surface for review (was it warranted? was the model right?)
- Engineers develop intuition about cost
- Attribution to product / feature lets finance allocate cost to revenue

## What to attribute per PR

The data:

| Field | What it captures |
|---|---|
| **PR ID** | The pull request the work resulted in |
| **Engineer** | The engineer driving the work |
| **Team** | The team owning the PR |
| **Product / surface** | The product area (e.g., billing, search, mobile) |
| **Total tokens (input)** | Sum across all sessions tied to this PR |
| **Total tokens (output)** | Same |
| **Cost (USD)** | Computed from tokens × pricing |
| **Model mix** | % Haiku / % Sonnet / % Opus by token volume |
| **Sessions** | Count of distinct agent sessions tied to the PR |
| **AI authorship classification** | Per Ch 31 §31.6 — `ai:none` / `ai:assisted` / `ai:authored` / `ai:agent` |
| **Outcome** | Merged / closed / abandoned |

## How to capture per-PR attribution

The mechanism:

### 1. Agent sessions tagged with PR ID

When the engineer starts an agent session, the session is tagged with the PR ID (or, if the PR doesn't exist yet, with a draft / branch name that resolves to a PR later).

Implementation:
- IDE plugin sets a tag at session start based on current branch
- Agent's gateway records the tag with each call
- When the PR is merged, the tag links to the PR ID

### 2. LLM gateway tracks per-tag spend

The gateway aggregates per-tag spend in real time:
- Total tokens (in/out) per tag
- Total cost per tag
- Model mix per tag

### 3. PR merge enriches with PR metadata

When a PR merges:
- PR description, files changed, CI results
- AI authorship classification from PR labels
- Author and team metadata

### 4. Dashboard surfaces the data

The team's cost dashboard shows:
- Top N PRs by cost (per week / month)
- Cost-per-merged-PR by team (rolling average)
- Cost distribution (median, p75, p90, p95)
- Outlier flagging (PRs >2 standard deviations above team mean)

## What good per-PR cost looks like

Calibration anchors (these vary by team and codebase, but are reasonable starting points):

| PR scope | Typical cost range |
|---|---|
| **Trivial** (typo fix, README update) | $0.10 - $1 |
| **Small** (single-file bug fix; well-scoped) | $1 - $10 |
| **Medium** (small feature; multi-file) | $10 - $50 |
| **Large** (substantial feature; cross-system) | $50 - $200 |
| **Very large** (architectural change; migration) | $200 - $1000 |

If a "trivial" PR cost $50, something went wrong. If a "very large" PR cost $5, the engineer probably did most of it manually (which is fine; not every PR uses heavy AI).

## How to use per-PR data

### Engineer self-review

Engineers see their own per-PR cost data. They develop intuition:
- "This bug fix cost $30 because I let the agent explore too long; next time I scope tighter"
- "This refactor was $200 but it should have been Sonnet, not Opus; routing fix"
- "My typo-fix PRs are $0.50; that's fine"

### Manager 1:1 conversations

In 1:1s, the manager can reference:
- "Your team's cost-per-merged-PR is in the 90th percentile this month; let's look at why"
- "I see a $400 PR; want to walk me through it?"
- "Your cost has dropped 30% over the quarter; what changed?"

### Team retrospectives

In team retros, the team can review:
- "We had three $300+ PRs this sprint; pattern?"
- "Our cost-per-merged-PR is trending up; investigation"

### Outlier review

Per Ch 29 §29.4:

> Most teams discover that 80% of cost comes from 20% of usage, and most of that 20% is one of: (a) Opus on routine tasks, (b) agents in retry loops, (c) one developer running unattended overnight jobs nobody approved.

Outlier review surfaces these patterns. The discipline is to investigate the top 10% of PRs by cost monthly.

### Finance attribution

For chargeback / showback to product or revenue lines:
- Sum cost per product / surface per month
- Compare against revenue per product / surface
- Surface cost-per-revenue ratios

This is the discipline that makes AI tooling investment defensible per Ch 29 §29.4.

## Common attribution failure modes

### Sessions not tagged

Engineer's session isn't linked to a PR. The cost goes to a generic bucket. The data is unattributable.

Mitigation: IDE plugin auto-tags from branch; explicit tag at session start in CLI tools.

### Multiple sessions per PR not aggregated

Engineer worked on a PR across 5 sessions over 3 days. The dashboard shows 5 separate cost entries, not one PR-level rollup.

Mitigation: aggregation happens at PR merge time, rolling up all tagged sessions.

### Sessions tagged to old PRs

Engineer's branch was previously a PR; the new work is on a different PR but the session is still tagged to the old one.

Mitigation: re-tag at branch switch; explicit PR association at session start.

### Cost attribution without context

The dashboard shows raw cost numbers without context (PR scope, complexity, outcome). Outliers can't be evaluated.

Mitigation: enrich with PR metadata; allow click-through to the actual PR.

## Privacy and surveillance

Per-PR cost data is operational data. The discipline is to use it for routing and patterns, not for surveillance.

Lines:

- ✅ Engineers see their own cost; team data is visible to the team
- ✅ Managers reference patterns in 1:1s constructively
- ✅ Outlier review surfaces routing issues, not engineer "performance"
- ❌ Per-developer cost as performance review input
- ❌ Public ranking of engineers by cost ("leaderboards" in the punitive sense)
- ❌ Cost data shared without engineer awareness

## What this attribution will NOT do

- Will not work without telemetry (per Ch 29 §29.3)
- Will not eliminate cost variation. Some PRs are legitimately expensive.
- Will not capture all AI-tooling cost. Some sessions don't result in PRs (exploration, debugging, learning); that's fine.
- Will not produce useful data without consistent tagging discipline.

## Companion artifacts

- [`token-budgets-by-team.md`](token-budgets-by-team.md) — the budgets the attribution informs
- [`model-routing-rubric.md`](model-routing-rubric.md) — adjacent (the routing decisions per PR)
- [`monthly-cost-review-structure.md`](monthly-cost-review-structure.md) — the cadence that uses the data
- Ch 29 §29.4, Ch 31 §31.1 — sources
