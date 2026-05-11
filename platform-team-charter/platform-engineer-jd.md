# Platform Engineer — Job Description

A template for an IC platform engineer role, calibrated to the AI-native era. This is the L4-equivalent role — senior individual contributor, mid-career, deep on harness work.

For more senior roles, see [`platform-staff-engineer-jd.md`](platform-staff-engineer-jd.md). For the manager role, see [`platform-engineering-manager-jd.md`](platform-engineering-manager-jd.md).

---

# Platform Engineer

## At [Company]

[Company description.]

## The role

You'll join our platform team — a real product team whose customers are the rest of our engineering organization. We build, ship, and maintain the harness that makes AI-native engineering work at scale.

The harness is real product work: skills libraries, hook templates, MCP servers, observability, cost dashboards, CLAUDE.md/AGENTS.md scaffolding tools, plugin marketplaces. We have a roadmap; we ship continuously; we measure adoption; we partner with stream-aligned teams without becoming their feature-development pool.

This is not "infrastructure" or "DevEx" in the legacy sense. The platform team in 2026 is one of the most leveraged engineering roles in the company. We hire senior engineers, we pay competitively with stream-aligned senior engineering, and we provide a real career path through L5+ on this team.

## What you'll do

- **Ship harness components.** Skills, hooks, subagents, MCP servers, dashboards. Each is a product: documented, versioned, owned, with metrics and retrospectives.
- **Talk to stream-aligned teams.** Office hours. Pair-driving sessions. User research. Their adoption is your success metric, so you spend time understanding their work.
- **Maintain what you've shipped.** When something we shipped doesn't work for a team, the platform engineer who shipped it owns the iteration.
- **Contribute to roadmap.** Quarterly priorities. Backlog grooming. Pushback on requests outside scope.
- **Dogfood the harness.** We use our own product on our own work. If our skills are bad, we discover it because they fail on our own tasks.
- **Onboard new engineers** to the harness — both new platform team members and engineers in stream-aligned teams.

## What you'll NOT do

- Build features for stream-aligned teams. We say no a lot; their work is theirs.
- Operate as on-call for stream-aligned services. We have our own (limited) on-call for our own systems.
- Do "DevOps" in the legacy sense. Infrastructure-as-code, deployment pipelines, and SRE work belong to other teams.
- Spend 60% of time in CRM, vendor calls, or admin. This is an engineering role.

## What we're looking for

### Required

- **Real engineering background.** 4+ years shipping production code. Specific stories about specific systems. Comfortable in the languages and stacks we use.
- **Strong code-review intuition.** Per Ch 22 §22.2, can spot the seven slop signatures. Calibrates diff size. Pushes back on AI-generated code that doesn't fit.
- **AI tooling fluency.** Has run productive Claude Code or Cursor sessions on real work. Can articulate what's working and what's not. Has opinions backed by experience.
- **Spec writing.** Can write an agent-ready issue from scratch in 15 minutes. Knows what models need and what they don't.
- **Comfort with bash, hooks, and CI.** Building hooks and CI integrations is part of the work. We don't need a kernel hacker; we do need someone who can write a 50-line bash script that does what it should.
- **Customer empathy.** This role has user research, office hours, and pair-driving. If interacting with engineers about their work sounds like a chore, this isn't your role.
- **Communication discipline.** Documentation matters. We write a lot. The writing is good — clear, tight, honest about limitations.

### Nice-to-have

- Experience as a tech lead or staff engineer in a previous role
- Open-source contributions (especially anything that resembles harness components — Lefthook, pre-commit, custom Git hooks, custom MCP servers, etc.)
- Experience with one or more specific AI tools at a depth (Claude Code, Cursor, Codex, Aider, etc.)
- Background in developer tooling, internal platforms, or developer experience

### What we're NOT looking for

- Engineers who want to "use AI more" without engaging with the platform discipline. The job is building the platform; we use AI as a tool but the work is engineering, not vibing.
- Pure SRE / infrastructure engineers without code-review depth. The work involves code review across many systems.
- Junior engineers. The role is L4-equivalent; we hire senior. Junior engineers can grow into platform via stream-aligned roles first.

## How we interview

5 rounds, ~6 hours of substantive interviewing.

1. **Hiring manager screen** (45 min). Why platform; your background; high-level fit.
2. **Code review with AI tooling** (60 min). Live. We give you a sample PR (with one or more slop signatures); you review with whatever AI tooling you'd normally use. We grade the substance and the AI-tooling fluency.
3. **Harness component design** (~3 hours async). We give you a recurring engineering pain point; you design a harness component (skill, hook, subagent) to address it. Output: design doc + skeleton implementation. We grade design judgment, not whether the code runs.
4. **Customer-empathy conversation** (60 min). One of our engineers plays a stream-aligned team member with a request. You navigate scope, push back appropriately, find the right path. We grade communication and judgment.
5. **Reference and final fit** (60 min). Two senior engineers from the team you'd join.

We do not run a separate "behavioral round." We do not run a "system design from scratch" round (the harness is product work; design conversations happen in context). We do not run more than 5 rounds.

## Compensation

[Your specific numbers]

The comp band matches senior IC engineering at the company. We do not pay platform engineers less than stream-aligned engineers at the same level. The career ladder goes through L6 (Principal Platform Engineer) on this team.

## Career path

Engineers on this team typically progress through:

- **L4 — Platform Engineer** (this role)
- **L5 — Senior Platform Engineer** ([`platform-staff-engineer-jd.md`](platform-staff-engineer-jd.md))
- **L6 — Staff / Principal Platform Engineer**

Some engineers move to engineering management (the platform team's manager role, or stream-aligned EM roles). Some move to stream-aligned senior engineering roles after a few years on platform. Internal mobility is supported.

## Apply if

- You think the harness is the most leveraged work in modern engineering
- You enjoy building tools that other engineers use
- You can articulate why an AI-generated solution is wrong, with specifics
- You want to be evaluated on what stream-aligned teams adopt, not on slide decks

## Don't apply if

- You haven't shipped production code in 3+ years
- You're looking for a path away from coding (this is an IC role; we ship a lot)
- You don't enjoy talking to other engineers about their work
- You think "platform" means "infrastructure" or "DevOps" in the legacy sense
