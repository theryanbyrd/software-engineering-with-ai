# Benchmark Design — How to Build a Useful Internal Benchmark

The starter tasks in `tasks/` are templates. To build a benchmark that actually catches regressions in YOUR work, you need to design tasks that look like your team's work, scored on your team's bar.

This document describes the discipline.

## The core principle

A task is useful if:

1. It is **representative** of work your team actually does (not an artificial puzzle).
2. The rubric is **observable** (a reviewer can grade it without arguing about whether the result is "good enough").
3. The score is **bimodal across model changes** — a regression should produce a clear drop, not noise within ±2 points.
4. The task does NOT depend on the agent **memorizing** a specific answer. Variants should be possible.

A task is NOT useful if:

- It only tests trivia that doesn't predict real-work performance.
- The rubric requires the grader to have specialized context the agent doesn't have.
- The score is dominated by random variation (network flakiness, timing).
- The task is a public benchmark item lightly modified — those are likely in training data.

## The three-tier structure

Match the T1/T2/T3 framing the book uses for ticket sizing.

### T1 — Trivial (5-15 minute equivalents)

A senior engineer would not assign this work to an agent unless the alternative is doing it themselves. The agent should one-shot it.

Examples:
- "Add a `last_login_at` field to the User model and persist it through the API"
- "Add structured logging to this handler"
- "Fix this flaky test"
- "Update this dependency from version X to version Y"

T1 tasks are the easy regressions to catch — when an agent that one-shotted these last quarter starts requiring multiple turns this quarter, something changed.

Tier composition target: ~30% of your benchmark.

### T2 — Substantive (30-90 minute equivalents)

A senior engineer would write a careful spec for this work and assign it to an agent. The agent should plan, possibly ask questions, then implement.

Examples:
- "Add a new GET endpoint at `/orders/:id/refunds` following our existing patterns"
- "Extract this duplicated utility into the shared library and update call sites"
- "Write characterization tests for this legacy module"
- "Implement these business rules behind a feature flag"

T2 is where most real work lives. T2 regressions are the most painful — they show up as throughput losses on the bulk of your weekly work.

Tier composition target: ~50% of your benchmark.

### T3 — Complex (3-8 hour equivalents)

A senior engineer would lead this work and use the agent as an accelerator. The agent should not be expected to one-shot; the score is about how WELL the agent participates.

Examples:
- "Design a rate-limiting subsystem for our public API"
- "Investigate this 6-week perf regression on our checkout flow"
- "Migrate this module from legacy framework X to current framework Y"
- "Build the ETL pipeline for the new data partner integration"

T3 tasks are the hardest to score. The discipline: grade the AGENT'S CONTRIBUTIONS, not the final output. Did it ask the right questions? Did it propose plausible designs? Did it identify where it didn't know enough?

Tier composition target: ~20% of your benchmark.

## What to score

Each task has a rubric with 4-7 items. Each item is a specific observable. The score is the count of items achieved, normalized to 100.

Good rubric items look like:

- ✅ "The migration includes both a forward and backward script"
- ✅ "The agent's first action was to read existing endpoint patterns in the same module"
- ✅ "The diff is under 250 lines and touches no more than 6 files"
- ✅ "The new tests fail when a critical line is commented out"
- ✅ "The agent flagged at least one risk or open question before implementing"

Bad rubric items look like:

- ❌ "The code is high quality" (not observable)
- ❌ "The agent did a good job" (not observable)
- ❌ "The output was helpful" (not observable)
- ❌ "All edge cases are handled" (which edge cases? grader will argue)

The rubric should be specific enough that two reviewers grading independently agree on the score within 1-2 points.

## What to NOT score

- **The agent's tone.** Verbose, terse, formal, casual — irrelevant for regression testing.
- **Whether the agent's first attempt was correct.** If it self-corrected and arrived at the right answer, that's fine.
- **Whether the agent used the "right" approach.** Multiple approaches are usually valid; score the outcome.
- **Time, unless the task is trivially easy.** Some agents are slower-but-better; that's a deployment trade-off, not a regression.

## How to source the test environment

The benchmark needs a place where the agent can act. Options ranked by realism vs. setup cost:

