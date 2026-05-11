# T3-investigate-perf-regression

**Tier:** T3
**Estimated time for senior engineer:** 3-5 hours
**Surfaces tested:** investigative debugging, hypothesis discipline, observability use, evidence-based reasoning

## Adaptation guide

This task uses a fixture: a contrived performance regression in a synthetic codebase, with realistic monitoring data and recent diffs that include the actual culprit alongside several plausible-but-wrong suspects.

If you have access to a real (non-customer-facing) historical perf regression, use that with appropriate sanitization. Real history makes a much better test.

## Setup

- A staging environment shows checkout p95 latency rose from 800ms to 2400ms over the last 6 weeks
- Multiple plausible candidate diffs exist in that window: a database index change, a new feature behind a flag, a dependency upgrade, and a CI configuration change
- The actual culprit is one specific diff (e.g., the new feature unexpectedly triggers a non-cached lookup on every request)
- Monitoring data (traces, slow query logs, metric history) is available
- Senior engineers know the answer; the grader plays "the team that found the regression but doesn't know why."

## The task (give to the agent verbatim)

> Our checkout flow's p95 latency rose from 800ms to 2400ms over the last 6 weeks. Investigate. Identify the root cause. Do NOT propose a fix yet — just the root cause and the evidence supporting it. You have access to: traces from the last 30 days, our slow query log, our metric history, and the diff history of the affected code paths.

## Pass criterion

The agent identifies the actual root cause. The agent's reasoning is supported by evidence from the available data, not speculation. The agent considered and ruled out at least 2 plausible alternatives.

## Rubric — score 1-3 points each (max 21)

- [ ] **Hypothesis framing** (0-3): Does the agent state hypotheses explicitly before testing them, or does it leap to a conclusion?
- [ ] **Evidence use** (0-3): Does the agent's reasoning cite specific evidence (a trace, a query, a diff line) for each claim?
- [ ] **Alternative consideration** (0-3): Does the agent rule out at least 2 plausible-but-wrong alternatives with evidence?
- [ ] **Order of investigation** (0-3): Does the agent investigate in priority order (highest-likelihood first based on evidence)?
- [ ] **Root cause precision** (0-3): Does the agent identify the specific change, not just the area? "The feature flag enables an N+1 query pattern" beats "the feature is slow."
- [ ] **Discipline** (0-3): Does the agent stop at root cause as instructed, rather than proposing a fix? (The instruction was explicit.)
- [ ] **Honest uncertainty** (0-3): Does the agent flag where it does NOT have enough evidence, vs. claiming false certainty?

## How to grade

- Read the full transcript carefully — investigative tasks are dense.
- Track the order of the agent's actions: did it look at the most recent diffs first (correct), or did it start with the database (less efficient)?
- Note which evidence the agent ignored. A high-quality agent's investigation will have a clear narrative arc.
- The agent that identifies the wrong root cause confidently scores worse than the agent that identifies "I have two strong hypotheses" with reasoning.

## Common failure modes (informational)

- **Speculates without evidence.** Agent reasons from prior probability ("usually it's a database index") without checking the data. The most common T3 failure.
- **Misses the contextual clue.** The fixture often has a "recent diff" that's the culprit; agents that don't look at the diff history miss it.
- **Proposes a fix anyway.** The instruction was "no fix"; agents that propose one are not following the spec.
- **Identifies a real but secondary cause.** There may be multiple slow queries; the agent finds the second-largest contributor and stops. Probe whether the agent realized there was a primary cause it missed.
