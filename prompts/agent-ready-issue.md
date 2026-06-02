# Pattern: Agent-Ready Issue

**When to use:** Delegating a discrete unit of work to an agent. An agent-ready issue is
a structured ticket the agent can implement *without a clarifying conversation* — "the
most underrated artifact in AI-assisted development and the single biggest determinant of
outer-loop success" (Ch 19).

**Template:**

```
# <imperative title>

## Context
<why this exists; the user-visible behavior or bug; link the trace/fixture>

## Tier
T1 (freely delegable) | T2 (inspection required) | T3 (do-not-automate from review)

## Acceptance criteria
- [ ] <observable behavior 1>
- [ ] <observable behavior 2>
- [ ] verify passes (lint + typecheck + tests)

## Relevant files / contracts
- <path> — <why it matters>
- <contract/schema/interface the change must honor>

## Edge cases that must be handled
- <null / empty / timeout / concurrency / auth>

## Out of scope
- <explicitly what NOT to touch — bounds the blast radius>

## Test plan
<which tests prove the acceptance criteria; new tests required>
```

**Notes:** Match depth to the work — thin tickets for trivial work, thick for complex
(Ch 19 names "every ticket at the same depth" as a top failure mode). The canonical
fill-in template is [`../templates/agent-ready-issue.md`](../templates/agent-ready-issue.md)
(Appendix C).

**References:** Ch 19 (Writing Agent-Ready Issues), Appendix C.
