# Metric 2 — Code Maturity Score (1–10, LLM-Graded)

The keystone metric. The highest-leverage and the highest-investment of the six. Per Ch 31 §31.7:

> LLM-graded code maturity is the highest-leverage metric and the highest-investment.

## Definition

Per Ch 31 §31.1:

> Run a daily or per-PR job that takes the diff, plus a rubric describing what code at each level looks like (1 = junior intern, 5 = competent mid-level, 7 = senior, 10 = staff engineer), and asks a frontier model to score the diff against the rubric with reasoning. Track team-level moving averages.

The full rubric, the validation procedure, and the prompt template live in [`../code-maturity-rubric.md`](../code-maturity-rubric.md). This file is the *dashboard* spec — definition, instrumentation, thresholds, anti-patterns.

## What it tells you

This is the only metric on the dashboard that:

1. Cannot be gamed by shipping more / faster (#3 #4 #5 can)
2. Cannot be gamed by manipulating token usage (#1 can)
3. Cannot be gamed by re-sizing stories (#5 #6 can)

The only way to game this metric is to actually improve code quality. That property is what makes it the keystone. Per Ch 31 §31.1 — paired with metric #3 (features-to-bugs ratio), this is how you distinguish "real productivity gain" from "slop rollout":

> AI rollouts that produce real productivity gains show velocity rising while the ratio in metric (3) stays flat or improves; AI rollouts that produce slop show velocity rising while metric (3) deteriorates.

The maturity score is the *leading* version of that signal. Maturity score drops 1–3 months before the features-to-bugs ratio drops.

## How to instrument

The mechanism is detailed in [`../code-maturity-rubric.md`](../code-maturity-rubric.md). The summary:

1. **Per-PR grading job** — on PR merge, run the LLM grader against the diff
2. **Daily team rollup** — aggregate all of today's PR scores into a team-day mean
3. **4-week moving average** — the actual surfaced metric
4. **Quarterly grader re-validation** — drift check against fresh human-graded gold set

### PromQL — surfacing the rolling average

Assuming each per-PR score is pushed as `code_maturity_score{team, pr_number, authorship_tag}`:

```promql
# Team-level 4-week moving average
avg_over_time(
  avg by (team) (code_maturity_score{team="$team"})
[4w])

# Breakout by authorship tag
avg by (authorship_tag) (
  avg_over_time(code_maturity_score{team="$team"}[4w])
)
```

### SQL — surfacing the rolling average

```sql
SELECT
  date_trunc('week', merged_at) AS week,
  team,
  authorship_tag,
  AVG(score) AS team_week_mean_score,
  AVG(AVG(score)) OVER (
    PARTITION BY team, authorship_tag
    ORDER BY date_trunc('week', merged_at)
    ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
  ) AS team_4wk_moving_avg
FROM code_maturity_scores
WHERE merged_at >= NOW() - INTERVAL '24 weeks'
GROUP BY 1, 2, 3
ORDER BY 1, 2;
```

## Thresholds

Per Ch 31 §31.4's executive dashboard:

> Maturity: LLM-graded code maturity (team mean) — Stable or rising; never falling >0.5

That ">0.5" drop is the watch threshold. Specifically:

- **Healthy:** team mean stable or rising across consecutive 4-week windows
- **Watch:** team mean dropping 0.3–0.5 over a 4-week window
- **Decay:** team mean dropping >0.5 over a 4-week window (matches the book's threshold)
- **Pull the lever:** team mean dropping >0.5 in two consecutive 4-week windows AND two or more other decay signals are red (per [`../quality-decay-signals.md`](../quality-decay-signals.md))

### What "good" looks like in absolute terms

The absolute score depends on your team's pre-AI baseline, but rough anchors:

| Team mean score | Description |
|---|---|
| 4.0–5.0 | Early-stage codebase or one with significant tech debt |
| 5.0–6.5 | Healthy mid-sized engineering team |
| 6.5–7.5 | Mature engineering organization with strong review culture |
| >7.5 | Either staff-engineer-heavy organization or grader drift (re-validate) |

The exact number matters less than the trend. A team that goes from 5.8 to 5.4 has a problem. A team that goes from 5.8 to 6.0 is improving.

## Anti-patterns to avoid

### Trusting an un-validated grader

Per Ch 31 §31.1: "You must validate the LLM grader against human grades on a sample of your own codebase before trusting it." See the full validation procedure in [`../code-maturity-rubric.md`](../code-maturity-rubric.md). Skipping this step makes the metric decorative.

### Showing individual scores

Per Ch 31 §31.1, explicit: "Do not show individual developers their own daily score — show team-level trends and use individual scores for coaching, not rankings." This is non-negotiable; see the trap warnings in [`../code-maturity-rubric.md`](../code-maturity-rubric.md).

### Per-PR scoring without rolling average

The trap: surfacing per-PR scores as the metric. Per-PR scores are noisy (4 to 8 on similar-looking diffs is normal). The metric must be a moving average to be useful. Per-PR scores are useful for outlier review (audit any PR scoring <3) and coaching, not for the dashboard.

### Grader drift undetected

The trap: the grader passed validation in Q1, then never re-validated. By Q4 the grader is off by 2 points and the team has been making decisions on noise. Quarterly re-validation is the discipline.

### Comparing maturity scores across teams without normalization

The trap: Team A has a maturity score of 6.2 and Team B has 5.8. Team A is "doing better." Maybe — or Team A works on a more architecturally clean codebase, or Team A has more staff engineers, or Team A's PRs are smaller and benefit from the length bias of LLM graders. Compare each team to *its own trend* across time. Don't rank teams.

### Setting a maturity-score gate at the team's current mean

The trap: a CI gate that rejects PRs scoring below the team's current mean. Half of all PRs will score below the team mean by definition — they're below average. The gate flaps. Use mutation score (per [`../quality-decay-signals.md`](../quality-decay-signals.md)) as the per-PR gate; use the maturity score as the team-trend signal.

## Companion artifacts

- [`../code-maturity-rubric.md`](../code-maturity-rubric.md) — the full rubric, validation procedure, prompt template
- [`README.md`](README.md) — the six-metric index
- [`../quality-decay-signals.md`](../quality-decay-signals.md) — the leading indicators that pair with this metric
- Ch 31 §31.1, §31.4, §31.7 — sources
