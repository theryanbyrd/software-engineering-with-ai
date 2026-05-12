# Metric 6 — Predictability: 1 − (σ/µ)

Per Ch 31 §31.1:

> The single most underrated metric in software engineering.

## Definition

Per Ch 31 §31.1, verbatim:

> 1 − (standard deviation / average) of committed vs delivered story points.

The mathematical formulation:

```
predictability = 1 - (σ / µ)

where:
  µ = mean of (committed_points - delivered_points) across N recent sprints
  σ = standard deviation of (committed_points - delivered_points) across N recent sprints
```

A predictability of 1.0 means the team perfectly hits its commitments every sprint. A predictability of 0.0 means the team's variance equals its mean — the average delivery is consistent with the deviation, which means the team has no real sense of what they can deliver.

Per Ch 31 §31.1:

> A team that consistently delivers 35 ± 3 points is dramatically more valuable than a team that delivers 50 ± 25 points.

The first team has predictability ~0.91; the second is ~0.50. The metric captures the business value of consistency in a single number.

## What it tells you

This metric matters disproportionately because of how downstream functions consume engineering output. Product, sales, customer support, and finance all plan against engineering's roadmap. A roadmap from a high-predictability team is plannable; a roadmap from a low-predictability team is fiction.

In the AI context specifically: predictability often *drops* in the first 90 days of AI rollout as the team adapts to new patterns. Some sprints overshoot (AI surprisingly capable on the work in scope); other sprints undershoot (AI surprisingly bad). This is normal. After 90 days, predictability should recover toward the pre-AI baseline; after 6 months, it should exceed the pre-AI baseline if the rollout is working.

The pattern to watch:

| Pre-AI baseline | First 90 days | Day 90–180 | Day 180+ |
|---|---|---|---|
| 0.70 | 0.55–0.65 (expected dip) | 0.70 (recovered) | 0.80–0.90 (healthy gain) |

A team that doesn't recover after 90 days has a process problem — usually spec quality (the agent is doing too well on well-specified work and disastrously on poorly-specified work, producing high variance).

## How to instrument

The data: your sprint commitment and delivery numbers, per team, per sprint.

### SQL — rolling predictability

```sql
WITH sprint_commitments AS (
  SELECT
    sprint_number,
    team,
    committed_points,
    delivered_points,
    delivered_points - committed_points AS variance
  FROM sprints
  WHERE sprint_end_at >= NOW() - INTERVAL '36 weeks'
),
rolling_stats AS (
  SELECT
    sprint_number,
    team,
    AVG(delivered_points) OVER (
      PARTITION BY team
      ORDER BY sprint_number
      ROWS BETWEEN 5 PRECEDING AND CURRENT ROW
    ) AS avg_delivered,
    STDDEV_POP(delivered_points) OVER (
      PARTITION BY team
      ORDER BY sprint_number
      ROWS BETWEEN 5 PRECEDING AND CURRENT ROW
    ) AS stddev_delivered
  FROM sprint_commitments
)
SELECT
  sprint_number,
  team,
  avg_delivered,
  stddev_delivered,
  CASE
    WHEN avg_delivered = 0 THEN NULL
    ELSE 1 - (stddev_delivered / avg_delivered)
  END AS predictability
FROM rolling_stats
ORDER BY team, sprint_number;
```

### PromQL — if sprint stats are pushed as gauges

```promql
# Predictability over a 6-sprint window (12 weeks at 2-week sprints)
1 - (
  stddev_over_time(sprint_delivered_points{team="$team"}[12w])
  /
  avg_over_time(sprint_delivered_points{team="$team"}[12w])
)
```

## Thresholds

Per Ch 31 §31.4 reference dashboard:

> Predictability: 1 − (σ/µ) of committed vs delivered — Rising toward 0.9+

The calibration anchors:

| Predictability | Description |
|---|---|
| <0.5 | Team has effectively no commitment discipline — every sprint is a guess |
| 0.5–0.7 | Below industry median; common during major transitions or with new teams |
| 0.7–0.85 | Healthy; most teams sit here |
| 0.85–0.95 | Strong; mature team with good sizing and good scope discipline |
| >0.95 | Either excellent OR under-committing — investigate |

The ">0.95 investigate" anchor is important. A team that always hits its commitments may be sandbagging — committing to less than they can deliver to look reliable. This shows up as flat-or-rising velocity *and* very high predictability — and you want to be careful to celebrate it as a win without verifying the team isn't holding back.

- **Healthy:** rising or stable above 0.7
- **Watch:** falling 0.05–0.10 over a 6-sprint window
- **Decay:** falling >0.10 over a 6-sprint window
- **Concern (different):** above 0.95 for multiple quarters — probable under-commitment

## What "predictability is dropping" usually means

In the AI context, the common causes:

1. **Spec quality is highly variable.** Some tickets are agent-ready; others are vague prose. The agent crushes the first and stalls on the second. Variance shoots up. The fix is the Tixie pattern from Ch 19 §19.5 — an AI ticket-writing assistant that levels up spec quality.
2. **Scope creep mid-sprint.** AI capability emboldens the team to take on adjacent work mid-sprint. Some sprints they finish; others they don't. The fix is sprint-scope discipline.
3. **Estimation hasn't been re-calibrated.** The team is still sizing tickets at pre-AI scale. AI-friendly work delivers faster than estimated; AI-dangerous work delivers slower. Re-calibrate.
4. **One or two ICs operating at very different productivity levels.** Aggregate team metric obscures this; per-engineer load distribution might be skewed. Diagnose in 1:1s, never in dashboards.

## Anti-patterns to avoid

### Per-sprint celebration of high predictability

The trap: one sprint of perfect-hit commitment gets celebrated as predictability win. One sprint isn't a signal. Predictability is inherently a rolling metric — you need 6+ sprints to have a reliable number.

### Counting points-completed instead of points-delivered

The trap: stories marked "complete" by the team count toward delivery even if not actually shipped. Predictability looks high; actual delivery rate is lower. Define "delivered" the same way metric #3 defines feature: shipped and live.

### Punishing teams for low predictability

The trap: low predictability becomes a stick. Teams respond by over-committing (gaming the variance) or sandbagging (gaming the average). The metric becomes useless within a quarter. Use it diagnostically, not punitively.

### Treating predictability as the primary metric

The trap: a team optimizes for predictability above all else — they sandbag, refuse stretch goals, never try new things. Their predictability is excellent and their codebase rots. Predictability paired with velocity (#5) and quality (#2 #3) keeps the optimization honest.

### Predictability without sprint commitment discipline

The trap: the team doesn't really commit to a sprint goal — they just put what they think they'll finish in the sprint. The "committed vs delivered" delta is always ~0 by construction. Predictability looks perfect; nobody is actually planning. The mitigation: commit happens at sprint-planning before work begins; the comparison is to that commitment, not to a rolling re-estimate.

### Ignoring the "too high" signal

The trap: 0.97 predictability gets celebrated, year over year. Nobody investigates. Six months later you realize the team has been sandbagging and burning ~30% of their capacity on side projects. Predictability above 0.95 sustained is an audit signal.

## Companion artifacts

- [`README.md`](README.md) — the six-metric index
- [`metric-05-velocity.md`](metric-05-velocity.md) — the volume that this measures the variance of
- [`metric-04-lead-time.md`](metric-04-lead-time.md) — the speed signal that pairs with predictability for "fast and reliable"
- Ch 31 §31.1, §31.4 — sources
