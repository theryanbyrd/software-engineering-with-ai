# Senior Software Engineer (Architecture)

**JD template** for an engineer with depth in the Architecture discipline — translating Direction into a reliable system through encoded constraints. From Ch 5 §5.2.

---

## About the role

[REPLACE — 2-3 sentences about the team]

We're hiring a Senior Engineer with depth in **Architecture**: the discipline of translating Direction into a reliable system. Performance budgets (latency, uptime, graceful degradation), safety requirements (privacy, security, compliance), and the constraints that prevent the team from accidentally breaking things as they move fast.

In 2026, Architecture's distinctive value is recognizing where AI is weak (data complexity, infrastructure interactions, novel cross-system reasoning) and **protecting those areas with explicit constraint** — encoded into hooks, lints, contracts, schemas, CODEOWNERS, and ADRs.

## What you'll do [KEEP]

- Own the architecture of one or more major systems on the team's surface. ADRs, system diagrams, interface contracts, performance budgets.
- Translate emerging product needs into the constraint surfaces that make the systems safe to evolve quickly: lint rules, schema validators, hooks, CODEOWNERS routes.
- Identify where AI is weak in our domain and design protective scaffolding around those areas. The handbook calls this "encoding constraints into hooks, lints, contracts, schemas, CODEOWNERS, and ADRs."
- Partner with the platform team on harness components that emerged from architectural needs.
- Lead architecture-with-AI conversations: how would we design this system, given AI tooling? Which boundaries matter? Which would we have drawn differently in 2022?
- Mentor more junior engineers on the discipline of architecture. Many engineers in 2026 want to write more code; the architecture-shaped contribution is the one that compounds.

## What we're looking for [KEEP]

**Required:** Senior IC AI-native baseline PLUS:

- Demonstrated experience designing and shipping complex systems with explicit constraint surfaces (schemas, contracts, lint rules, ADRs).
- Strong system-level reasoning. You can read a stack trace and identify which boundary failed.
- Comfort writing infrastructure-as-code, hooks, lint rules, contract validators — not just application code.
- A concrete worked example of where AI tooling produced a problem and an architectural-constraint surface (lint rule, hook, schema validator) prevented its recurrence.

**Preferred:**

- Background in distributed systems, data infrastructure, security engineering, or any domain where the cost of an architectural mistake is high.
- Experience writing ADRs that other engineers actually read.

## Interview process [KEEP]

1. Intro call (30m).
2. **Architecture conversation** (90 minutes): a system design problem with explicit AI tooling in the room. We're looking at the constraint surfaces you propose, not just the boxes-and-arrows.
3. **Constraint design exercise** (60 minutes async): given a real (anonymized) bug from production, design the smallest constraint surface that would have prevented it.
4. PR review exercise.
5. Team interviews.
6. References.

## What we won't do [KEEP]

- We won't accept "I'd use kubernetes" as an answer. We're testing whether you understand the trade-offs.

## Application

[REPLACE]
