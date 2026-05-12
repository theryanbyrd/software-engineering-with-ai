# Agent-Ready Issue Pipeline — From Production Signal to Triaged Ticket

The Ch 24 observability-to-issue automation. Direct expansion of the production-to-fix loop in Ch 24 §24, and the chapter takeaway:

> Production signals should auto-create agent-ready issues.
>
> — Ch 24 §24.3

This file is the operational pipeline that makes that real: signal capture, deduplication, triage, agent-ready issue templating, and the read-only MCP discipline that keeps the pipeline safe.

## The book's loop (Ch 24 §24)

The production-to-fix loop for AI-era teams:

```
Production signal (Sentry, Datadog, OTel trace, log, session replay)
└─ Auto-create issue with context (stack trace, trace ID, request shape, recent diff)
└─ Agent reproduces in sandbox
└─ Agent writes failing regression test
└─ Agent writes fix branch
└─ Human review
└─ PR
└─ Canary deploy
└─ Signal closes
```

This pipeline implements the first two arrows: signal → auto-create issue → agent reproduces. The rest of the loop is the standard plan-implement-review flow from Ch 20.

## What makes an issue "agent-ready"

The contract is Ch 19 §19.2. An agent-ready issue is one the agent can implement without a clarifying conversation. The full template lives in Appendix C; the load-bearing sections per Ch 19:

```markdown
## Objective
One sentence describing the desired outcome in user-visible terms.

## Current behavior
What the system does now. Cite files.

## Desired behavior
What it should do. Be concrete.

## Scope
- In: list specific files, modules, or areas
- Out: explicit non-scope items

## Acceptance criteria
- [ ] Behavior X is true (test: `path/to/test.spec.ts::it('does X')`)
- [ ] Behavior Y is true
- [ ] No existing tests fail
- [ ] No new lint or typecheck errors

## Required tests
Concrete test names or scenarios to add.

## Commands the agent will use
- `pnpm verify`
- `pnpm --filter <pkg> test`

## Risk and blast radius
- Touched areas: <list>
- User-facing? Y/N
- Data-affecting? Y/N
- Reversible? Y/N

## Approval-required checkpoints
- After plan, before implementation
- Before any DB migration
- Before any change to <restricted areas>

## Tool / model
Default: Claude Code, Sonnet 4.6. Escalate to Opus 4.7 if architectural questions arise.
```

When the pipeline auto-creates an issue from a production signal, it fills in as much of this template as it can from observability data; the gaps it cannot fill (Desired behavior, Scope, Acceptance criteria) are surfaced as "needs human input" fields that block the issue from moving to "ready for agent" status.

## The pipeline architecture

```
┌──────────────────────────────────────────────────────────────────┐
│  Production Signals                                              │
│  • Sentry error events    • Datadog APM alerts                   │
│  • OTel trace anomalies   • Log-based alerts (Splunk, ELK)       │
│  • Session replay sessions flagged by users                      │
│  • Customer support tickets (confirmed bugs)                     │
└──────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│  Observability MCP (READ-ONLY, enforced)                         │
│  • Pulls stack trace, request payload, recent commits            │
│  • Cannot mutate any production state                            │
└──────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│  Signal Categorization                                           │
│  • Severity (P0 / P1 / P2 / P3)                                  │
│  • Affected component (service, module, route)                   │
│  • Recent-deploy correlation (was there a deploy in last 24h?)   │
│  • AI-authorship correlation (was the deploy ai:authored?)       │
└──────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│  Deduplication                                                   │
│  • Fingerprint by error signature + component                    │
│  • Existing issue → comment with new occurrence                  │
│  • New signature → new issue                                     │
└──────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│  Issue Templating                                                │
│  • Apply agent-ready template (Ch 19 Appendix C)                 │
│  • Fill in observability-derived sections                        │
│  • Flag gaps that need human input                               │
│  • Apply tier (T1 / T2 / T3 per Ch 19 §19.5)                     │
└──────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│  Investigative Prompt Attached                                   │
│  Per Ch 24 §24.1, the "do not edit files yet" prefix             │
└──────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│  Issue posted to tracker                                         │
│  • Labels: ai-ready, signal-source, tier, component              │
│  • Status: "needs human input" until gaps closed, then "ready"   │
└──────────────────────────────────────────────────────────────────┘
```

## The investigative prompt prefix (Ch 24 §24.1)

The book's prompt template, verbatim:

> "Given this stack trace, trace ID `<id>`, request payload shape `<schema>`, and recent deploy diff `<commit range>`, identify the likely root cause. Do not edit files yet. Produce a reproduction plan including: the exact failing assertion, the minimum set of files to read, the proposed regression test, and the rollback path if your hypothesis is wrong."

Per Ch 24 §24.1:

> The "do not edit files yet" clause is critical. It forces the agent to reason about the bug before destroying evidence.

This prompt is attached to every auto-created issue as the "first prompt" — the agent runs investigation before any edit. The agent's investigation output becomes a comment on the issue; the human reviewer approves the reproduction plan before the agent moves to implementation.

