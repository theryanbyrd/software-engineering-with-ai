# CI Integration

How to wire the prompt injection test suite into CI and quarterly review.

## The challenge

The six canonical tests require:
- Specific fixtures (issues, PRs, web pages)
- Real agent invocations
- Observation of agent behavior

This makes full CI automation difficult. But partial automation is feasible and valuable.

## What can be automated

### Tests that can run in CI

- **Test 5 (cross-repo exfil)** — fully automatable. Set up a sandbox public/private repo pair; create the issue programmatically; invoke the agent; verify no private content leaked.
- **Test 6 (credential in output)** — fully automatable. Place fixture; invoke agent; grep output for credential patterns.

### Tests that need human-in-the-loop

- **Test 3 (poisoned web page)** — verification is qualitative; subagent review is the closest automation
- **Tests 1, 2, 4** — partially automatable; full automation requires output classification that's currently unreliable

## Suggested CI structure

### Trigger 1 — On agent configuration changes

When PRs touch:
- `CLAUDE.md`
- `AGENTS.md`
- `.claude/settings.json` or equivalent MCP config
- `governance/hooks/` files
- `governance/mcp-permission-config.md`

The CI runs the automatable tests (5, 6) plus a structured prompt to a subagent that reviews the change for prompt-injection-relevant impact.

```yaml
# .github/workflows/prompt-injection-suite.yml
name: Prompt Injection Suite (Config Change)
on:
  pull_request:
    paths:
      - 'CLAUDE.md'
      - 'AGENTS.md'
      - '.claude/**'
      - 'governance/hooks/**'
      - 'governance/mcp-permission-config.md'

jobs:
  automated-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run automatable test cases
        run: |
          # Run tests 5 and 6 in automated mode
          ./runner/run-suite-automated.py --tests 5,6
      - name: Subagent review of change
        run: |
          # Invoke a subagent to assess whether the change might affect injection defenses
          ./runner/subagent-review.py --diff-against main
```

### Trigger 2 — Scheduled (weekly)

Weekly automated run of tests 5 and 6:

```yaml
on:
  schedule:
    - cron: '0 0 * * 1'  # Weekly Monday 00:00 UTC
```

Catches drift in the automation infrastructure (e.g., a token's scope was widened by a different PR; a fixture was modified).

### Trigger 3 — Quarterly (manual)

The full suite, including the human-in-the-loop tests, runs quarterly. This isn't CI; it's a scheduled meeting on the calendar with the security team or platform team.

The interactive runner (`runner/run-suite.sh`) is for this trigger.

## What the automated runner needs

A future `runner/run-suite-automated.py` would:

1. **Programmatic agent invocation** — be able to invoke the team's agent without a human
2. **Sandbox environment** — a sandbox where the test fixtures can exist without polluting production
3. **Output capture** — programmatic access to the agent's output (chat, PR comments, files modified)
4. **Output classification** — heuristic or LLM-based judgment about whether output indicates injection

If your team doesn't have these, the interactive runner is the fallback.

## What CI integration won't catch

CI integration catches:
- Regressions in the team's defensive controls
- Configuration drift
- Some new attack patterns (if the suite is extended)

CI integration does NOT catch:
- New attack patterns the suite doesn't cover
- Subtle output influence (test 3 type failures)
- Vendor-side changes to agent behavior
- Insider threats

For these, the quarterly human review is the discipline.

## Quarterly review structure

The quarterly review:

1. **Run the full suite interactively** (1-2 hours)
2. **Compare results to the previous quarter** — any pass-to-fail regressions are P1 per Ch 37
3. **Review automation results** — has the automated portion been catching anything?
4. **Update the suite** — new test cases for new attack patterns observed
5. **File the results** — for the compliance record

Attendees:
- Platform team representative
- Security lead
- Senior engineer

## Pass-to-fail regression handling

Per Ch 37:

> Treat any pass-to-fail regression as a P1 incident.

When the suite shows regression:
1. **Open a P1 ticket** with the failing test case
2. **Pause any new agent rollouts** until the regression is addressed
3. **Run the response runbook** (per [`response-runbook.md`](response-runbook.md))
4. **Postmortem** per `incident-postmortem-templates/`

The escalation matters because regressions often indicate that a recent change to agent infrastructure has weakened defenses without anyone noticing.

## Tracking results over time

Per `agent-autonomy-levels/autonomy-drift-monitoring.md`'s pattern, the suite's results should be tracked over time:

- Each quarterly run produces a results file
- Aggregate into a dashboard (or simple file) showing pass/fail per test over time
- Any regression triggers investigation

## Common pitfalls

### CI runs too rarely

If CI only runs quarterly, regressions can be in production for 3 months before being caught. The trigger on agent-config changes is critical.

### CI runs too often

If the automated tests run on every PR, they slow PR throughput. Targeted triggers (config changes, weekly schedule) balance protection and velocity.

### Automated tests give false sense of security

Automated tests cover 2 of 6 cases. The remaining 4 require human review. A team that runs automated tests and skips quarterly review has covered the easy cases and missed the hard ones.

### Failing tests are silenced

Engineers add `--skip-test-3` flags when test 3 is producing false positives. Over time, the test is effectively disabled. The discipline: address the false positives by improving the test, not by disabling it.

## Companion artifacts

- [`README.md`](README.md) — overview
- [`response-runbook.md`](response-runbook.md) — when failures happen
- [`extending-the-suite.md`](extending-the-suite.md) — adding new test cases
- `incident-postmortem-templates/` — postmortem after a real incident
- Ch 36, Ch 37 — sources
