# Platform Team Charter

The platform-team-as-product-team charter. Direct implementation of Chapter 42 §42.4 of [_Software Engineering with AI: A Practical Handbook for the Claude Code Era_](https://www.linkedin.com/in/ryanbyrd) by Ryan Byrd:

> Platform teams grow. The harness is real product work — skill libraries, hook templates, MCP servers, observability, cost dashboards, CLAUDE.md/AGENTS.md scaffolding tools, plugin marketplaces. Budget this as a team, not as 20% time.

This folder is the operational charter, JDs, scope boundaries, budget framing, and success metrics for treating the platform team as a real product team — not as the "infrastructure" backwater of pre-AI engineering.

## What's in here

| File | Purpose |
|---|---|
| [`charter.md`](charter.md) | The platform team's mission, scope, principles, and operating model |
| [`scope-boundaries.md`](scope-boundaries.md) | What platform owns vs. what stream-aligned teams own — the line where most companies struggle |
| [`platform-engineer-jd.md`](platform-engineer-jd.md) | Job description for IC platform engineers |
| [`platform-staff-engineer-jd.md`](platform-staff-engineer-jd.md) | Job description for senior IC platform engineers (L5+) |
| [`platform-engineering-manager-jd.md`](platform-engineering-manager-jd.md) | Job description for the platform team's engineering manager |
| [`budget-and-headcount-framing.md`](budget-and-headcount-framing.md) | The "this is a team, not 20% time" conversation with finance and leadership |
| [`success-metrics.md`](success-metrics.md) | How the platform team's value is measured and reported |
| [`case-studies.md`](case-studies.md) | "Platform team built this; here's what shipped" — calibration examples for what the team produces |

## The book's stance

The chapter is direct on this:

> Platform teams grow. The harness is real product work — skill libraries, hook templates, MCP servers, observability, cost dashboards, CLAUDE.md/AGENTS.md scaffolding tools, plugin marketplaces. Budget this as a team, not as 20% time.

The two most common failure modes:

1. **Treating platform as 20%-time.** A few senior engineers maintain harness "when they have time." They don't have time. The harness decays. Stream-aligned teams build their own ad-hoc tools. The codebase fragments.

2. **Treating platform as infrastructure (cost center).** The team is staffed but evaluated on "is everything still up?" rather than "are we shipping things stream-aligned teams use?" Engineers leave for stream-aligned teams where promotion velocity is faster.

The charter encoded here addresses both: platform is a real team with real product, and its product is the harness that makes the rest of engineering productive.

## Who this is for

- **VP of Engineering or CTO** structuring the engineering org for AI-native operations
- **Heads of platform / infrastructure / DevEx** writing their charter or arguing for budget
- **Hiring managers** trying to attract senior engineers to platform roles
- **The platform team itself** — the artifacts here are what your team operates from

## Read first

- Ch 42 §42.4 — the source
- `migration-playbooks/` — the platform team's role in cross-team migrations
- `governance/` — adjacent content the platform team often owns
- `skills/` — the platform team's primary product surface

## What the charter WILL do

- Establish the platform team as a product team with named scope, deliverables, and success metrics
- Give hiring managers a credible JD that attracts senior engineers
- Make the budget conversation reproducible (instead of arguing for headcount each quarter)
- Surface the boundary disputes between platform and stream-aligned teams before they become political problems
- Provide success metrics that survive engineering reorganizations

## What the charter will NOT do

- Will not work in companies where leadership genuinely doesn't believe platform is product work. Cultural alignment is upstream.
- Will not save a platform team staffed entirely with junior engineers. Senior platform engineers are the team's core asset.
- Will not eliminate friction with stream-aligned teams. Some friction is healthy; some platform-team-vs-stream-team disputes resolve over months.
- Will not work without a credible product manager or staff engineer running the team's roadmap.

## How this folder fits with adjacent material

| Need | Where to look |
|---|---|
| Skills library (the team's primary product) | `skills/` |
| Hooks library | `governance/hooks/` |
| Subagent library | `subagents/` |
| Migration playbooks the platform team executes | `migration-playbooks/` |
| Platform team's own promotion criteria | `promotion-and-leveling-rubric/` (this round) |
| Onboarding for new platform engineers | (referenced but not yet built — adjacent to `legacy-codebase-onboarding/`) |

## The core idea, one paragraph

The platform team's product is the harness — the skills, hooks, subagents, MCP servers, dashboards, scaffolding, and onboarding material that makes AI-native engineering work for stream-aligned teams. The harness is shipped continuously, with named owners, with metrics, with retrospectives. Stream-aligned teams are the customers; their adoption and satisfaction is the platform team's success metric. The platform team has its own roadmap, its own promotion criteria, its own JDs. It is not a side project of senior engineers; it is a team with the same operational discipline as any product team.

## Companion artifacts

- `migration-playbooks/` — operational playbooks for cross-team work
- `governance/` — content the platform team often owns
- `skills/` — the team's primary product
- Ch 42 §42.4 — source