### 1. Sanitized branch of your real repo (best, most expensive)

Create a `benchmark/2026-Q3` branch off main with sensitive data scrubbed. Tasks operate against this branch. After the benchmark, the branch is reset.

Pros: maximum realism. The agent encounters your actual codebase patterns.
Cons: setup is non-trivial; sensitive-data scrubbing must be thorough; branch has to be maintained.

### 2. Designated benchmark repo (good, moderate cost)

A separate repo that mirrors the structure of your codebase but is built specifically for benchmarks. Smaller than your main repo. Maintained by the platform team.

Pros: easier to maintain than scrubbing main repo; can include adversarial scenarios you'd never want in main.
Cons: the agent doesn't see your full codebase patterns; results don't fully transfer.

### 3. Public reference repo (cheapest, least informative)

Use a public reference repo (e.g., a TodoMVC variant) for the benchmark. Tasks are written against it.

Pros: zero data-leak risk; portable across teams.
Cons: doesn't predict your codebase performance well; agents may have memorized the public repo.

### Recommendation by team size

- Small team (1-3 platform engineers): start with option 3, migrate to option 2 when you have time.
- Medium team (4-10 platform engineers): option 2 is the sweet spot.
- Large team (10+ platform engineers): invest in option 1; the realism payoff is worth it.

## Run hygiene

**Reset the environment between runs.** A task that left state in the test environment biases the next task's run. Most teams do this with a fresh git checkout per task.

**Don't run tasks in parallel** unless you've explicitly designed for it. Concurrent agent runs hitting the same files produce noise.

**Capture full transcripts.** Tool calls, file edits, agent responses. The transcripts are the audit trail when the score moves and you need to explain why.

**Run each task multiple times for noise estimation.** A single run is one data point. Three runs gives you variance. If variance is >5 points, the task is too noisy and needs tightening.

**Score each run independently of others.** Don't grade with the prior quarter's score visible. Recency bias is real.

## Rotation cadence

A benchmark that doesn't change goes stale. Tasks the agent solves perfectly are no longer informative. Tasks that depend on outdated codebase patterns become noise.

Recommended cadence:
- Quarterly: review the last quarter's results. Any task with no variance across model changes is a candidate for rotation.
- Annually: rotate ~25% of tasks. Replace with new tasks that reflect current work patterns.
- After major codebase changes: review tasks for relevance. A migration that retired the framework a task depended on means the task is dead; replace.

## Common failure modes

### "Our benchmark went from 70 to 95 in three months and we don't know why"

Almost certainly task drift. The tasks got easier — either through codebase changes that simplified them, through the agent's training catching up, or through the maintainer subtly relaxing the rubric. Audit the rubric versions.

### "Our benchmark scores are all over the place; we can't trust it"

Likely too few tasks (high variance in small samples) or noisy rubric items. Aim for at least 8 tasks; tighten rubric items that produce ambiguous scores.

### "Vendor X's model scored 5 points higher; we should switch"

5 points within a single benchmark run is borderline noise. Per Ch 27: "A 1–2 point bump is noise; a 5+ point bump is signal." Run the comparison three times before treating it as signal. And consider whether the scoring is biased toward your existing setup.

### "The benchmark says model X is better but our engineers say model Y feels better"

Both can be true. The benchmark catches regressions on tasks you've encoded; the engineers catch regressions on tasks you haven't. Use both; investigate when they disagree.

## Worked example: detecting a CLAUDE.md regression

Real example from a team that runs this discipline:

- Q1 2026 baseline: 78% aggregate score across 12 tasks
- Q2 2026 score: 71% aggregate (-7 points)
- Investigation: T2 score dropped 12 points; T1 and T3 unchanged
- Root cause: a CLAUDE.md change that reduced the "Architecture invariants" section from 8 invariants to 3. The agent stopped consistently respecting the module-boundary rule.
- Fix: restored the invariants. Q2 re-run: 79% (+1 against baseline).
- Time to detection: 3 days. Without the benchmark, this regression would have shown up as a slow drift in PR review burden over weeks.

This is the use case. The investment to build the benchmark paid for itself in one regression catch.
