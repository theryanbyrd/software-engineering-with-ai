# Junior Trajectory — A Program in a Box

The 18-month curriculum, anti-pattern catalog, manager playbook, and 6/12/18-month calibration rubric for developing junior engineers in the AI-native era. Direct implementation of Chapter 42 §42.3 of [_Software Engineering with AI: A Practical Handbook for the Claude Code Era_](https://www.linkedin.com/in/ryanbyrd) by Ryan Byrd.

## What's in here

| File | Purpose |
|---|---|
| [`18-month-curriculum.md`](18-month-curriculum.md) | The four phases (review → small features → harness contribution → first solo design) with month-by-month milestones and exit criteria |
| [`anti-patterns.md`](anti-patterns.md) | Specific patterns that produce engineers who never develop, with mitigations |
| [`manager-1on1-playbook.md`](manager-1on1-playbook.md) | Question banks and conversation patterns for the weekly 1:1 cadence with juniors |
| [`calibration-rubric.md`](calibration-rubric.md) | Is this junior on track? Specific signals at 6, 12, and 18 months |
| [`pair-driving-guide.md`](pair-driving-guide.md) | The discipline of pair-driving on agent sessions — the most important hour of the junior's week |

## The book's stance

> The junior hiring case is harder in 2026 than in 2022. The work that used to be where juniors built pattern recognition (typing out CRUD, writing the boilerplate, fixing the lint warnings) is now agent work.
>
> — Ch 42 §42.3

This isn't a reason to stop hiring juniors. It's a reason to hire fewer with more investment per junior, and to invest in a real apprenticeship rather than the rubber-stamp-reviewer pattern that became the dominant antipattern in 2024-25.

The three responses from the chapter:

1. **Hire fewer juniors and pay them more.** The bar is now closer to "can read a diff critically" than "can write a function."
2. **Invest in a real apprenticeship.** Two seniors per junior, rotation through Direction/Architecture/Evaluation, mandatory pair-driving on agent sessions, mandatory ownership of postmortems. Six to nine months before they own real work.
3. **Don't use juniors as rubber-stamp reviewers.** This produces engineers who never built the pattern library that lets them spot slop. By 18 months in, they're harder to retrain than a fresh hire.

The artifacts here are the operational implementation of all three.

## Who this is for

- Engineering managers with juniors on their team (1-3 reports)
- Senior engineers serving as mentors / tech leads
- The junior themselves, with the manager's permission to share
- Heads of engineering designing the org's apprenticeship program

## Read first

- Ch 42 — the chapter itself
- Ch 5 §5.2 — the three bottleneck disciplines (Direction / Architecture / Evaluation) the junior rotates through
- Ch 22 — the seven slop signatures the junior must recognize by month 6
- Ch 13 §13.4 — the canonical skill shape the junior contributes to by month 12

## What this is NOT

- **Not a replacement for university CS or a coding bootcamp.** Assumes the junior has foundational skills (a working Python or TypeScript, basic data structures, can read code). The program is about engineering judgment, not introductory coding.
- **Not for "junior" engineers who are actually mid-career changing fields.** Those engineers move faster; the program is for early-career engineers in the first 18-24 months of professional engineering.
- **Not a checklist.** Following the curriculum mechanically without the manager's judgment produces engineers who can list what they did but can't articulate why. The 1:1 cadence is what produces the judgment.
- **Not infinitely scalable.** Two seniors per junior is the floor. A team trying to onboard six juniors with two seniors total will fail; the seniors will burn out and the juniors won't learn.

## What this WILL do

- Give the manager a structured way to track the junior's development
- Surface anti-patterns before they become permanent
- Give the junior a clear sense of what "on track" looks like
- Give senior engineers a clear sense of their mentorship responsibilities

## What this will NOT do

- Will not turn a poor hire into a good engineer. Calibration at 6 months is honest; the rubric tells you when to course-correct vs. when to part ways.
- Will not work without senior engineers who actually invest. The single point of failure is mentor availability and engagement.
- Will not work in a team that uses juniors as rubber-stamp reviewers (the antipattern). Fix that first.
- Will not protect against burnout, market poaching, or the junior deciding they want a different career. The program is the engineering-development side; the retention work is separate.

## How to use

1. **Manager reads the curriculum and rubric before the junior starts.** No surprises.
2. **Junior is given the curriculum on day one.** Transparency about expectations is part of the program.
3. **Manager runs the 1:1 cadence weekly.** Skipping or shortening the 1:1 cadence is the most common failure mode.
4. **Calibration at 6, 12, 18 months.** Honest assessment. The rubric is designed to surface "this junior needs different support" early enough to act.
5. **Adapt to your stack and team.** The curriculum names patterns; your team has specifics. The manager's job is the bridge.

## Companion artifacts

- `people/jds/` — JD templates that calibrate to the program's outputs
- `people/career-ladder/ic-track-additions.md` — L3-L4 promotion criteria the junior is working toward
- `people/perf-reviews/` — performance review structure that recognizes the work this program produces
- `skills/code-review/SKILL.md` — the canonical review discipline the junior internalizes by month 6
- `benchmarks/` — the work the junior helps maintain by month 18
