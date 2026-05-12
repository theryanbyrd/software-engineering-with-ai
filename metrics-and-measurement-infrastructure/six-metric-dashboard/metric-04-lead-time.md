# Metric 4 — Time from User Story to Production (Lead Time)

The canonical speed signal. DORA-derived, with one specific modification per Ch 31 §31.1.

## Definition

Per Ch 31 §31.1:

> DORA's "lead time for changes" with a small modification: measure from when the story enters the in-progress column to when the related code is in production and the feature flag is on. Median, not mean.

The DORA standard is "from first commit to production." The book's modification is to start the clock when the story enters in-progress and end when the feature flag is on. Two reasons:

1. **First-commit start time understates lead time** when the engineer is exploring the codebase or running an agent in plan mode (no commits) for the first hour. The story-enters-in-progress timestamp captures that.
2. **In-production-with-flag-on end time understates "delivered"** when teams ship code dark for days before flipping. A feature in production but not flag-flipped is not delivered to users; it's deployed.

The combination — earlier start, later end — is a slightly more punitive lead-time measurement than DORA standard. It's the right one for AI-era teams because both endpoints align better with user-perceived speed.

## What it tells you

Lead time answers "how long does it take to get an idea from approved to live?" In AI-era teams it specifically answers:

- Where the bottleneck sits — implementation, review, deploy, flag-flip
- Whether AI assistance is moving the implementation bar without moving the rest
- Whether process overhead (review, deploy, flag-flip) is now the bottleneck

