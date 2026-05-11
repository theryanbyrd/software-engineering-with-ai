---
name: observability-change
description: Use when adding or modifying metrics, logs, traces, or alerts in a code path. Adds telemetry consistent with the team's existing observability stack. Does NOT introduce a new observability tool or pattern; matches what's there.
allowed_tools: Read, Edit, Write, Bash, Grep
---

# Observability change

## When to use this skill

The user asks to add metrics, logs, traces, or to change what's already emitted. Examples: "instrument this endpoint," "add tracing to the order pipeline," "we need a metric for cache hit rate."

## Procedure

1. **Read existing observability in the same module.** What's the metric library? What's the log format? Are there structured-logging conventions? Is there a tracing framework already?
2. **Identify the right granularity.** A new metric is justified when:
   - It answers a question we cannot answer with existing telemetry
   - The cardinality is bounded (no per-user metrics, no high-cardinality labels)
   - The team has agreed it should be in the SLO/dashboard
3. **For logs:** match the existing format (JSON with specific fields, or text with specific patterns). Use the team's logger, not `print` or `console.log`.
4. **For metrics:** use the team's metric library. Follow the naming convention (`<service>_<noun>_<unit>` or whatever the team uses).
5. **For traces:** use the team's tracing library. Add spans at meaningful boundaries: external calls, expensive computation, error paths.
6. **For alerts:** define the alert in the team's alert-as-code system (if any). Include: severity, runbook link, rate threshold, evaluation window.
7. **Test:** ensure the new telemetry actually fires. Add a test that asserts the metric/log/span is emitted.

## Output

```
## Observability change

**What's added:**
- Metric: `<name>` — <description> — labels: <list>
- Log: at `<file>:<line>` — fields: <list>
- Trace: span `<name>` in `<file>:<func>`

**Cardinality:** <bounded — list of label values, or unbounded justification>

**Storage cost estimate:** <if metric, rough events/min × retention>

**Dashboard updates needed:** <list, or "none">
**Alert updates needed:** <list, or "none">

**Tests added:** path/to/test
```

## Forbidden

- Do not introduce a new observability tool without explicit team approval. If the team uses Datadog, do not add OpenTelemetry. If they use OTel, do not add a custom metric library.
- Do not emit high-cardinality labels (user_id, request_id, full URL with query string) into metrics. Logs/traces are fine; metrics are not.
- Do not log secrets, PII, or full request bodies. Sanitize.
- Do not change the log format wholesale. Match what's there.
- Do not add an alert without a runbook.

## References

- The codebase's observability conventions doc (if exists)
- Chapter 38 §38.x — observability for AI-authored code