Why this matters: an agent that starts editing immediately on production-derived signals will:
- Modify the file the bug is in before fully understanding the bug
- Add defensive code that masks the underlying issue
- Generate a fix that passes the unit tests but doesn't address the actual production failure mode
- In the worst case, modify files the agent shouldn't be touching at all (production config, secrets handling, the failing-test fixture itself)

The investigative-only first pass is the discipline that prevents all of these. It's a load-bearing convention.

## The observability MCP (read-only, always)

Per Ch 24 §24.2:

> The MCPs that matter: read-only access to the observability stack so the agent can pull evidence without escalated privileges.

And Ch 24 §24.3:

> Observability MCPs are read-only by default. Always.

This is non-negotiable. The agent's MCP for Sentry / Datadog / your-observability-tool MUST be configured for read access only. Specifically:

| Tool | Allowed | FORBIDDEN |
|---|---|---|
| Sentry | Read issues, traces, events; download attachments | Mark issues resolved; assign issues; modify alert rules |
| Datadog | Read metrics, traces, logs; query dashboards | Modify monitors; create dashboards; modify SLOs |
| Log aggregation | Read logs; tail; search | Delete logs; modify retention; create alerts |
| Session replay | Read sessions | Modify recording config; export PII without redaction |

Why the strict line: an MCP with mutate permissions on observability tooling is an MCP with mutate permissions on the production-monitoring stack. An agent that can mark its own bugs resolved can also "fix" the signal by suppressing it. An agent that can modify alert rules can disable the alert that flagged its bug.

See also `../agent-autonomy-levels/forbidden-categories.md` — observability mutation is on the forbidden list.

## Sample template — incident → agent-ready issue

The pipeline produces issues that look like this:

```markdown
# [AUTO] NullPointerException in OrderListHandler.parseShippingAddress

## Source signal
- Tool: Sentry
- Issue ID: PROJ-12345
- First seen: 2026-MM-DD HH:MM UTC
- Occurrences (last 24h): 47
- Affected users: 12
- Severity: P2

## Tier
T2 — Inspection (per Ch 19 §19.5)
- Localized bug; reproducible from observability data; well-scoped fix expected

## AI-authorship correlation
- Introducing PR: #5678 (merged 2026-MM-DD by @alice)
- Authorship tag: ai:authored
- Slop signature flags (from slop-detector run on PR): partial-error-handling (warning)

## Current behavior
NullPointerException in `OrderListHandler.parseShippingAddress` at line 42
when `customer.shipping_address` is null. Stack trace:

```
java.lang.NullPointerException
  at com.example.OrderListHandler.parseShippingAddress(OrderListHandler.java:42)
  at com.example.OrderListHandler.handle(OrderListHandler.java:23)
  ...
```

## Reproduction data
- Trace ID: 7f8e9d-...
- Request payload shape: `{"customer": {"id": 1234, "shipping_address": null}, ...}`
- Recent deploy diff: 8a3f9c1..1d2e7b4 (PR #5678)

## Desired behavior
[NEEDS HUMAN INPUT] — typical fix is to handle null shipping address gracefully,
returning a 400 with clear error message OR using default empty address per
business rules. Confirm which is correct.

## Scope
- In: `src/main/java/com/example/OrderListHandler.java`
- Out: schema changes; client-side validation (separate ticket)

## Acceptance criteria
- [ ] No NullPointerException when shipping_address is null
- [ ] [NEEDS HUMAN INPUT] — 400 response with clear error, OR default address used
- [ ] Regression test added in OrderListHandlerTest
- [ ] No existing tests fail

## Required tests
- `OrderListHandlerTest::handlesNullShippingAddress`
- Property-based: parseShippingAddress survives any combination of present/null fields

## Commands the agent will use
- `./gradlew test`
- `./gradlew check`

## Risk and blast radius
- Touched areas: OrderListHandler (handler-level)
- User-facing: Y (changes error response shape if status code changes)
- Data-affecting: N
- Reversible: Y (handler-level change)

## Approval-required checkpoints
- After investigative pass; before implementation
- Before any change to error response shape (user-facing)

## Investigative prompt (run this first)
> Given this stack trace, trace ID 7f8e9d-..., request payload shape
> {"customer": {"id": 1234, "shipping_address": null}, ...}, and recent deploy
> diff 8a3f9c1..1d2e7b4, identify the likely root cause. Do not edit files
> yet. Produce a reproduction plan including: the exact failing assertion,
> the minimum set of files to read, the proposed regression test, and the
> rollback path if your hypothesis is wrong.

## Tool / model
Default: Claude Code, Sonnet 4.6.

---

[bot] This issue was auto-created from a production signal via the
observability-to-issue pipeline. Marked status=needs-human-input until
the [NEEDS HUMAN INPUT] gaps above are closed.
```

