# Worked Examples as Case Studies

Three concrete walkthroughs you can tell your CEO. Per Ch 47:

> Three example scenarios, walked through using the patterns from the rest of the book.

This file reframes the Ch 47 worked examples as case studies for executive conversations. The book uses them to illustrate the discipline; this file uses them to ground abstract conversations in concrete reality.

## Why this matters for executive communication

The CEO's questions about AI productivity tend to be abstract:
- "How is the AI rollout going?"
- "Is the harness investment paying off?"
- "What does this look like in practice?"

Abstract answers ("we're tracking to commitments; metrics are healthy") don't satisfy. The CEO often needs a concrete walkthrough — a specific story that makes the work visible.

The three Ch 47 examples are exactly this. Adapted to your team, they answer the CEO's "what does this actually look like" question.

## Example 1 — A T2 bug fix in well-understood code

The success case. Tell this when the CEO asks "what does AI tooling do for a normal day?"

### The scenario

Customer reports that downgrades mid-cycle produce wrong proration. Sentry has a stack trace. The bug is reproducible.

### The walkthrough (Ch 47 §47.1 condensed)

1. Engineer files an agent-ready issue (Tier 2). Cites the Sentry trace, fixture, expected behavior, acceptance test.
2. Inverted brief: "What do you need to know?" Claude asks two clarifying questions; engineer answers via ADR + README links.
3. Engineer triggers Claude Code (Sonnet 4.6). Subagents run: explorer maps call graph, planner produces plan, engineer approves.
4. test-writer writes failing reproduction test.
5. implementer makes the smallest change to pass the test.
6. Hooks fire: format, lint, typecheck, tests. PR-creation hook gates on verify.
7. Draft PR opens. AI reviewer subagent flags one diff line touching unrelated code; engineer trims.
8. Senior reviewer approves. CI passes. Canary 5% / 50% / 100%. Sentry trace closes.
9. Total wallclock: ~2 hours, mostly review. AI tokens: ~$0.40.

### The lesson (the part you tell the CEO)

> Bounded T2 work in a clean codebase with a strong harness is where AI assistance shines. Two hours, one engineer, one senior reviewer.

### How to tell this story

In a 90-second walkthrough:

> "Take a real example from last sprint: a billing bug where downgrades mid-cycle produced wrong proration. Sentry caught the trace, engineer wrote a tier-2 spec, AI tooling did the implementation in under an hour with the human reviewing. Two hours total wallclock, $0.40 in AI tokens. The same work would have been three or four hours of pure engineering time without the tooling. We do dozens of these per sprint; the cumulative gain is real."

### Why this story lands with executives

- **Concrete bug** — not abstract productivity. The CEO can picture the customer impact.
- **Specific time and cost** — defensible numbers. Not "much faster"; "two hours, $0.40."
- **Visible humans** — engineer, reviewer. Not "AI did it"; "AI assisted, humans verified."
- **Visible discipline** — agent-ready issue, AI reviewer subagent, canary deployment. The harness is part of the story.

### Adapting to your team

Pick a real bug fix from the last 30 days. Walk through it the same way. The specifics matter:

- Real customer impact (not made up)
- Real engineer (named, with context)
- Real review path (the actual reviewer)
- Real metrics (actual time and tokens)

Don't fabricate. The CEO can usually tell.

## Example 2 — A T3 cross-cutting refactor

The hard work case. Tell this when the CEO asks "but doesn't AI struggle with hard problems?" or when the CEO is questioning the value of senior engineers.

### The scenario

The auth module's session-handling code has accreted special cases over five years. Now the team needs to add SSO, and the existing code is unsafe to modify.

### The walkthrough (Ch 47 §47.2 condensed)

