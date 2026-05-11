# Platform Engineer — Harness

**JD template** for the engineer who builds and maintains the AI engineering harness. This role is mentioned in Appendix H of _Software Engineering with AI_ as one of the readiness scorecard requirements: "Platform team has named harness owner."

---

## About the role

[REPLACE — 2-3 sentences about the team and product]

We're hiring a Platform Engineer to own and evolve our AI engineering harness — the skills library, subagent roster, hook framework, MCP integrations, and the verify command that gates every change. You are the person whose work makes other engineers faster, safer, and more boring (in the good way).

This is a deeply technical role. It is not a "DevRel for AI" role. It is not a "prompt engineer" role. The deliverable is software (hooks, skills, framework code, CI integrations) that other engineers depend on.

## What you'll do [KEEP — adapt to your stack]

- Own the harness for the engineering organization. The skills library, subagent roster, hook framework, CLAUDE.md/AGENTS.md infrastructure, MCP integrations, the verify command, the AI readiness audit, the slop detector, the prompt-injection test suite.
- Triage incoming requests from product teams. Build skills/hooks that are general; document the patterns; refuse to build skills that are too narrow for shared infrastructure.
- Run the quarterly evaluations: model regression tests, prompt-injection test suite, audit scorecards. Report results to the engineering leadership team.
- Partner with security on the agent's security posture. The bash firewall, the protected-paths hook, the credential filter, the egress allow-list — these live in your harness.
- Partner with finance on cost telemetry. Token spend dashboards, per-team cost attribution, model routing policy.
- Mentor the engineers who want to contribute to the harness. The most senior engineers on every team should be capable of shipping a skill or hook; you make that path smooth.

## What we're looking for [KEEP]

**Required:**

- 5+ years of professional software engineering experience, including 2+ years on platform / infrastructure / developer tooling work
- Deep familiarity with at least one production AI coding tool (Claude Code, Cursor, Codex, Copilot Workspace) — including its hook/extension model, not just its prompt interface
- Strong systems thinking. You can reason about token cost vs. throughput vs. accuracy trade-offs across a fleet of engineers.
- Comfortable writing bash, comfortable writing scripts in two or more of [Python, Go, TypeScript, Ruby] depending on the codebase.
- Strong code review intuition (same signal as for the senior IC role).

**Preferred:**

- Public contributions to an open-source AI engineering tool, or a company-internal harness whose patterns you can describe in detail.
- Experience with prompt-injection / red-team testing. You've broken an agent on purpose and patched the harness afterward.
- Familiarity with MCP (Model Context Protocol) implementations and the security model around tokens.
- Background in observability tooling. The engineer who ships a Datadog dashboard for token spend is the engineer we want.

**Things that are NOT requirements:**

- A PhD in NLP. This role does not train models.
- Experience with vector databases or RAG pipelines. The harness work is upstream of those.
- Specific deep expertise in one AI vendor. Vendors change every 18 months; the platform discipline is what we're hiring.

## Compensation and benefits [REPLACE]

[The platform-team harness owner is one of the most retention-sensitive roles per Ch 60 §60.4. Compensation parity with senior IC plus public credit (internal blog, conference talks) is the standard retention play.]

## Interview process [KEEP]

1. **30-minute intro call** with hiring manager.
2. **Take-home harness exercise** (3-4 hours of your time): we give you a small repo with a working code agent setup and three engineering teams' wishlist requests. We want to see how you'd prioritize, what you'd build, what you'd refuse to build.
3. **Architecture conversation** (60 minutes): how would you design the harness for a 200-engineer organization? What goes in shared infrastructure vs. per-team? How do you measure success?
4. **Hook / skill code review** (60 minutes): we share a real hook script (with deliberate flaws) and ask you to review it.
5. **Team interviews** (3 × 45 minutes): two engineers and one cross-functional partner from security or finance.
6. **Reference checks.**

## What we won't do [KEEP]

- We will not ask "what's your AI strategy" as if you're a consultant. We'll ask "what would you build first" with specifics.
- We will not require you to be a public AI thought leader. Many of the best harness engineers have zero Twitter following.

## Application

[REPLACE]

---

## For the recruiter / hiring manager

This is a hard role to fill in 2026. The market is small. The candidates worth hiring are usually employed and not actively looking. Treat the application funnel accordingly: be willing to make multiple touch attempts, be specific about what's interesting in the role, and don't make them grind through a generic "tell me about yourself" loop. The "tell me about a hook you shipped" signal predicts success better than any algorithm question we've ever used.
