# Metric 5 — Story Points Delivered (Quantity)

The volume signal. Paired with metric #3 (features-to-bugs ratio), this is the explicit slop-vs-win diagnostic per Ch 31 §31.1.

## Definition

Per Ch 31 §31.1:

> Track team velocity and watch the trend, not the absolute number. AI rollouts that produce real productivity gains show velocity rising while the ratio in metric (3) stays flat or improves; AI rollouts that produce slop show velocity rising while metric (3) deteriorates.

The metric is the rolling sum of story points delivered (stories marked done) per team per sprint, surfaced as a 6-sprint moving average.

## What it tells you

Velocity, *in isolation*, is among the easier-to-game metrics on the dashboard. A team can re-size existing stories upward, split work to inflate counts, or rush low-quality work to "done" status. By itself, the number says little.

In *combination* with metric #3, velocity becomes the explicit slop-vs-win discriminator. The book's table (re-stated from [`metric-03-features-to-bugs.md`](metric-03-features-to-bugs.md)):

| Velocity (#5) | Features/Bugs (#3) | Diagnosis |
|---|---|---|
| Rising | Rising | Real productivity gain |
| Rising | Flat | Cautious win — investigate |
| Rising | Falling | **Slop rollout** — generating more, lower quality |
| Flat | Flat | No AI impact yet |
| Falling | Falling | Team problem unrelated to AI |
| Falling | Rising | Shipping less but better (rare) |

That's why velocity is on the dashboard despite its known gameability — its pairing with #3 makes the diagnostic possible.

## How to instrument

The source: your team's story tracker (Jira, Linear, Shortcut, GitHub Projects, etc.).

### SQL — the 6-sprint moving average

```sql
WITH sprint_velocity AS (
  SELECT
    sprint_number,
    team,
    SUM(story_points) AS points_delivered
  FROM stories
  WHERE status = 'done'
    AND completed_at >= NOW() - INTERVAL '36 weeks'
  GROUP BY 1, 2
)
SELECT
  sprint_number,
  team,
  points_delivered,
  AVG(points_delivered) OVER (
    PARTITION BY team
    ORDER BY sprint_number
    ROWS BETWEEN 5 PRECEDING AND CURRENT ROW
  ) AS rolling_6_sprint_avg
FROM sprint_velocity
ORDER BY team, sprint_number;
```

### PromQL — if velocity is pushed as a sprint-end event

```promql
# 6-sprint rolling sum of velocity divided by 6 (sprints typically pushed every 2 weeks)
avg_over_time(
  team_velocity_points{team="$team"}[12w]
)
```

## Thresholds

Velocity is team-specific. There is no industry-wide "good" number — a team's sprint capacity depends on its size, its product surface, its baseline story-size calibration, and what its sprint length is.

The trend, however, is universal:

- **Healthy (pre-AI baseline):** velocity stable across 6 sprints; variance modest
- **Healthy (post-AI):** velocity rising 10–30% over 12 sprints, then stabilizing
- **Watch:** velocity rising while metric #3 stays flat (early sign of slop pattern)
- **Decay:** velocity rising while metric #3 falls (the slop pattern; pull the lever)
- **Concern (different):** velocity rising >50% in 6 sprints — likely a story-sizing change, not actual productivity

The Ch 31 §31.4 reference dashboard tile for "Quantity" is "Stable or rising." That's the right framing — rising is the goal, but stable-with-improving-quality is also a win.

## Anti-patterns to avoid

### Treating velocity as a productivity metric in isolation

The trap most teams fall into. Velocity *only* tells you something useful when paired with quality. Showing velocity without #3 next to it is misleading.

### Cross-team velocity comparison

Velocity numbers are not comparable across teams. Team A delivering 50 points/sprint vs Team B delivering 30 doesn't mean Team A is more productive — they might just size stories differently. Compare each team to its own trend.

### Re-sizing historical stories

The trap: the team realizes its baseline was "low" and starts sizing stories higher. Velocity jumps. Looks like a win; isn't. The mitigation: when story-size estimates change, flag the change on the dashboard and reset the baseline at that point.

### Counting partially-done work as "delivered"

The trap: stories that shipped behind a flag (but flag is off) get marked done. Velocity inflates. Define "done" the same way you define "feature delivered" in metric #3: shipped to production AND the feature is reaching users.

### Counting tech-debt / refactor work the same as feature work

Per metric #3's strict feature definition, refactors and infra changes are not "features." For velocity, this is a finer judgment — refactor work *is* work delivered. The discipline: show velocity broken down by category (feature / bug / refactor / infra / etc.) so the mix is visible.

### Velocity-driven over-commitment

The trap: the team's velocity rises, and the PM commits to more next sprint. The next sprint is over-committed; predictability (metric #6) drops; quality falls. The mitigation: commitment is set against the rolling average, not the peak.

### Story splitting for the dashboard

The trap: engineers learn that more stories = higher velocity, so they split work into more, smaller stories. Velocity rises mechanically; nothing actually changed. The mitigation: track total story-points delivered, not just story count.

## Companion artifacts

- [`README.md`](README.md) — the six-metric index
- [`metric-03-features-to-bugs.md`](metric-03-features-to-bugs.md) — the metric that pairs with this one for slop diagnosis
- [`metric-06-predictability.md`](metric-06-predictability.md) — the variance signal on top of velocity
- Ch 31 §31.1 — source
