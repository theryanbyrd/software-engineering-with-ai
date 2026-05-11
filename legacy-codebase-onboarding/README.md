# Legacy Codebase Onboarding — A Program in a Box

The onboarding wrapper around `starter-kits/legacy-bridge/`. Direct implementation of Chapter 11 of [_Software Engineering with AI: A Practical Handbook for the Claude Code Era_](https://www.linkedin.com/in/ryanbyrd) by Ryan Byrd, calibrated for engineers inheriting brownfield codebases.

The legacy-bridge starter kit gives you the harness mechanics: hooks, skills, scripts, MVH levels, an 8-week worked example. This folder gives you the *human* program around it: what to do in the first 30/60/90 days as the new engineer or new tech lead, when to characterize vs. rewrite vs. leave alone, how to resist the rewrite instinct, and how to communicate with leadership about a realistic timeline.

## What's in here

| File | Purpose |
|---|---|
| [`30-60-90-day-plan.md`](30-60-90-day-plan.md) | Day-by-day, week-by-week structure for the engineer or tech lead inheriting the brownfield codebase |
| [`characterize-rewrite-leave-alone-rubric.md`](characterize-rewrite-leave-alone-rubric.md) | The decision rubric for each module: which gets characterization, which gets rewrite, which gets left alone |
| [`first-conversation-with-leadership.md`](first-conversation-with-leadership.md) | The conversation that resets expectations from "AI will modernize this in a quarter" to "we'll bring 1-2 services to MVH Level 2-3 in 90 days" |
| [`anti-patterns.md`](anti-patterns.md) | The brownfield-specific anti-patterns: the rewrite instinct, the false-coverage trap, the comprehensive plan that never ships |
| [`module-status-tracker-template.md`](module-status-tracker-template.md) | The living document tracking every module by MVH level, owner, and status |
| [`reading-order.md`](reading-order.md) | The ordered set of files an engineer should read in week 1 — book chapters, starter kit, this folder |

## The book's framing

> **Rule Zero:** In legacy code, AI writes observation and characterization tests *before* it writes a refactor.
>
> Modern AI works beautifully in clean, well-typed, well-tested codebases. It is a hazard in old enterprise systems. The hazard pattern: AI confidently rewrites a function, the change passes the (sparse) test suite, the silent behavior change shows up six weeks later in a customer escalation.
>
> — Ch 11 opening

The brownfield onboarding program assumes:
- The codebase exists and works (mostly)
- The codebase has been there longer than most of the current engineering team
- Documentation is sparse to absent
- Tests exist but are unreliable as a regression gate
- AI tooling is being introduced; the codebase has not been adapted for it
- Leadership has expectations calibrated by vendor demos, not by Ch 11

The program defends against the dominant failure mode: an engineer or tech lead inheriting the codebase, taking the AI tooling as a license to "finally fix this," and producing a 6-month rewrite project that ships nothing while the team's normal work degrades.

## Who this is for

- **The new engineer** joining a team that owns brownfield code (someone in their first 90 days)
- **The new tech lead** taking over a brownfield service or codebase
- **The engineer transitioning from greenfield** to brownfield work for the first time
- **The hiring manager or director** designing the onboarding for the engineers above

This is the human-program companion to the technical scaffolding in `starter-kits/legacy-bridge/`. Read both.

## Read first

- Ch 11 — the source chapter
- `starter-kits/legacy-bridge/README.md` — the technical scaffold
- `starter-kits/legacy-bridge/MVH_LEVELS.md` — the maturity rubric this program targets
- `starter-kits/legacy-bridge/BROWNFIELD_PLAN.md` — the 90-day plan from the harness side

## What this program WILL do

- Calibrate the engineer's expectations against Ch 11's reality
- Give a structured 30/60/90 day roadmap with checkpoints
- Surface the rewrite instinct and provide a structured push-back
- Build the institutional discipline of "characterize first, refactor second"
- Produce a module-status tracker that lasts beyond any individual engineer's tenure

## What this program will NOT do

- Will not modernize the codebase. That's a multi-year program; this is the start.
- Will not work without leadership buy-in on timeline. Compressed timelines produce shadow rewrites that fail.
- Will not replace the technical scaffolding in `starter-kits/legacy-bridge/`. Use both.
- Will not save you if the codebase is genuinely beyond saving — sometimes the answer is rewrite, but the rubric helps you know when.
- Will not work for engineers without 3+ years of professional experience. The program assumes engineering judgment that brownfield specifically tests.

## How the program fits with adjacent material

| Need | Where to look |
|---|---|
| Technical harness for legacy modules | `starter-kits/legacy-bridge/` |
| Junior engineer development (greenfield-shaped) | `junior-trajectory/` |
| Migration off existing AI tooling stack | `migration-playbooks/` |
| Skip-level conversations about progress | `skip-level-defense/` |
| Promotion criteria that recognize brownfield work | `promotion-and-leveling-rubric/` (this round) |

## The honest timeline

The book is direct on this:

> The brownfield harness takes longer to mature than the greenfield one. Plan for nine to twelve months to feel comfortable, not three. The teams that try to compress this end up with the worst of both worlds: slop in legacy code with no safety net.
>
> — Ch 11 §11.6

The 30/60/90 plan in this folder produces *one or two services* at MVH Level 2-3 in 90 days. Bringing the whole codebase requires multiple iterations across multiple engineers across multiple quarters. The first 90 days is a foothold, not a finish.

## Companion artifacts

- `starter-kits/legacy-bridge/` — technical scaffold (this folder is the human program around it)
- `incident-postmortem-templates/` — for when characterization gaps surface in production
- `skip-level-defense/productivity-plateau-message.md` — the honest progress communication
- Ch 11 — the source
