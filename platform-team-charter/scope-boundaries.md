# Scope Boundaries — Platform vs. Stream-Aligned

The line where most companies struggle. This document is the source of truth for what the platform team owns and what stream-aligned teams own.

## The principle

Platform team builds the harness; stream-aligned teams build features.

A stream-aligned team is responsible for their service end-to-end: the code, the tests, the deployment, the on-call, the retrospectives. They use the platform team's harness; they don't depend on the platform team to write their code.

## The boundary table

| Concern | Platform owns | Stream-aligned owns |
|---|---|---|
| **The harness itself** (skills, hooks, subagents, MCP servers) | Yes | No |
| **Stream-aligned team's service code** | No | Yes |
| **Cross-cutting infrastructure** (logging, metrics, tracing libraries) | Yes (the libraries) | Yes (using them) |
| **Database schemas and migrations** | No (the migration tooling, yes) | Yes (the schemas themselves) |
| **AI tooling vendor relationships** | Yes | No |
| **AI tooling cost tracking and dashboards** | Yes | No |
| **Per-service CLAUDE.md content** | No (templates, yes) | Yes (the actual content) |
| **Per-service AGENTS.md content** | No (templates, yes) | Yes |
| **Bug fixes in stream-aligned services** | No | Yes |
| **Feature development in stream-aligned services** | No | Yes |
| **On-call for stream-aligned services** | No | Yes |
| **Migration execution across stream-aligned services** | Joint (platform leads playbook; stream-aligned executes in their service) | Joint |
| **Code review** | Platform reviews each other; teaches review discipline | Stream-aligned does its own |
| **Postmortems** | Platform owns its own; helps stream-aligned with structure | Stream-aligned owns its own |
| **Documentation of stream-aligned services** | No (tooling for documentation, yes) | Yes |

## Common boundary disputes

### "Can the platform team just fix this for us?"

The pattern: a stream-aligned team has a bug, a feature need, or an integration challenge. They ask the platform team to handle it because "you have the skills."

The answer: no, but here's the harness component that makes you able to handle it.

If the harness component doesn't exist yet, that's a platform team backlog item — not a "we'll do the fix this week" item. The discipline is to maintain the boundary even when it's slightly slower, because crossing the boundary trains stream-aligned teams to depend on platform for their work.

Exception: if the stream-aligned team is genuinely blocked and the impact is significant, platform may help with execution as a one-time exception, with explicit documentation that this is exceptional. Don't let exceptions become routine.

### "We need to build a feature; can the platform team build the underlying capability?"

The pattern: stream-aligned team needs Feature X. Feature X requires Capability Y. The team asks platform to build Y.

Triage:
- Is Y a harness component (a skill, hook, subagent, MCP server, dashboard)? Then yes, it's platform's scope. Add to roadmap.
- Is Y service-level infrastructure that's specific to the stream-aligned team's service? Then no, the team builds Y itself.
- Is Y something multiple teams will need? Then maybe — work with the team to scope what's truly cross-cutting (which is platform's) vs. team-specific.

### "We don't have time to learn the harness; can platform just take this over?"

The pattern: the harness has a learning curve. Stream-aligned engineers ask platform to operate the harness for them.

The answer: no. The harness has a learning curve; we'll help you up it.

Operating the harness for stream-aligned teams means platform becomes the bottleneck for everything. The whole value of the harness is that it's self-service. We invest in:
- Documentation that's good enough that engineers can self-serve
- Office hours where teams can get help
- Pair-driving sessions for new engineers learning the harness
- Onboarding material that gets new engineers productive in days, not months

We don't operate the harness for stream-aligned teams. That's an anti-pattern.

### "Our service has unique needs that don't fit the standard harness"

The pattern: stream-aligned team finds the standard harness doesn't fit their context. They ask for a customized version.

Triage:
- If the team's needs are genuinely unique to their service, they extend the harness for their service (we provide the extension points; they build the extension).
- If the team's needs reflect a gap in the standard harness that's relevant for other teams, we work together to extend the standard.
- If the team's "unique needs" are actually general engineering pain points the team hasn't recognized as such, we have the conversation about what's standard vs. exotic.

