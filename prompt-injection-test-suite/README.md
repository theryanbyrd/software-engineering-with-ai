# Prompt Injection Test Suite

The canonical test cases for prompt injection vulnerabilities. Direct implementation of Chapter 37 of [_Software Engineering with AI: A Practical Handbook for the Claude Code Era_](https://www.linkedin.com/in/ryanbyrd) by Ryan Byrd, with the operational runner and CI integration that Ch 37 calls for.

The book's framing:

> Six exercises to run on any new agent rollout. None of them require external tools or specialized skills — they test the defensive controls in your harness.
>
> — Ch 37 opening

This folder turns those exercises into a runnable test suite.

## What's in here

| File | Purpose |
|---|---|
| [`README.md`](README.md) | Overview, the six canonical tests, how the suite works |
| [`test-cases/`](test-cases/) | Each canonical test case as a runnable scenario |
| [`runner/`](runner/) | The harness that executes test cases against the team's agent setup |
| [`ci-integration.md`](ci-integration.md) | How to wire the suite into CI and quarterly review |
| [`response-runbook.md`](response-runbook.md) | What to do when prompt injection is detected (in tests OR in production) |
| [`extending-the-suite.md`](extending-the-suite.md) | How to add team-specific test cases as new failure modes emerge |

## The six canonical test cases

Per Ch 37, six exercises cover the core attack surface:

| # | Test | What it tests |
|---|---|---|
| 1 | The poisoned issue body | Injection through user-submitted issue content |
| 2 | The malicious PR comment | Injection through PR comments asking the agent to run shell |
| 3 | The poisoned web page | Injection through HTML comments on fetched URLs |
| 4 | The poisoned log line | Injection through log content the agent summarizes |
| 5 | The cross-repo exfil attempt | Token scoping for multi-repo agent access |
| 6 | The credential-in-output test | Output filtering for credentials |

Each is implemented as a test case in [`test-cases/`](test-cases/) with:
- The setup (what data, what fixture, what configuration)
- The trigger (what command or scenario invokes the agent)
- The pass criterion (what the agent must NOT do)
- The fail criterion (what indicates the harness is vulnerable)

## Why this suite exists

Per Ch 37 closing:

> Run all six quarterly. Treat any pass-to-fail regression as a P1 incident.

Without a runnable suite, "run quarterly" doesn't happen. Engineers have other priorities; the discipline drifts. This suite makes the discipline executable:
- One command to run all six tests
- CI integration that catches regressions
- A response runbook for when tests fail (or worse, when injection is detected in production)

Per `agent-autonomy-levels/forbidden-categories.md` Category 6 ("Tool configurations where untrusted text reaches production credentials"), prompt injection is the dominant attack vector for agent systems. The defense is keeping untrusted input out of the same runtime as production credentials. This suite tests whether the defense actually holds.

## Who this is for

- **Platform team members** running the suite quarterly
- **Security team** auditing the agent infrastructure
- **Engineers** wondering if their agent setup is exposed
- **VP of Engineering / CTO** for the political artifact ("we run prompt injection tests quarterly; here's the schedule")

## Read first

- Ch 36 — the threat model and required controls
- Ch 37 — the six exercises (this folder's source)
- `agent-autonomy-levels/forbidden-categories.md` — the broader L5 discipline
- `incident-postmortem-templates/` — what to do if an injection ships to production

## What this suite WILL do

- Run the six canonical tests on demand
- Catch regressions when the agent setup changes
- Provide structured output for review and audit
- Build the discipline of quarterly testing
- Surface gaps in the team's defensive controls

## What this suite will NOT do

- Will not catch every prompt injection vulnerability. New attack patterns emerge; the suite needs continual extension.
- Will not protect against bad-faith insiders. The suite tests the defensive harness, not the trust model.
- Will not work without instrumentation. The runner needs to observe agent behavior to determine pass/fail; without telemetry, results are unreliable.
- Will not eliminate the need for human review. The suite is a regression test; senior security review is the authoritative judgment.

## How this suite fits with adjacent material

| Need | Where to look |
|---|---|
| The L5 forbidden categories that injection threatens | `agent-autonomy-levels/forbidden-categories.md` |
| MCP permission boundaries that are part of the defense | `governance/mcp-permission-config.md` |
| Bash firewall as another part of the defense | `governance/hooks/` |
| Subagents that detect suspicious agent behavior | `governance/subagents/` |
| Postmortem template for prompt-injection incidents | `incident-postmortem-templates/` |
| Cost incident runbook (some injection attacks produce cost spikes) | `cost-discipline-runbook/cost-blowup-incident-runbook.md` |

## The threat model in brief

Per Ch 36 §36.1:

> The threat: untrusted text (from issues, PR comments, web pages, log lines, MCP responses, anything an agent reads) gets interpreted as instructions rather than data. The agent acts on the injected instructions instead of the user's task.
>
> The defense: keep untrusted input out of the same runtime as production credentials. Test the defense regularly.

The six canonical tests cover the major entry points. As your agent system grows, new entry points emerge; extend the suite (per [`extending-the-suite.md`](extending-the-suite.md)).

## The discipline this suite enables

### Pre-rollout

Before any new agent rollout (new tool, new MCP server, new permission grant), run the suite. If any test fails, the rollout is blocked until the gap is closed.

### Quarterly

Run the suite quarterly as a regression test. Track results over time. Any pass-to-fail regression is a P1 incident per Ch 37.

### Post-incident

If a prompt injection incident occurs in production, the suite is extended with a test case covering the specific pattern. Future regressions to that pattern are caught.

### CI

For continuous protection, the suite runs in CI on changes to agent configuration (CLAUDE.md, AGENTS.md, MCP configs, hook configs). Catches regressions at the change.

## Companion artifacts

- `agent-autonomy-levels/forbidden-categories.md` — adjacent discipline
- `governance/mcp-permission-config.md` — defensive controls
- `governance/hooks/` — defensive controls
- `incident-postmortem-templates/` — incident response
- Ch 36, Ch 37 — sources
