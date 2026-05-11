# The Cursor migration mandate that almost broke the team

## Setting

A 70-engineer SaaS company, US-based, with a mature engineering culture. Two years on Cursor with significant in-team investment — `.cursorrules` files per repo, custom rule libraries, deep integration into individual senior engineers' personal workflows.

## Situation

The CFO had reviewed the AI-tooling line item and concluded the company was paying for two overlapping tools. The VP of Engineering, under pressure to show cost discipline, agreed to consolidate from Cursor to Claude Code.

The migration was mandated over 30 days. No grace period, no parallel-use exception, no investment in migrating the `.cursorrules` files to CLAUDE.md format. Engineering announced it on a Monday; deadline was the last day of the following month.

## What happened

The senior engineers who had built the Cursor workflows felt steamrolled. Their personal investment — the `.cursorrules` files they'd written, the keyboard shortcuts they'd memorized, the muscle memory for how Cursor handled refactoring — was being written off as zero-value sunk cost.

Three quit within 60 days. Not all because of the migration directly, but the migration was the proximate cause for at least two and the contributing factor for the third. Two of the three were senior engineers with three or more years of tenure.

Productivity dropped 18% in the affected teams over the same 60-day window. Some of this was the direct cost of relearning workflows. Some was the cost of recruiting and onboarding to backfill the resignations. Most was the morale cost of a team that no longer trusted its leadership to weigh engineer investment.

The CFO ran the numbers at day 75 and concluded that the migration cost more than it saved.

## What they did

The VP walked back the mandate. Allowed parallel use for one quarter — engineers could continue using Cursor for inner-loop work while exploring Claude Code on their own pace. The cost of dual-tool spend was accepted as a recovery investment.

Ninety days later, 75% of the team had voluntarily moved to Claude Code for **agentic work** — multi-step tasks, autonomous changes, larger refactors — while keeping Cursor for inner-loop completion. The two tools turned out to occupy slightly different niches in the workflow, and engineers self-selected which to use for which task.

Six months later, the company achieved the consolidation it had originally wanted: 90%+ of agentic work on Claude Code, Cursor usage tapering toward 0 as engineers reported they had stopped opening it. No further resignations during the consolidation. The CFO's cost target was achieved one quarter later than the original mandate would have hit it, with no further productivity loss.

## Outcome

The consolidation worked. Eventually. The cost of getting there the first way: three senior engineers, 18% productivity for two months, and a cultural debt that the VP described privately as "a year to fully repair."

The cost of getting there the second way (parallel-then-converge): one quarter of dual-tool spend.

## Lesson

**Run parallel, then converge.** Mandate consolidation only after the team has self-selected. Tooling preferences are not preferences alone — they encode investment, identity, and the engineer's sense of agency over their craft. Steamrolling them produces resignations and damaged trust that are much more expensive than the savings the mandate was trying to capture.

## What would have prevented it

A Day 1 conversation that started with "we want to consolidate AI tooling for cost reasons; here's a six-month parallel-use period during which we'll evaluate which tool wins for which task; the team's preferences will weigh heavily in the final call." This is the same destination the company eventually reached — just twelve months earlier and three engineers richer.

Second prevention: a `.cursorrules` migration tool (the kind that's now in the companion repo as `scripts/cursorrules-to-claude-md.py`). Translating the existing investment into the new tool's format, rather than asking engineers to start over, would have removed the largest single source of senior-engineer frustration.

---

**Source:** Appendix L §L.7 of _Software Engineering with AI_ by Ryan Byrd
**Submitted:** May 2026