The two `[NEEDS HUMAN INPUT]` markers are the gate. The issue cannot move to "ready for agent" status until the human (typically the on-call engineer or the affected component's owner) closes those gaps. This is the discipline that prevents the agent from inventing a "desired behavior" out of an ambiguous signal.

## Deduplication discipline

The pipeline must aggressively deduplicate. The fingerprinting:

1. **Exception type + top 3 stack frames** — the canonical Sentry fingerprint
2. **Component / file path** — exceptions in different files are different issues even if the exception type matches
3. **Request shape signature** — `null shipping_address` is a different fingerprint from `malformed shipping_address`

When a new occurrence matches an existing open issue:

- The pipeline posts a comment on the existing issue with the new occurrence's trace ID and timestamp
- The occurrence counter increments
- If the cumulative occurrence count crosses a threshold (e.g., >100), the severity escalates and a separate alert fires

When a new occurrence matches a *closed* issue (recently fixed):

- A separate "regression" issue is filed, linked to the original
- This triggers the AI-authored regression flow per `../incident-postmortem-templates/`

## Tier assignment automation

The pipeline assigns a default tier (T1 / T2 / T3 per Ch 19 §19.5) using heuristics:

| Heuristic | Default tier |
|---|---|
| Touches auth, billing, payments, RBAC | T3 — never auto-run; human leads |
| Cross-cutting; multiple files; multiple modules | T3 |
| Localized to one file; clear stack trace; reproducible from data | T2 |
| One-line fix; typo; clear semantic bug | T1 |
| Cannot determine from data | T3 (conservative default; human re-tiers) |

Per Ch 19 §19.5:

> The trap most teams fall into is treating T1 work with T2 ceremony — which produces engineer revolt — or treating T3 work with T1 thinness — which produces production incidents.

The automation errs toward higher tier. A misclassified T1-as-T2 produces unnecessary review overhead; a misclassified T2-as-T1 produces a slop-prone agent run on insufficient spec. The cost asymmetry favors over-tiering.

## How this pipeline pairs with the failure triage taxonomy

When an agent run on an auto-created issue fails, the failure feeds the Score / Question / Opportunity / Train triage in [`triage-taxonomy.md`](triage-taxonomy.md). The signal:

- If most failures are **Train**, the pipeline's `[NEEDS HUMAN INPUT]` gates aren't catching enough ambiguity. Tighten the gates.
- If most failures are **Opportunity**, the harness (CLAUDE.md, AGENTS.md, fixtures) is missing context the agent needs to fix the kinds of bugs the pipeline surfaces. Build the missing context.
- If most failures are **Question**, the pipeline is filing bugs that exceed the agent's current capability. Route those to humans automatically (raise the tier).
- If most failures are **Score**, the pipeline is working — invest in raising the autonomy ceiling for that work category.

## Failure-mode catalog

### Issue files but agent never runs

The trap: the pipeline files agent-ready issues, but the team doesn't have an L2+ workflow set up. Issues pile up. The mitigation: pair pipeline rollout with the agent-runner infrastructure. Don't ship the pipeline without the runner.

### Issue files at high volume

The trap: a noisy alert (one error happening 10K times per hour) generates 10K issues. The mitigation: dedup at the source; rate-limit issue creation per fingerprint (e.g., max 1 issue per fingerprint per 24 hours).

### Agent edits files during investigation

The trap: the agent ignores the "do not edit files yet" prefix and starts editing. The mitigation: hook on agent file-write that blocks edits during the investigative phase (the issue's `status=investigating` label triggers the hook).

### Observability MCP gets mutate permissions

The trap: an engineer "for convenience" gives the observability MCP write permissions. Now the agent can mark its own bugs resolved. The mitigation: enforce read-only at the MCP server level; review MCP configs quarterly per `../agent-autonomy-levels/forbidden-categories.md`.

### The investigation output isn't reviewed

The trap: the agent posts its reproduction plan to the issue; nobody reads it; the agent proceeds. The fix lands but doesn't address the right cause. The mitigation: the issue cannot transition from `status=investigating` to `status=implementing` without a human-approved reproduction plan.

### PII in issues from observability data

The trap: production payload data ends up in an auto-created issue, including PII. The mitigation: PII redaction at the pipeline boundary; never trust upstream tools to redact for you.

## What this pipeline will NOT do

- Will not fix bugs. It files agent-ready issues. The agent (in the standard plan-implement-review flow) does the fixing.
- Will not work without the AI-authorship tagging convention (Ch 31 §31.6). The correlation column requires it.
- Will not work without read-only MCPs. The discipline is non-negotiable.
- Will not replace human triage for high-tier issues. T3 issues are filed; humans direct.
- Will not run on incidents currently active. Active incidents go to the incident commander, not the agent queue. The pipeline picks up post-mortem.

## Companion artifacts

- [`README.md`](README.md) — the directory index
- [`triage-taxonomy.md`](triage-taxonomy.md) — the seventh metric: Score / Question / Opportunity / Train
- [`quality-decay-signals.md`](quality-decay-signals.md) — customer-reported defects feed the same pipeline
- `../failed-one-shot-triage/` — the triage discipline this pipeline feeds
- `../incident-postmortem-templates/` — the AI-authored postmortem flow for confirmed defects
- `../agent-autonomy-levels/forbidden-categories.md` — read-only MCP discipline
- Ch 19 §19.2, §19.5, Ch 20, Ch 24 §24.1–§24.3 — sources
