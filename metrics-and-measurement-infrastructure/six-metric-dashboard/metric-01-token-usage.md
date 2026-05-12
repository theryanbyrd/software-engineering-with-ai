# Metric 1 — AI Token Usage per Developer

The first of the six metrics from Ch 31 §31.1.

## Definition

Per Ch 31 §31.1:

> Pulled directly from Claude Code's OpenTelemetry export, the Anthropic Analytics API, or your equivalent. Track median (not mean) tokens per active developer per week, broken down by Opus/Sonnet/Haiku. Use this as a leading indicator of adoption and a cost-control input — never as a performance-evaluation metric.

Three things to pin from that definition:

1. **Median, not mean.** The token-usage distribution is heavy-tailed — a handful of engineers running unattended overnight jobs can blow the mean by 5x. The median is the actually-defensible number.
2. **Per active developer.** Not per seat. An active developer is one who used the tool at least once in the period. Inactive seats are an adoption question, not a usage one.
3. **Broken down by model.** The Opus / Sonnet / Haiku split is the routing signal. A team running 80% Opus has a routing problem (Ch 26 §26.2); a team running 80% Haiku may be using AI for low-value work only.

## What it tells you

This metric is dual-purpose: adoption rate (are people using AI?) and cost control (what does the usage cost?). Per Ch 31 §31.1:

> Use this as a leading indicator of adoption and a cost-control input — never as a performance-evaluation metric.

The "never as a performance-evaluation metric" is load-bearing. Engineers who use more tokens are not better engineers. Engineers who use fewer tokens are not worse engineers. The metric tracks tooling behavior, not engineer productivity. If your team's culture or HR system attaches token usage to performance, the metric will be gamed within a quarter and the rest of the dashboard will start lying.

## How to instrument

### Source 1: Anthropic Analytics API (the canonical source)

For Claude Code users on Team / Enterprise plans, the Anthropic Analytics API is the primary source. Per-developer token data with model breakdowns is available via the dashboard and exportable API.

### Source 2: OpenTelemetry export from Claude Code

Claude Code emits OTel traces. Configuration:

```bash
# In your shell rc (per-developer, opt-in)
export OTEL_EXPORTER_OTLP_ENDPOINT=https://otel-collector.example.com:4318
export OTEL_EXPORTER_OTLP_HEADERS="x-team=$TEAM_NAME"
```

The traces include token counts per call, per model, with the team header for routing.

### Source 3: gateway-level capture (if you proxy)

If your team routes Claude API calls through a gateway (LiteLLM, OpenRouter, or your own proxy), the gateway captures token usage by API key, which you tag per developer.

### Computing the metric (PromQL)

Assuming token counts pushed as a counter labeled by developer, team, and model:

```promql
# Median weekly tokens per active developer
quantile_over_time(0.5,
  sum by (developer) (
    increase(claude_tokens_total{team="$team"}[7d])
  )[7d:1d]
)

# Model breakdown (proportion)
sum by (model) (
  increase(claude_tokens_total{team="$team", model="opus"}[7d])
)
/
sum (
  increase(claude_tokens_total{team="$team"}[7d])
)
```

### Computing the metric (SQL)

```sql
WITH weekly_per_dev AS (
  SELECT
    developer,
    date_trunc('week', occurred_at) AS week,
    SUM(input_tokens + output_tokens) AS tokens
  FROM claude_api_calls
  WHERE occurred_at >= NOW() - INTERVAL '8 weeks'
    AND team = $team
  GROUP BY 1, 2
)
SELECT
  week,
  PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY tokens) AS median_tokens,
  PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY tokens) AS p90_tokens,
  COUNT(DISTINCT developer) AS active_devs
FROM weekly_per_dev
GROUP BY 1
ORDER BY 1;
```

## Thresholds

The book quotes Anthropic's own benchmark from Ch 27 §27.1:

> Average cost is around $13 per developer per active day and $150–$250 per developer per month, with costs remaining below $30 per active day for 90 percent of users.

Calibration anchors (translate cost to tokens via the routing mix; per Ch 27 §27.1 pricing):

| Tier | Daily tokens | Monthly tokens (20 active days) | Notes |
|---|---|---|---|
| Low usage | <500K | <10M | Light AI use; mostly chat / explanation |
| Median user | 500K–2M | 10M–40M | Sonnet-default daily driver |
| Heavy user | 2M–10M | 40M–200M | Long-horizon sessions; subagent-heavy |
| Outlier (audit) | >10M/day | >200M/month | Almost certainly Opus drift or retry loops |

- **Healthy adoption pattern:** median rising from week 1 to week 12, then stabilizing
- **Watch:** median falling after weeks 8–12 (engineers churning off the tool)
- **Cost concern:** median >2x the team's calibration anchor, or model mix >30% Opus

## Anti-patterns to avoid

### "Token usage = productivity"

The trap: someone in finance / HR / leadership latches onto token usage as a quantitative productivity signal. It is not. Per Ch 31 §31.1 explicitly. The mitigation: communicate this at the same time you publish the dashboard, in writing.

### Aggregating to the mean

The trap: showing "average tokens per developer" because it's easier to compute. The mean is contaminated by outliers (one engineer running unattended overnight jobs makes the mean look 3x higher than typical usage). Use median.

### Adopting "tokens per PR" as a productivity metric

The trap: tokens-per-PR seems like a productivity signal. It isn't — it correlates with PR complexity, not engineer skill. Tokens-per-merged-PR is a routing / cost-attribution metric (see `../cost-discipline-runbook/cost-attribution-per-pr.md`), not a productivity metric.

### Not breaking out by model

The trap: total tokens look fine, but 60% of those tokens are Opus on routine tasks. The fix is the routing rubric (Ch 26 §26.2). The dashboard must show the model mix or this fix gets missed.

### Showing individual usage publicly

The trap: a per-engineer leaderboard. Engineers will respond by running padding scripts to look "engaged." Token usage data goes on the team-level dashboard; individual data is visible to that engineer and their manager only.

## Companion artifacts

- [`README.md`](README.md) — the six-metric index
- [`metric-02-code-maturity.md`](metric-02-code-maturity.md) — the keystone quality signal
- `../../cost-discipline-runbook/` — the operational cost discipline this metric feeds
- Ch 31 §31.1, Ch 26 §26.2, Ch 27 §27.1 — sources
