# Benchmarks — Golden Tasks for Agent Regression Testing

A starter library of golden tasks for quarterly model-regression testing of your AI agents. Direct implementation of Chapter 6 §6.5.2 of [_Software Engineering with AI: A Practical Handbook for the Claude Code Era_](https://www.linkedin.com/in/ryanbyrd) by Ryan Byrd, with operational guidance from Chapter 27 §27.x and Chapter 28.

## Why this matters

> A small set of golden tasks that the agent can be re-run against periodically gives you a quantitative regression signal when models change, when CLAUDE.md changes, or when a new skill lands. This is what the AI literature calls _agent unit testing_. Most teams aren't doing it yet. The teams that are doing it catch agent-quality regressions weeks before everyone else.
>
> — Ch 6 §6.5.2

The book is direct about the use case: when a new model drops, when you change CLAUDE.md, when you ship a new skill — you want to know whether the change improved or regressed agent quality on tasks that look like your work. Public benchmarks (SWE-bench, Aider Polyglot, LiveCodeBench) are useful directionally; they are not what your team actually does.

This directory is the scaffold for an internal benchmark you maintain.

## What's in here

```
benchmarks/
├── README.md                    ← this file
├── BENCHMARK_DESIGN.md          ← how to design a task set that's useful
├── tasks/                       ← 8 starter tasks across difficulty tiers
│   ├── _TEMPLATE.md
│   ├── T1-add-field-to-user-model.md
│   ├── T1-fix-flaky-test.md
│   ├── T1-add-logging-to-handler.md
│   ├── T2-add-api-endpoint.md
│   ├── T2-extract-shared-utility.md
│   ├── T2-write-characterization-tests.md
│   ├── T3-design-rate-limiter.md
│   └── T3-investigate-perf-regression.md
├── scripts/
│   ├── run-benchmark.py         ← orchestrator: run tasks, score, report
│   └── score-result.py          ← rubric-based scoring (used by orchestrator)
└── fixtures/
    └── README.md                ← guidance on sourcing the test repos
```

Tasks come in three tiers matching the T1/T2/T3 framing in the book:

- **T1 — Trivial:** ~5-15 min for a senior engineer; a strong agent should one-shot.
- **T2 — Substantive:** ~30-90 min for a senior engineer; a strong agent should plan, ask questions, then implement.
- **T3 — Complex:** ~3-8 hours for a senior engineer; even a strong agent typically needs multiple turns and human direction.

A useful internal benchmark has tasks across all three tiers. T1-only benchmarks miss the regressions that matter most (where the agent fell off a cliff on harder work). T3-only benchmarks have too much variance to detect anything.

## Quickstart

```bash
# 1. Read BENCHMARK_DESIGN.md before writing your own tasks.
#    The starter tasks here are for your codebase to copy and adapt;
#    they will not run against your repo as-is.

# 2. Pick 3-5 starter tasks; copy them; rewrite for your codebase.
cp tasks/T1-add-field-to-user-model.md tasks/your-T1-add-field-to-CustomerProfile.md

# 3. Set up the test repo (a sanitized copy of your codebase, or a designated
#    benchmark branch). See fixtures/README.md.

# 4. Run the benchmark
python3 scripts/run-benchmark.py --model claude-sonnet-4-6 --tasks tasks/

# 5. Compare against the previous quarter
python3 scripts/run-benchmark.py --report --compare results/2026-Q1.json
```

## What this is NOT

- **Not a public benchmark.** Your task set is private. Public tasks get gamed; internal tasks track what you actually care about.
- **Not a model leaderboard.** The point is regression detection on your work, not "which model is best in general." (For that, the public benchmarks are appropriate.)
- **Not a substitute for your verify command.** `verify` is the per-PR gate. Benchmarks are the quarterly model-and-harness gate. Different concerns.
- **Not a one-time investment.** Tasks go stale as your codebase evolves. Plan to rotate ~25% of tasks each year.

## What this IS

- **A regression signal.** When the score drops 5+ points, something changed. Investigate.
- **A negotiation tool.** "Our internal benchmark shows the new model is 8 points worse on T2 work" is the conversation you have with the vendor. (Do not run it on the vendor's preview environment without permission, by the way.)
- **A skill validator.** When you ship a new skill, run the benchmark with and without it. The skill that lifts the score is real; the one that doesn't isn't.
- **A CLAUDE.md regression detector.** Some "improvements" to CLAUDE.md make the agent worse. The benchmark tells you which.

## When to run the benchmark

| Trigger | What to compare against |
|---|---|
| New model release (Sonnet, Opus, GPT-5, etc.) | Last quarter's run on the previous model |
| CLAUDE.md / AGENTS.md changes | Run before merging the change; compare to baseline |
| New skill or subagent ships | Run with and without the new component |
| Quarterly cadence (default) | Previous quarter |
| Vendor's contract renewal | Last 12 months of runs |
| Investigating a "the agent feels worse lately" complaint | Latest baseline |

## What gets reported

Per-task: pass/fail, score (0-100 per the rubric), wall-clock time, token cost.

Per-run: aggregate score, pass rate by tier, cost summary, regression flags (any task that dropped 10+ points from baseline).

The report is markdown by default; JSON is also written for downstream dashboards.

## What gets gamed (and how to prevent)

If the same engineer who wrote the task is the one running the benchmark, and the benchmark's score affects their bonus or their team's metrics, the task will get gamed. Common patterns:

- **The task gets easier over time.** Rotate the engineer who maintains the task list. Quarterly review by a different reviewer.
- **The rubric gets looser.** Document the rubric verbatim in the task file. Changes to the rubric require an explicit version bump and a re-run of the prior quarter's data against the new rubric.
- **The model gets the answer in its training data.** If you use real PRs from your codebase, the model may have seen them. Synthesize variants where possible.

The right governance: the benchmark is reviewed quarterly by someone who is NOT on the team that owns it. Often the platform team owns it and a senior IC from a product team reviews.

## Adapting the starter tasks

The 8 starter tasks are written generically. They will not run against your codebase as-is. Each task file contains a `## Adaptation guide` section telling you what to swap for your stack.

For each task, the typical adaptation work is 30-90 minutes: rewrite the task description with your specific files/types/conventions, set up the fixture (a sanitized branch or a designated test repo), write the rubric items in your stack's vocabulary.

The starter set covers common surfaces:
- Schema/data work (T1, T2)
- Test work (T1, T2)
- Observability work (T1)
- API work (T2)
- Refactor work (T2)
- Architecture/perf work (T3)

If your team's work is concentrated elsewhere (heavy frontend, heavy ML, heavy infrastructure), augment with tasks that look like your work.

## Cost expectations

Each full benchmark run with a frontier model on 8 tasks across T1/T2/T3 typically costs $5-30 in tokens, depending on how much exploration the agent does on T3 tasks. Quarterly run for ~$120/year is a rounding error against the value of catching a regression two weeks early.

## License

MIT. Tasks here are templates; the rubrics and operational guidance are MIT-licensed for adaptation. Your own task set is yours and should not be checked into a public repo.
