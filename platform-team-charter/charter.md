# Platform Team Charter

The mission, scope, principles, and operating model of the platform team in an AI-native engineering organization.

This document is the foundation. Use it to onboard new platform team members, to align with leadership, and to push back when the team's mission is being eroded by ad hoc requests.

## Mission

The platform team's mission is to make AI-native engineering work at scale for stream-aligned teams.

Specifically: we build, ship, and maintain the harness — the skills, hooks, subagents, MCP servers, observability, cost dashboards, scaffolding tools, plugin marketplaces, and CLAUDE.md / AGENTS.md infrastructure — that lets stream-aligned teams ship faster, more reliably, and more cheaply with AI tooling.

Our customers are the stream-aligned teams in this engineering organization. They're not external customers; their satisfaction and adoption are how we measure success.

## What we ship

The platform team's product surface:

- **Skills library** — canonical patterns engineers and agents invoke for recurring tasks. The most-used product.
- **Hooks library** — pre-commit, pre-merge, and CI hooks that enforce invariants mechanically.
- **Subagents** — specialized review agents (security-reviewer, performance-reviewer, migration-reviewer, etc.) that run on PRs.
- **MCP servers** — integration points between agents and the team's systems.
- **Observability and cost dashboards** — visibility into AI tooling usage, cost, and impact.
- **CLAUDE.md / AGENTS.md scaffolding** — templates, generators, validators for repo-level agent configuration.
- **Migration playbooks** — when the engineering org needs to migrate AI tooling, the platform team owns the playbook execution.
- **Onboarding material** — for new engineers learning the AI-native stack at this company.

We do not ship customer-facing features. We do not ship business logic. Our product is the engineering productivity infrastructure.

## How we work

### We are a product team

The platform team operates with the discipline of a product team:

- We have a named roadmap with quarterly priorities
- We have a backlog with explicit prioritization
- We have user research — talking to stream-aligned teams about what's working and what isn't
- We have launch processes for new harness components — beta, gradual rollout, measurement
- We have retrospectives on what shipped vs. what was planned
- We have a dedicated engineering manager (or staff IC) running the roadmap, not a senior engineer doing it on the side

### We have customers, not stakeholders

Stream-aligned teams are our customers. The vocabulary matters: "stakeholders" implies obligation; "customers" implies optionality. If our customers don't adopt what we ship, that's our problem to solve, not theirs to be educated about.

The customer relationship discipline:

- Quarterly user interviews with engineers from each stream-aligned team
- Feedback channels (a Slack channel, an issue tracker, office hours) that are responsive
- Ride-alongs with stream-aligned engineers using our tools, observing where the friction is
- Adoption metrics tracked per-team, per-tool

### We say no

A real product team has the right to refuse work. We exercise it.

We say no to:
- Requests that would make us a generic "engineer for hire" pool for stream-aligned teams
- Requests that would shift the maintenance burden of feature work to us
- Requests that bypass our roadmap process
- Requests that don't fit our scope (see [`scope-boundaries.md`](scope-boundaries.md))

The discipline is not arbitrary. We have a mechanism for stream-aligned teams to influence our roadmap; we have escalation paths for genuine emergencies; we have explicit "we're not going to do this and here's why" responses for things outside our scope.

### We measure ourselves

The team's success is measured per [`success-metrics.md`](success-metrics.md). Roughly: adoption (are stream-aligned teams using what we ship?), impact (does what we ship measurably change engineering outcomes?), and quality (does what we ship work reliably?).