1. Engineer files T3 (architecting) issue.
2. Senior engineer writes ADR before any code. Three options. Team picks strangler-fig (new auth path next to old, traffic shifted gradually, old retired only after 30 days zero regressions).
3. Inverted brief: Claude (Opus 4.7, plan mode) returns 12 clarifying questions. Senior addresses in writing. Plan grows to 4 pages.
4. Characterization tests written first. 30+ tests captured against existing auth flow, including bugs-as-features. These pass before refactor begins.
5. implementer builds new path behind feature flag. Senior engineer leads, Claude assists. Six PRs over two weeks, each ≤400 lines, each individually reviewable.
6. security-reviewer subagent (Opus 4.7) reviews every diff. CODEOWNERS gate requires senior security review on auth-touching PRs. Engineer pairs with security lead.
7. Migration: 1% canary for week, 5% for week, 25% for week, 50%, 100%. Each step gated on metrics + manual sign-off.
8. Old path retired only after 30 days at 100% with zero regressions. Old path deleted in final PR.
9. Logged as Score in retro. Seven-week timeline beats prior estimate of three months.

### The lesson (the part you tell the CEO)

> T3 work needs the full discipline. The AI assists the senior; it does not replace the senior. The win is the schedule compression and the test-coverage discipline, not the line-of-code count.

### How to tell this story

In a 2-minute walkthrough:

> "Take the SSO migration we did in Q2. Five-year-old auth code, brittle, needed to add SSO. Senior engineer led — wrote the ADR, three options, picked the safe path. AI tooling assisted on six PRs over two weeks, each individually reviewable. The security review used a specialized AI subagent on every diff plus a senior security pair-review. The migration deployed gradually over four weeks with zero customer-facing incidents. The original estimate was three months; we shipped in seven weeks."

### Why this story lands with executives

- **Hard problem** — not a typo fix. The CEO knows auth code is dangerous.
- **Senior engineer leading** — answers the "are seniors still useful" question concretely.
- **Discipline visible** — ADR, characterization tests, gradual deploy. Not "AI did it"; "we did it with discipline, AI assisted."
- **Specific schedule compression** — three months to seven weeks. Defensible.
- **No incidents** — the trump card. Hard work shipped without breaking things.

### Why this story matters for headcount conversations

The CEO who is wondering "do we still need senior engineers if we have AI" reads this story and sees: yes, we need senior engineers. The senior engineer's judgment is the pivotal capability. AI accelerates the work; it does not replace the engineer.

If the CEO is pushing for senior engineer cuts, this is the kind of story that grounds the pushback in reality. The schedule compression is a productivity gain that comes from senior engineers using AI well — not from AI replacing them.

## Example 3 — A failed one-shot, triaged

The discipline case. Tell this when the CEO asks "what about when AI fails?" or when the CEO has heard about an incident at another company.

### The scenario

Engineer files T2 issue: "Add CSV export to reports page." Files listed. Acceptance test described. The agent runs and produces a PR that downloads the wrong data.

### The walkthrough (Ch 47 §47.3 condensed)

1. Reviewer reads diff. Two issues: agent picked wrong query because it didn't see the report's filtering logic in the front-end state; test mocks the response rather than asserting on CSV bytes.
2. Engineer killed the run, re-read the issue, and noticed: issue listed the backend file but not the front-end state file. Agent didn't have the context.
3. Triage: this is **Opportunity**, not Train. Harness was missing. Fix: add `reports/AGENTS.md` pointing at the relevant front-end state file and a fixture for a representative filtered report.
4. Engineer files separate ticket for harness improvement. Ships that day.
5. Original issue re-run with upgraded harness. Agent succeeds. Logged as Score.

### The lesson (the part you tell the CEO)

> Failed one-shots are diagnostic. The triage discipline is what closes the loop. Without it, the team would have written the agent off as "broken on this kind of work" and gone back to writing the code by hand.

### How to tell this story

In a 90-second walkthrough:

> "Last month an engineer ran an AI task to add CSV export to a reports page. The agent produced wrong code — picked the wrong query because it couldn't see the front-end filtering logic. Two paths from there: (a) conclude AI doesn't work for this kind of task and stop using it, or (b) figure out what the harness was missing and fix it. We did (b). Engineer triaged it as an 'Opportunity' — the agent's failure was a missing piece of documentation. Filed a separate ticket for the documentation, shipped it that day, re-ran the original task. Agent succeeded. The whole loop took half a day; the harness improvement makes the next 50 reports-page tasks easier."

