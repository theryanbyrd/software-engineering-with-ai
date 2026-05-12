# Metric 3 — Features Delivered to Bugs Introduced Ratio

The lagging quality signal. Paired with metric #2 (code maturity), this is how you distinguish a real AI win from a slop rollout.

## Definition

Per Ch 31 §31.1:

> Define both terms precisely. Compute monthly per team. The DORA "change failure rate" metric is the inverse formulation.

The metric is straightforward; the precision is in the definitions.

### "Feature delivered"

Specifically:

- Shipped to production (not staging, not behind a flag that is still off)
- Tied to a story (ticket / issue) with a measurable acceptance criterion
- The story is marked done by the team

**Not** features:

- Refactors with no user-visible behavior change (these are infrastructure)
- Doc updates
- Test additions
- Type-fix sweeps
- Internal tooling changes

The reason for the strict definition: the metric ratios shipped *outcomes* to introduced *bugs*. Outcome work is what the metric counts.

### "Bug introduced"

Specifically:

- A defect attributed to a deploy in the measurement period
- Confirmed (reproducible, real bug — not user error)
- Severity P0 / P1 / P2 (don't include cosmetic P3 — they swamp the metric)

**Not** bugs:

- Tickets later re-classified as feature requests
- Tickets reported pre-deploy but tied to no specific change
- Test flakiness or CI infrastructure issues
- Inherited bugs from before the measurement period (these belong to the prior period)

### The ratio

```
features_delivered_this_month / bugs_introduced_this_month
```

A ratio of 5.0 means 5 features per bug. A ratio of 0.5 means 2 bugs per feature.

## What it tells you

Per Ch 31 §31.1:

> AI rollouts that produce real productivity gains show velocity rising while the ratio in metric (3) stays flat or improves; AI rollouts that produce slop show velocity rising while metric (3) deteriorates.

That single sentence is the entire diagnostic value of this metric. Paired with metric #5 (velocity), the diagnostic table:

| Velocity (#5) | Features/Bugs (#3) | Diagnosis |
|---|---|---|
| Rising | Rising | Real productivity gain — the win story |
| Rising | Flat | Cautious win — investigate before celebrating |
| Rising | Falling | **Slop rollout** — generating more, lower quality |
| Flat | Flat | No AI impact yet |
| Falling | Falling | Team problem unrelated to AI; check process |
| Falling | Rising | Team is shipping less but better quality (rare; often a reorg signal) |

## How to instrument

The data sources:

| Field | Source |
|---|---|
| Features delivered | Story tracker (Jira, Linear, Shortcut, GitHub Projects) — count of stories marked done in the period that match the "feature" definition |
| Bugs introduced | Same tracker — count of bugs created in the period, confirmed, attributed to deploys in the period |
| Deploy → story attribution | Deploy tooling (your CI/CD records what shipped in each deploy; cross-ref to merged PRs and stories) |

### SQL — the basic ratio

```sql
WITH features AS (
  SELECT
    date_trunc('month', completed_at) AS month,
    team,
    COUNT(*) AS feature_count
  FROM stories
  WHERE type = 'feature'
    AND status = 'done'
    AND completed_at >= NOW() - INTERVAL '12 months'
    -- Exclude refactor / docs / infra per metric definition
    AND category NOT IN ('refactor', 'docs', 'infrastructure', 'tests')
  GROUP BY 1, 2
),
bugs AS (
  SELECT
    date_trunc('month', created_at) AS month,
    team,
    COUNT(*) AS bug_count
  FROM stories
  WHERE type = 'bug'
    AND status IN ('confirmed', 'in_progress', 'done')
    AND severity IN ('P0', 'P1', 'P2')
    AND created_at >= NOW() - INTERVAL '12 months'
  GROUP BY 1, 2
)
SELECT
  COALESCE(f.month, b.month) AS month,
  COALESCE(f.team, b.team) AS team,
  COALESCE(f.feature_count, 0) AS features,
  COALESCE(b.bug_count, 0) AS bugs,
  CASE
    WHEN b.bug_count IS NULL OR b.bug_count = 0 THEN NULL
    ELSE f.feature_count::float / b.bug_count
  END AS features_per_bug
FROM features f
FULL OUTER JOIN bugs b ON f.month = b.month AND f.team = b.team
ORDER BY month, team;
```

### Cross-tag with AI-authorship

The diagnostic that makes this metric specifically useful for AI rollouts: bugs broken down by the authorship tag of the introducing PR (per Ch 31 §31.6).

```sql
SELECT
  date_trunc('month', bug.confirmed_at) AS month,
  introducing_pr.authorship_tag,
  COUNT(*) AS bugs_introduced,
  -- Defects per 100 PRs of this authorship type
  100.0 * COUNT(*) / NULLIF((
    SELECT COUNT(*) FROM pull_requests
    WHERE authorship_tag = introducing_pr.authorship_tag
      AND date_trunc('month', merged_at) = date_trunc('month', bug.confirmed_at)
  ), 0) AS defects_per_100_prs
FROM bugs bug
JOIN pull_requests introducing_pr ON bug.introducing_pr_id = introducing_pr.id
WHERE bug.confirmed_at >= NOW() - INTERVAL '6 months'
GROUP BY 1, 2
ORDER BY 1, 2;
```

If `ai:authored` defects-per-100-PRs is significantly above `ai:none`, the harness is failing for that authorship category (per Ch 31 §31.6).

## Thresholds

The absolute ratio varies by team and product maturity. The calibration anchors:

| Ratio | Description |
|---|---|
| <1.0 | More bugs than features — almost always an early-stage or distressed codebase |
| 1.0–3.0 | Below industry median; common during major refactors / migrations |
| 3.0–6.0 | Healthy; most teams sit here |
| 6.0–10.0 | Strong; mature product; effective review and testing |
| >10.0 | Either exceptional team / suspiciously low bug capture |

Trending matters more than absolutes:

- **Healthy:** ratio stable or rising month over month
- **Watch:** ratio falling >20% month over month for one month
- **Decay:** ratio falling >20% for two consecutive months — pair with metric #5 to diagnose
- **Slop pattern:** ratio falling while velocity (#5) rising — pull the lever

## Anti-patterns to avoid

### Loose "feature" definition

The trap: counting every shipped story (including refactors, type fixes, infra) as a "feature." This inflates the numerator and makes the ratio meaningless. Stick to the strict definition above; if you're not sure, exclude.

### Counting bugs by reported date instead of introduced date

The trap: bug reported in September is counted in September's ratio even though it was introduced by a March deploy. This makes the metric a lagging-of-lagging indicator with 6-month lag. Attribute bugs to their introducing deploy / commit / month.

### Counting all severities equally

The trap: P3 bug ("button is 2 pixels off") counts the same as P0 ("payment processing broken"). The metric drowns in noise. Filter to P0 / P1 / P2.

### Ignoring inherited bugs

The trap: counting all "bugs marked introduced this month" without verifying the introducing commit. Sometimes a bug was latent for 18 months and only surfaced now. That's not a current-period quality signal; it belongs in the period it was introduced (if known) or excluded.

### Conflating "more rigorous bug intake" with "more bugs"

The trap: the team starts being more disciplined about logging real bugs. The ratio drops. Looks like decay; isn't. The mitigation: pair this metric with revert rate and customer-reported defects from [`../quality-decay-signals.md`](../quality-decay-signals.md). If those are flat while this drops, the change is in intake discipline, not in quality.

### Comparing ratios across teams without context

The trap: Team A has a ratio of 5.0 and Team B has 8.0. Team B is "doing better." Maybe — or Team B is on a less-trafficked product surface, or Team A is doing more risky work (database migrations, auth changes), or Team B doesn't bother filing P2 bugs. Use the ratio for trend within a team, not for cross-team ranking.

## Companion artifacts

- [`README.md`](README.md) — the six-metric index
- [`metric-02-code-maturity.md`](metric-02-code-maturity.md) — the leading version of this signal
- [`metric-05-velocity.md`](metric-05-velocity.md) — the metric this pairs with for the slop-vs-win diagnostic
- [`../quality-decay-signals.md`](../quality-decay-signals.md) — revert rate, customer defects (related lagging signals)
- Ch 31 §31.1, §31.6 — sources
