# AI Tooling Onboarding Curriculum

The structured curriculum for new engineers joining an AI-native team. Direct implementation of Chapter 44 of [_Software Engineering with AI: A Practical Handbook for the Claude Code Era_](https://www.linkedin.com/in/ryanbyrd) by Ryan Byrd, with cross-references to the certification gates in `agent-autonomy-levels/certification-gates.md`.

The book's framing:

> A new engineer joining an AI-native team should go through a structured onboarding before touching production code. The default week:
>
> - Day 1: Tools installed (Claude Code, IDE plugins, gateway access, SSO). Read the company's CLAUDE.md, the team's AGENTS.md, the Approved Tooling Matrix (Chapter 30), the Do-Not-Automate catalog (Chapter 33), the autonomy ladder (Chapter 32).
> - Day 2: Walk the harness with a senior. Review the skill library, the subagent roster, the hook library. Run a skill end-to-end on a sandbox repo.
> - Day 3: Write an agent-ready issue from scratch on a real backlog ticket. Get it reviewed.
> - Day 4: Run the plan → implement → review loop on a Tier-3 (low-stakes) ticket end-to-end. Open a draft PR. Get it reviewed.
> - Day 5: Run the prompt-injection exercises (Chapter 37). Discuss findings with the team's security lead.
>
> — Ch 44 §44.1

This folder operationalizes that week and extends through the first 30 days, aligning with the L1 certification gate.

## What's in here

| File | Purpose |
|---|---|
| [`week-1-curriculum.md`](week-1-curriculum.md) | Day-by-day for the first week, mapped to Ch 44 §44.1 |
| [`days-8-to-30.md`](days-8-to-30.md) | The next three weeks: real work, deepening fluency, L1 cert sign-off |
| [`reading-list.md`](reading-list.md) | The ordered set of book chapters and internal docs to read in week 1 |
| [`pair-driving-milestones.md`](pair-driving-milestones.md) | The structured pair-driving sessions across the 30 days |
| [`team-norms-and-tribal-knowledge.md`](team-norms-and-tribal-knowledge.md) | What new engineers need to know that isn't in the codebase yet |
| [`l1-certification-checklist.md`](l1-certification-checklist.md) | The explicit checklist for L1 cert sign-off at end of 30 days |
| [`buddy-and-manager-roles.md`](buddy-and-manager-roles.md) | Who does what during onboarding — buddy responsibilities, manager 1:1 cadence |

## How this differs from `legacy-codebase-onboarding/`

| | `legacy-codebase-onboarding/` | This folder |
|---|---|---|
| **Scope** | Engineers inheriting brownfield code | Engineers joining a team that has AI tooling in place |
| **Pace** | 30/60/90 day program; first 30 days are listening | Standard one-week onboarding then 3 weeks ramping |
| **Default codebase state** | Brownfield; harness immature | Greenfield-shaped; harness mature |
| **Autonomy target at 30 days** | L0/L1 (suggesting only) | L1 (per-edit approval); L2 within 60-90 days |
| **First substantive work** | Days 30-45 (after Phase A listening) | Day 4 (Tier-3 ticket end-to-end) |

If your team has AI-mature tooling AND owns brownfield code, both apply. The brownfield onboarding for the legacy modules; this curriculum for greenfield work and general team integration.

## The book's stance on onboarding

Per Ch 44 §44.1:

> By the end of the week, the engineer can ship a small change with senior review and has met the team's review discipline, security stance, and harness expectations.

This is the goal: a productive first week that ends with a real ship. Not "done with training" — meaningfully contributing while still ramping.

The discipline:
- **Day 1 reading** is non-negotiable. The engineer reads CLAUDE.md, AGENTS.md, autonomy ladder, do-not-automate catalog, approved tooling matrix.
- **Day 2 walking the harness** with a senior is the unique-to-AI-native part. The harness has invariants the codebase alone won't reveal.
- **Day 3 agent-ready issue writing** is the practice that makes the rest work. Without spec clarity, the engineer's AI tooling sessions will struggle.
- **Day 4 ship** is the proof point. Real PR, real review, real merge.
- **Day 5 prompt-injection exercises** is the security calibration. Per `prompt-injection-test-suite/`, run all six exercises with the security lead.

Days 8-30 turn this into sustained productivity: 5-15 PRs shipped at L1, the L1 cert earned by day 30.

## Who this is for

- **New engineers joining an AI-native team** — the curriculum itself
- **Buddies** — assigned to walk the new engineer through the curriculum
- **Engineering managers** running onboarding for the new hire
- **Engineering directors / VPE** designing onboarding at the org level
- **Platform team** maintaining the curriculum content as the team's tooling evolves

## Read first

- Ch 44 — the source chapter
- `agent-autonomy-levels/certification-gates.md` — the L1 cert this curriculum targets
- `agent-autonomy-levels/autonomy-ladder.md` — the broader framework
- `agent-autonomy-levels/forbidden-categories.md` — the L5 list the engineer must internalize
- `do-not-automate-catalog/` — the Tier 1/2/3 catalog the engineer must internalize
- `prompt-injection-test-suite/` — the day-5 exercises

## What this curriculum WILL do

- Get a new engineer productive in week 1
- Build the harness fluency that makes AI tooling a productivity multiplier
- Establish the team norms, security discipline, and review practice
- Earn the L1 cert by day 30
- Surface gaps in the team's harness or documentation that only new-engineer eyes catch

## What this curriculum will NOT do

- Will not work for engineers without prior engineering experience (this is L4-equivalent role onboarding, not first-job training)
- Will not work without an assigned buddy. The pair-driving sessions are the highest-leverage part; without a buddy, the curriculum is reading.
- Will not work in cultures that under-invest in onboarding. If a senior engineer's "buddy" duties are unfunded time, the curriculum erodes.
- Will not transfer 1:1 to brownfield contexts. Use `legacy-codebase-onboarding/` for that.

## How this folder fits with adjacent material

| Need | Where to look |
|---|---|
| Certification gates this curriculum targets | `agent-autonomy-levels/certification-gates.md` |
| What "autonomy levels" means for the engineer | `agent-autonomy-levels/autonomy-ladder.md` |
| The catalog the engineer reads on day 1 | `do-not-automate-catalog/` |
| Brownfield-equivalent program | `legacy-codebase-onboarding/` |
| Day 5 prompt-injection exercises | `prompt-injection-test-suite/` |
| Pair-driving structure (junior-specific) | `junior-trajectory/pair-driving-guide.md` |
| Skill library the engineer learns | `skills/` |

## The expected outcome at 30 days

A new engineer 30 days in:

- L1 certified (per `agent-autonomy-levels/certification-gates.md`)
- Has shipped 5-15 small PRs at L1
- Has demonstrated the seven slop signatures recognition (per Ch 22 §22.2)
- Has used 3-5 of the team's skills end-to-end
- Has run the prompt-injection exercises and discussed with security lead
- Knows the team's CLAUDE.md, AGENTS.md, do-not-automate catalog
- Has met the team's senior engineers in pair-driving sessions
- Is starting to be productive at the team's pace

## Companion artifacts

- `agent-autonomy-levels/certification-gates.md` — the gate
- `agent-autonomy-levels/autonomy-ladder.md` — adjacent
- `do-not-automate-catalog/` — adjacent
- `legacy-codebase-onboarding/` — brownfield equivalent
- `prompt-injection-test-suite/` — day 5
- Ch 44 — source
