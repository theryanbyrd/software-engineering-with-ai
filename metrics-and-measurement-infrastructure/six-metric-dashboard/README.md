# The Six-Metric Dashboard

The canonical six metrics from Ch 31 §31.1. One dashboard. No more.

Per the book:

> Six metrics on the dashboard, no more. Resist dashboard sprawl. LLM-graded code maturity is the highest-leverage metric and the highest-investment. Lines of code is the discredited metric for AI productivity.
>
> — Ch 31 §31.7

Per the executive-dashboard table in Ch 31 §31.4:

> If five of those eight are green and three are red, you are in the normal operating range. If all are green, you are either an exceptional organization or your dashboard is lying to you — investigate the second possibility first.

That "investigate the second possibility first" line is the entire philosophy of this dashboard: build something that can show you bad news, then defend against the temptation to build it so it never does.

## The six metrics

Per Ch 31 §31.1, in the book's order:

| # | Metric | File | What it tells you |
|---|---|---|---|
| 1 | AI Token Usage per Developer | [`metric-01-token-usage.md`](metric-01-token-usage.md) | Adoption rate + cost-control input. *Never* a performance metric. |
| 2 | Code Maturity Score (1–10, LLM-graded) | [`metric-02-code-maturity.md`](metric-02-code-maturity.md) | The keystone quality signal. Team-level only. |
| 3 | Features Delivered to Bugs Introduced Ratio | [`metric-03-features-to-bugs.md`](metric-03-features-to-bugs.md) | DORA "change failure rate" inverted. Quality-of-output signal. |
| 4 | Time from User Story to Production | [`metric-04-lead-time.md`](metric-04-lead-time.md) | DORA "lead time" with the in-progress-column anchor. Speed signal. |
| 5 | Story Points Delivered (Quantity) | [`metric-05-velocity.md`](metric-05-velocity.md) | Velocity trend. Paired with #3 — that's how you separate productivity from slop. |
| 6 | Predictability — 1 − (σ/µ) | [`metric-06-predictability.md`](metric-06-predictability.md) | "The single most underrated metric in software engineering." (Ch 31 §31.1) |

The "seventh metric" (Score / Question / Opportunity / Train per Ch 31 §31.5) lives in [`../triage-taxonomy.md`](../triage-taxonomy.md) — it is not on this dashboard because, per the book, it "lives in retro, not on a dashboard."

## Why these six

Per Ch 31 §31, the metric problem in AI-assisted engineering:

> The things that are easy to measure (lines of code, tokens consumed, PR count, suggestion acceptance rate) are exactly the things you do not want to optimize, and the things you do want to optimize (code maturity, predictability, customer outcomes) require either survey instruments or LLM judgment.

These six are deliberately chosen to span the trade-offs:

- **#1 (Token Usage)** is the easy-to-measure metric, included because cost control matters and adoption rate is a useful leading indicator. The discipline is to not over-interpret it.
- **#2 (Code Maturity)** is the hard-to-measure metric. It's the keystone because everything else can be gamed by an AI rollout that ships more, faster, of lower quality. This one cannot — or rather, gaming it requires actually improving code.
- **#3 (Features / Bugs Ratio)** is the lagging quality signal. Pairs with #2: maturity is leading, ratio is lagging.
- **#4 (Lead Time)** is the canonical speed signal. DORA-derived; widely accepted.
- **#5 (Velocity)** is the volume signal. Paired with #3, this is how you separate "the team is shipping more good work" from "the team is shipping more work."
- **#6 (Predictability)** is the variance signal. Per Ch 31 §31.1: "A team that consistently delivers 35 ± 3 points is dramatically more valuable than a team that delivers 50 ± 25 points."

The six fit together as the CEO-defensible answer to "is AI working?" — see [`dashboard-overview.md`](dashboard-overview.md) for the full read.

## The reference executive dashboard (Ch 31 §31.4)

The book provides a specific tile layout:

| Tile | Metric | Direction you want |
|---|---|---|
| Adoption | % of developers active in Claude Code in last 7 days | Rising to ~60–70% then stable |
| Cost | Median Claude Code spend per active developer per week | Stable or dropping per unit of output |
| Speed | Median story-to-production lead time | Decreasing |
| Quantity | 6-sprint rolling velocity | Stable or rising |
| Quality | Features-to-bugs ratio | Rising |
| Maturity | LLM-graded code maturity (team mean) | Stable or rising; never falling >0.5 |
| Predictability | 1 − (σ/µ) of committed vs delivered | Rising toward 0.9+ |
| Slop alerts | Duplication growth, churn rate, test ratio | All flat |

This is the executive-level rollup. It maps onto the six core metrics plus the slop alerts from [`../quality-decay-signals.md`](../quality-decay-signals.md). The team-level dashboard is one level deeper — same six metrics, but per team and with the underlying queries surfaced.

## File layout

```
six-metric-dashboard/
├── README.md                       ← this file
├── dashboard-overview.md           ← how the six fit together; the CEO-defensible read
├── metric-01-token-usage.md
├── metric-02-code-maturity.md
├── metric-03-features-to-bugs.md
├── metric-04-lead-time.md
├── metric-05-velocity.md
├── metric-06-predictability.md
└── (your team's grafana JSON exports live here as you build them)
```

Each metric file has the same structure:

1. **Definition** — verbatim from Ch 31 §31.1 where possible
2. **What it tells you** — diagnostic value
3. **How to instrument** — PromQL / SQL / source data
4. **Thresholds** — healthy / watch / decay
5. **Anti-patterns** — common ways the metric gets gamed or misread

## The cadence

| Surface | Frequency |
|---|---|
| Team standup | Glance at trends (10 seconds, not a discussion) |
| Team weekly retro | Discuss any tile that flipped state |
| Engineering leadership weekly | Review across teams |
| Executive monthly review | The eight-tile rollup |
| Quarterly board review | The story the dashboard tells |

The dashboard is for trends, not point-in-time judgments. A bad week on metric N is not a fire. Two bad months on three of them is the "pull the lever" rule from [`../quality-decay-signals.md`](../quality-decay-signals.md).

## What this dashboard will NOT do

- Will not work without the AI-authorship tagging convention (Ch 31 §31.6).
- Will not work without a 30+ day pre-AI baseline. Capture it now via [`../baseline-measurement-template.md`](../baseline-measurement-template.md).
- Will not work as a per-engineer surveillance tool. Per Ch 31 §31.1: team-level only.
- Will not be useful in the first 6 weeks of operation. Trends require baseline.
- Will not detect every quality issue. Pair with the decay signals.

## Companion artifacts

- [`dashboard-overview.md`](dashboard-overview.md) — how the six fit together
- [`../quality-decay-signals.md`](../quality-decay-signals.md) — the leading indicators that pair with the lagging dashboard
- [`../code-maturity-rubric.md`](../code-maturity-rubric.md) — the rubric for metric #2
- [`../triage-taxonomy.md`](../triage-taxonomy.md) — the seventh metric (off-dashboard)
- [`../baseline-measurement-template.md`](../baseline-measurement-template.md) — pre-rollout baseline
- Ch 31 §31.1, §31.4, §31.7 — sources