### Why this story lands with executives

- **Real failure** — concrete; not a hypothetical. The CEO knows AI fails sometimes.
- **Discipline response** — not "AI is broken"; "the harness needed work; we fixed the harness."
- **Self-improving system** — the harness compounds. One fix prevents N future failures.
- **Specific outcome** — half-day loop; future tasks succeed.

### Why this story matters when an incident happens

If the team has a real AI-related incident (production bug, security issue, embarrassing mistake), this story is the template for the response.

The CEO's worry: "AI tooling is dangerous; we should pause."

The response framing: "The failure is diagnostic. We triage every failure. Most failures map to specific harness gaps; we fix the harness. The team's overall reliability goes up over time, not down. Here's the specific incident, here's what we triaged, here's what we shipped to prevent it."

This is the difference between a team that learns from failures and a team that hides them. The CEO who sees the discipline trusts the rollout; the CEO who sees defensiveness loses trust.

## When to use which story

| CEO question | Story to tell |
|---|---|
| "How's it going?" | Story 1 (the success case) |
| "What about hard problems?" | Story 2 (the cross-cutting refactor) |
| "Do we still need senior engineers?" | Story 2 |
| "What about when it fails?" | Story 3 |
| "Should we pause?" | Story 3 (in incident response framing) |
| "Why is the platform team so big?" | Story 3 (the harness compounds) |
| "What does the harness investment buy us?" | Stories 2 and 3 (where the harness shows up) |

## Adapting all three to your team

For each story, you need a real version from your team. Ideally:

- **A real T2 bug fix** from the last 30 days, with metrics
- **A real T3 architecture project** from the last 6 months, with timeline and outcome
- **A real failed one-shot** from the last 90 days, with the triage and resolution

If you don't have a real version of any of these, the rollout itself is the issue. The book describes patterns that should be visible in any disciplined team within months. If they aren't, that's the conversation to have — but you have to have it without these stories to tell.

## How to keep the stories fresh

Stories age. A bug fix from a year ago doesn't have the same vividness as one from last month.

Recommended cadence:
- Refresh the story library quarterly
- Pull from the last 90 days for examples
- Have 2-3 versions of each (the same shape, different specifics)
- Brief your direct reports on the stories they should be ready to tell

The CEO might ask any of them at any time. Being able to tell a fresh, specific story signals that you are paying attention to the work, not just to metrics.

## What NOT to do

### Don't fabricate

If you don't have a real version of one of the stories, don't make one up. The CEO will sometimes ask follow-up questions. "Who was the engineer? What was the customer impact? Show me the PR." Fabricated stories collapse under questions.

### Don't tell stories you don't understand

If you tell story 2 (the T3 refactor) and you don't actually understand what a strangler-fig pattern is or why characterization tests matter, the CEO will figure it out. You'll lose more credibility than if you'd just declined to walk through the example.

### Don't pad with stories the CEO didn't ask for

If the CEO asked one question, tell one story. Don't bombard with three stories. The CEO has limited attention.

### Don't moralize

The stories illustrate the discipline. They don't moralize about teams that don't have the discipline. The lesson is concrete; the framing is "here's what works for us."

### Don't overclaim

If the T3 refactor took 7 weeks but the original estimate was generous, don't claim "we shipped in half the time." The CEO will eventually find out, and the credibility hit is worse than the original honesty would have been.

## Companion artifacts

- [`hype-rebuttal-table.md`](hype-rebuttal-table.md) — for when the CEO is pushing back on hype
- [`realistic-roi-message.md`](realistic-roi-message.md) — for the aggregate numbers
- [`four-slide-board-deck-walkthrough.md`](four-slide-board-deck-walkthrough.md) — for board-level versions
- [`eleven-pm-podcast-clip-protocol.md`](eleven-pm-podcast-clip-protocol.md) — for the anxious-CEO ping
- `failed-one-shot-triage/` — adjacent (the discipline behind story 3)
- `legacy-codebase-onboarding/` — adjacent (the discipline behind story 2's strangler-fig)
- Ch 47 — source