The common pattern in AI-adopting teams: implementation time drops 30-50%, but review time rises 200-400% (per Faros AI data cited in Ch 31 §31.3), and overall lead time only improves 5-15% (per Ch 31's A/B framework expected outcome).

## How to instrument

The data sources:

| Phase | Start | End |
|---|---|---|
| In-progress | Story moves to in-progress column | First commit on the story's branch |
| Implementation | First commit | PR opened |
| Review | PR opened | PR merged |
| Deploy | PR merged | Production deploy includes commit |
| Flag-flip | Production deploy | Flag turned on (if behind a flag) |

### Story tracker → first commit

Most story trackers fire webhooks on column changes. Link story ID to the branch name (convention: `story-1234-foo` or PR description references `STORY-1234`).

### PR / git → deploys

CI/CD logs the commit SHA at each deploy. Cross-reference: PR merged commit → deploy that included it → deploy timestamp.

### Flag-flip data

Most feature-flag systems (LaunchDarkly, Split, Statsig, ConfigCat, in-house tooling) emit flag-toggle events. Cross-reference: PR description mentions flag ID → first flag-on event for that flag.

### SQL — the lead time calculation

```sql
WITH story_timeline AS (
  SELECT
    story_id,
    team,
    MIN(CASE WHEN event = 'in_progress' THEN occurred_at END) AS in_progress_at,
    MIN(CASE WHEN event = 'first_commit' THEN occurred_at END) AS first_commit_at,
    MIN(CASE WHEN event = 'pr_opened' THEN occurred_at END) AS pr_opened_at,
    MIN(CASE WHEN event = 'pr_merged' THEN occurred_at END) AS pr_merged_at,
    MIN(CASE WHEN event = 'deploy_to_prod' THEN occurred_at END) AS deployed_at,
    MIN(CASE WHEN event = 'flag_on' THEN occurred_at END) AS flag_on_at
  FROM story_events
  WHERE occurred_at >= NOW() - INTERVAL '12 weeks'
  GROUP BY 1, 2
)
SELECT
  date_trunc('week', flag_on_at) AS week,
  team,
  PERCENTILE_CONT(0.50) WITHIN GROUP (
    ORDER BY EXTRACT(EPOCH FROM (flag_on_at - in_progress_at))
  ) / 86400 AS median_lead_days,
  PERCENTILE_CONT(0.90) WITHIN GROUP (
    ORDER BY EXTRACT(EPOCH FROM (flag_on_at - in_progress_at))
  ) / 86400 AS p90_lead_days,
  -- Phase breakdown
  PERCENTILE_CONT(0.50) WITHIN GROUP (
    ORDER BY EXTRACT(EPOCH FROM (pr_opened_at - first_commit_at))
  ) / 3600 AS median_implementation_hours,
  PERCENTILE_CONT(0.50) WITHIN GROUP (
    ORDER BY EXTRACT(EPOCH FROM (pr_merged_at - pr_opened_at))
  ) / 3600 AS median_review_hours,
  PERCENTILE_CONT(0.50) WITHIN GROUP (
    ORDER BY EXTRACT(EPOCH FROM (deployed_at - pr_merged_at))
  ) / 3600 AS median_deploy_hours
FROM story_timeline
WHERE flag_on_at IS NOT NULL
GROUP BY 1, 2
ORDER BY 1, 2;
```

The phase-breakdown columns are critical. If the median lead time is unchanged but implementation hours dropped 50% and review hours rose 200%, the AI rollout *did* speed up implementation; the review bottleneck is the new constraint.

## Thresholds

DORA's reference distribution for "elite" / "high" / "medium" / "low" performers per the State of DevOps reports:

| Performer tier | Lead time |
|---|---|
| Elite | <1 day |
| High | 1–7 days |
| Medium | 7–30 days |
| Low | >30 days |

The book's modification (story-enters-in-progress to flag-on) shifts these slightly higher than the DORA standard. Calibration anchors:

- **Healthy:** median lead time stable or decreasing; below team's pre-AI baseline
- **Watch:** median rising 10–25% month over month
- **Decay:** median rising >25% for two consecutive months
- **Bottleneck investigation:** any single phase >50% of total lead time

### What the phase breakdown should look like

For a healthy AI-era team on T2 / T3 work:

| Phase | % of lead time |
|---|---|
| In-progress → first commit | <15% |
| Implementation | 25–40% |
| Review | 30–50% |
| Deploy | <5% |
| Deploy → flag-flip | 5–25% (varies by rollout strategy) |

The review phase being the largest is normal for AI-era teams. Per Ch 31 §31.3, that's where the industry signal shows the biggest shift.

## Anti-patterns to avoid

### Using mean instead of median

The trap: a few outlier stories that took 6 months drag the mean to 30 days while the median is 5 days. Mean is useless for lead time; use median throughout.

### Counting only the implementation phase

The trap: "implementation took 2 hours" gets celebrated; meanwhile the PR sat for 5 days in review and shipped 3 days after that. The metric covers the full pipeline; partial measurements are misleading.

### Excluding stories that are blocked

The trap: filtering out "blocked" stories because they're "not the team's fault." A high blocked-rate IS the team's signal — about dependencies, about external coordination, about scope. Include them; if blockage time is dominating, that's worth knowing.

### Gaming the start time

The trap: engineers learn that "in progress" starts the clock, so they delay moving stories to in-progress. The mitigation: the manager checks the column-state changes during 1:1s. If stories spend >3 days in "ready" before moving to "in progress," the team is gaming the metric.

### Gaming the end time

The trap: counting "PR merged" as the end time, so engineers merge before deploying. The fix is in the definition: the book specifies "in production and the feature flag is on." Implement that endpoint, not the convenient one.

### Ignoring the phase breakdown

The trap: aggregate lead-time number is your only insight. You can see the metric drop without seeing *why*. The phase breakdown tells you whether AI is helping (implementation hours) or whether the win is being eaten by review time.

## Companion artifacts

- [`README.md`](README.md) — the six-metric index
- [`metric-05-velocity.md`](metric-05-velocity.md) — the volume signal paired with lead time
- [`../quality-decay-signals.md`](../quality-decay-signals.md) — review-time-per-line, which decomposes the review phase
- Ch 31 §31.1, §31.3 — sources
