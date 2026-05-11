# Reading Order — Week 1 Curriculum for Brownfield Onboarding

The ordered set of files an engineer should read in their first week. Calibrated for engineers joining a team that owns brownfield code.

## The principle

Reading is not optional in brownfield onboarding. The temptation is to skip the reading and start coding; the discipline is to invest the first week in understanding before doing.

The reading order goes from "what's the philosophy" → "what's the program" → "what's the technical scaffold" → "what's our specific situation."

## Day 1 — Philosophy

Goal: understand why brownfield AI work is different from greenfield, and why the discipline matters.

1. **Ch 11** of [_Software Engineering with AI_](https://www.linkedin.com/in/ryanbyrd) by Ryan Byrd — start here. The whole chapter is short (a few pages). Read in one sitting.
2. **Ch 11 §11.6** specifically — the brownfield minimum viable harness. The seven principles you'll be following.
3. **Ch 22 §22.2** — the seven slop signatures. These describe what AI-introduced bugs look like; in brownfield code, they're the failure modes you're guarding against.

After Day 1: you should be able to articulate why "rewrite this with AI" is the wrong instinct.

## Day 2 — The program

Goal: understand the human program around brownfield work.

1. **[`README.md`](README.md)** of this folder
2. **[`30-60-90-day-plan.md`](30-60-90-day-plan.md)** — what you'll be doing in the first 90 days
3. **[`characterize-rewrite-leave-alone-rubric.md`](characterize-rewrite-leave-alone-rubric.md)** — the per-module decision discipline

After Day 2: you should know roughly what your first 30 days will look like.

## Day 3 — The technical scaffold

Goal: understand the harness mechanics.

1. **`starter-kits/legacy-bridge/README.md`** — the brownfield minimum viable harness in code form
2. **`starter-kits/legacy-bridge/MVH_LEVELS.md`** — the maturity rubric you'll be tracking modules against
3. **`starter-kits/legacy-bridge/CLAUDE.md`** — the agent configuration; understand what the agent will and won't do
4. **`starter-kits/legacy-bridge/AGENTS.md`** — the agent's view of the codebase

After Day 3: you should know what scripts and hooks you'll be running, and what they enforce.

## Day 4 — The 8-week worked example

Goal: see how the discipline plays out in practice.

1. **`starter-kits/legacy-bridge/examples/`** — the 8-week worked example of strangling `User#preferences` in a 9-year-old Rails monolith
2. **The accompanying postmortem-style notes** — what was learned at each phase

After Day 4: you should have a concrete model of what success looks like in a real codebase.

## Day 5 — The codebase you actually own

Goal: begin the listening phase of the 30/60/90 plan.

1. **The team's existing CLAUDE.md or AGENTS.md** (whatever exists; if neither exists, that's a finding)
2. **The team's existing README files** — at the repo level and at module level
3. **The team's most recent 5-10 postmortems** — what's gone wrong recently? What's the failure pattern?
4. **The team's deploy cadence and any feature flag tooling** — understanding the release surface
5. **Ad-hoc reading in the modules engineers told you mattered most** (per Day 6-7 of the 30/60/90 plan)

After Day 5: you've started Phase A of the 30/60/90 plan.

## Days 6-7 — Adjacent material

If you finish the above with time remaining, the adjacent material that's worth reading:

- **`incident-postmortem-templates/postmortem-template.md`** — what a good postmortem looks like (you'll be writing them)
- **`junior-trajectory/anti-patterns.md`** — the anti-patterns that affect engineers in brownfield contexts (anti-patterns 4, 5, and 8 specifically)
- **`skip-level-defense/productivity-plateau-message.md`** — the conversation pattern for honest progress communication, which you'll need

## What to AVOID reading first

- **Don't read the codebase yet.** It's tempting; resist. Reading the codebase before the philosophy and program produces the rewrite instinct.
- **Don't read about other teams' modernization wins.** They'll bias you toward optimistic timelines.
- **Don't read vendor demos or success stories.** They calibrate to ideal conditions; your codebase is not ideal.

## What this curriculum will NOT do

- Will not work without uninterrupted reading time. If your first week is dominated by meetings and admin, slip the reading; don't compress.
- Will not work as substitute for actual engineering work. After week 1, the proportion shifts to mostly working with the codebase.
- Will not work for engineers who have already worked extensively in this codebase before this onboarding. They have a different problem set.

## How to verify you've absorbed it

You should be able to answer these questions at the end of week 1:

- Why is "rewrite this with AI" usually the wrong instinct?
- What does it mean to "characterize" a module?
- What's the difference between MVH Level 0 and Level 2?
- What are the seven slop signatures?
- What's our codebase's rough state today (modules, their MVH levels, their owners)?
- Who knows the modules we own most deeply?

If you can't answer most of these, the reading didn't land. Re-read what's relevant; the on-the-ground work depends on these foundations.

## Companion artifacts

- [`README.md`](README.md) — folder overview
- [`30-60-90-day-plan.md`](30-60-90-day-plan.md) — the work the reading prepares you for
- `starter-kits/legacy-bridge/` — the technical scaffold
- Ch 11 — the source