### "This isn't really platform; it's just engineering excellence"

The pattern: someone (often a manager outside the platform team) suggests that "platform" should be broader — engineering excellence, technical practices, cross-team standards.

Push back. The platform team's scope is the harness. Engineering excellence is a broader concern that belongs to senior engineers across the org, the engineering manager community, and the CTO/VPE. Conflating the two erodes the platform team's product focus.

If "engineering excellence" is genuinely a need, it's a different team or a different program — not the platform team.

### "Can the platform team own the AI tooling decision?"

The platform team owns the technical evaluation, the harness compatibility, the vendor relationship, the procurement runbook execution. The platform team strongly influences but does not unilaterally make the decision.

The decision rights:
- **CTO / VPE:** the strategic decision (which model family, which class of tools)
- **Procurement / Legal:** the contractual side
- **Platform team:** the technical evaluation, integration, harness work, and operational ownership
- **Stream-aligned team leads:** input on what's working and what isn't

This is joint, with platform driving the technical evaluation and operational ownership.

## What the boundary is NOT

The boundary is not absolute. Some sensible exceptions:

### One-time crisis support

When a stream-aligned team has a genuine crisis (production outage, regulatory deadline, customer escalation), platform can help directly. This is one-time, scoped, documented.

The discipline: platform helps, then writes the harness component that makes the crisis pattern preventable next time. The crisis is the input, the harness improvement is the output.

### Onboarding new teams

A stream-aligned team that's new — newly formed, newly inheriting work, newly onboarded engineers — gets more platform attention than steady-state teams. Pair-driving sessions, office hours, sometimes even direct help with getting their service onto the harness.

This tapers as the team matures. After 90 days, the team should be self-sufficient.

### Critical bug in the harness affecting their work

If the platform team's harness has a bug that's blocking a stream-aligned team's work, platform fixes it (it's in our scope) and unblocks the team directly if needed.

This isn't a boundary crossing; it's the harness team supporting its own product.

## Communicating the boundary

The platform team's communication discipline:

### When stream-aligned asks for something out of scope

Verbatim response template:

> "That's a feature in your service; that's your team's work to do. The piece of this that's platform scope is [specific harness component], and we [have / are building / will prioritize] that. Once that's available, your team can ship the feature using it."

Don't apologize for the boundary. Don't over-explain. Be specific about what's platform vs. stream-aligned.

### When stream-aligned pushes back on the boundary

> "I understand the request and I know it'd be faster for us to just do it. The reason we don't: if we did this for you, we'd do it for every team, and we'd become the bottleneck for all engineering work in the org. That's a worse outcome than the current one. Let's find the right path: I can help you get unblocked on [specific thing], and our roadmap has [specific item] that addresses the underlying need."

### When platform makes a one-time exception

> "We're going to help you with this directly — one time. The reason this is exceptional: [specific reason]. The standard pattern is [stream-aligned does this]. After this case, we'll be back to the standard."

Document the exception. Track them. If exceptions are frequent, the boundary needs reconsidering or the harness needs investment.

## Boundary review cadence

Quarterly, the platform team reviews:

- What requests came in this quarter that we said no to? Were the no's right?
- What requests came in that we said yes to as exceptions? Did those produce harness improvements?
- Where is the boundary unclear? What needs clarification?
- Are stream-aligned teams successfully self-serving on the harness, or are they still routing things through us?

Adjust the boundary documentation based on this review. The boundary evolves as the harness matures and the stream-aligned teams' capabilities grow.

## What this document will NOT do

- Will not work in companies where leadership doesn't enforce the boundary. If a VP routinely overrides "platform doesn't do feature work," the boundary erodes.
- Will not work as a one-time exercise. The boundary must be enforced repeatedly.
- Will not eliminate friction. Some friction is the price of having the boundary. Without the friction, you have a different (worse) team.

## Companion artifacts

- [`charter.md`](charter.md) — the source of the principle
- [`success-metrics.md`](success-metrics.md) — what the team measures within the boundary
- `migration-playbooks/` — joint work patterns
- Ch 42 §42.4 — source
