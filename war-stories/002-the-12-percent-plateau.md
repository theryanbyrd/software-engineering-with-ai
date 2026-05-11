# 60% adoption, 12% gain, then plateau

## Setting

A 110-engineer fintech, US-based. Two years on Cursor before adding Claude Code in Q3 2025. Mature engineering culture with good test discipline, real CI, and a CFO who took the productivity dashboards seriously.

## Situation

The VP of Engineering had pitched the AI rollout as a multi-quarter productivity investment. The board approved a year-one target of 12-15% lead-time reduction on tier-2 work, with a working-assumption that year two would compound to 25%+ as the team built up skill and harness.

The harness was good. Golden-master tests on the critical services, a strong CLAUDE.md, an AI reviewer subagent in CI. The team measured honestly with Jira lead-time data, not vibes.

## What happened

Adoption hit 60% in 60 days, faster than expected. Senior engineers used the tooling for PR drafting and bug-fix scaffolding. Lead time on tier-2 work dropped 12% over six months.

Then it plateaued. Six more months: no further improvement. Senior engineers reported that the gain had come almost entirely from PR drafting and bug-fix scaffolding; tier-3 architectural work was unchanged.

The technical situation was fine. The team had honestly hit a real efficiency frontier for their codebase, harness, and workflow. The political situation was not fine: the CEO had been quietly assuming the 12% would compound to 25% by year two. It didn't. Year-two gains came from harness investment, not from raw AI capability improvement.

## What they did

The VP did not try to manufacture a fake number. She did the harder thing: a redo of the board commitment in Q3 2026, framing the next-year target as 18-22% **conditional on harness team headcount**. She brought:

- Six months of honest lead-time data showing the plateau
- A breakdown of where the 12% came from (PR drafting 7%, bug-fix scaffolding 4%, code review 1%)
- A specific theory of where the next 6-10% would come from (better harness on the four services where AI was currently struggling, plus targeted skills for the tier-3 architectural work)
- The cost: two senior engineers reallocated to a harness team for two quarters

The board approved.

## Outcome

The Q3 2026 board commitment landed. The harness team was funded. The 18-22% target was honest, and there was a plausible plan to hit it.

The CEO's relationship with the engineering org survived because the VP had not let the expectation gap go unaddressed. The conversation was harder for one quarter than it would have been to have at month six.

## Lesson

**Throughput gains plateau.** The first-derivative gain from AI tooling is real and measurable, but it doesn't compound automatically. Year two requires deliberate harness investment, not just continued use of the same tools.

**Plan the second-year commitment from data, not from the slope of the first six months.** First-six-months extrapolation is the most common board-level miscommunication in mid-size AI rollouts.

## What would have prevented it

A clear board-level briefing at month three saying *"the year-one target is 12-15%, the year-two target depends on harness investment we haven't yet committed to."* The VP had said this verbally; she had not written it down where the CEO would re-read it. Verbal caveats in board conversations are routinely lost between meetings; written caveats survive.

Second prevention: a quarterly "where did the gains come from" breakdown shared with finance. If the CFO had seen at month three that 100% of the gain was concentrated in two activities, the conversation about ceiling and harness investment would have happened then, not nine months later.

---

**Source:** Appendix L §L.5 of _Software Engineering with AI_ by Ryan Byrd
**Submitted:** May 2026