We do NOT measure ourselves on:
- Lines of code shipped
- Number of skills published (volume isn't quality)
- Engineering hours saved (often unmeasurable; easy to claim, hard to defend)
- "Is the harness still working?" alone (necessary but not sufficient)

## Principles

### 1. The harness is real product work

Every artifact we ship is a product:
- It has a named owner
- It has documentation
- It has a versioning model
- It has a deprecation policy
- It has telemetry
- It has retrospectives when it doesn't work

Treating the harness as "infrastructure" instead of "product" is the dominant failure mode that erodes platform teams. We resist explicitly.

### 2. Adoption is the metric

A skill that nobody uses is not a successful skill. A hook that engineers bypass is not a successful hook. A subagent that produces noise is not a successful subagent.

The bar isn't "we built this." The bar is "stream-aligned teams use this and it makes their work better."

### 3. Stream-aligned teams own their work

We build the harness. We don't build features for stream-aligned teams. When a stream-aligned team needs a feature, they build it; we provide the infrastructure that makes building it tractable.

This boundary is sometimes uncomfortable. A stream-aligned team will ask us to "just build this one thing." We say no, and we explain how the platform we provide makes them able to build it themselves.

### 4. The platform team is the test bed

We use our own harness on our own work. If our skills are bad, we discover it because they fail on our own tasks. If our hooks are noisy, we feel the noise.

This is the dogfooding discipline. It's the most reliable signal that what we ship is real.

### 5. Senior engineers run the team

Per Ch 42 §42.1, the high-value engineer profile in 2026 is "great code reviewer + clear spec writer + harness-comfortable + skeptical without being cynical." Platform engineering at the senior IC level is one of the most leveraged roles in the org.

We hire senior engineers for the platform team. We pay competitively with stream-aligned senior engineering. Career progression is real (see [`platform-staff-engineer-jd.md`](platform-staff-engineer-jd.md)). The platform team is a destination role, not a backwater.

## What we are NOT

To be clear about scope:

- **We are not the on-call team.** Stream-aligned teams own their on-call rotation for their systems. We have on-call only for our own systems.
- **We are not the security team.** Security has its own structure; we partner with security but they're a separate function.
- **We are not the SRE team.** SRE owns reliability of production systems; we own the development-time productivity infrastructure.
- **We are not "the people who say no to AI tooling."** We're the people who make AI tooling work. When a stream-aligned team has an AI tooling need, we work with them; we don't gatekeep.
- **We are not 20% time for senior engineers.** This is its own team with its own engineers.

## Operating cadence

### Daily
- Stream-aligned teams use what we shipped without our involvement (the desired state)
- The team's on-call (limited to our own systems) handles incidents

### Weekly
- Team standup, calibrated for asynchronous review (per Ch 41 §41.1's standup adaptation)
- Office hours for stream-aligned teams (1-2 hours, anyone can drop in)

### Sprint cadence (typically 2 weeks)
- Sprint planning with the next 2 weeks of priorities
- Mid-sprint check on what's tracking
- Demo at end of sprint to interested stream-aligned engineers
- Retro on what worked / didn't

### Monthly
- Adoption review — which artifacts are being used, by which teams, with what feedback
- Roadmap review with engineering leadership
- Cost review — AI tooling spend, vendor relationships

### Quarterly
- Stream-aligned team interviews (rotating set)
- Roadmap planning for next quarter
- Charter review (revisit this document, update if needed)

### Annual
- Comprehensive retrospective
- Headcount and budget planning
- JD and leveling calibration

## Governance

The platform team has the following decision rights:

- **Sole authority** on what we ship (within our roadmap)
- **Strong influence** on AI tooling vendor selection (per `vendor-procurement-runbook/`)
- **Veto** on stream-aligned team requests that would make us a feature-development pool
- **Joint decision** with security on harness components touching auth, payments, regulated data
- **Joint decision** with SRE on observability and reliability tooling

Escalation path for disagreements:
1. Platform engineering manager + stream-aligned team lead direct conversation
2. Platform engineering manager → engineering director or VP
3. VP-level resolution

We don't escalate quickly. Most disputes resolve at level 1.

## What success looks like at 12 months

A year from establishment, the platform team produces:

- A shipped skills library covering the canonical patterns of the engineering org (see `skills/` for shape)
- A hooks and subagents library that catches the seven slop signatures and adjacent failure modes
- Migration playbooks for the AI tooling transitions the org has been through
- Quarterly roadmap reviews with leadership; meaningful adoption metrics; honest reports on what didn't work
- Senior engineers who chose to join because the work is real, not because they were assigned

What success does NOT look like:
- "Everything is fine" — the harness is always evolving; "fine" means we're not tracking the gaps
- Massive volume of artifacts — quality and adoption matter more than count
- "Stream-aligned teams love us" — they shouldn't love us; they should not notice us, because their work is unblocked

## Companion artifacts

- [`scope-boundaries.md`](scope-boundaries.md) — the line between platform and stream-aligned
- [`success-metrics.md`](success-metrics.md) — how we measure
- [`platform-engineer-jd.md`](platform-engineer-jd.md) — who we hire
- [`budget-and-headcount-framing.md`](budget-and-headcount-framing.md) — the leadership conversation
- Ch 42 §42.4 — the source
