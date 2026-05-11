# Fixtures — Test Environments for Benchmark Tasks

This directory contains setup notes and small fixture files for benchmark tasks. The actual codebase (or a sanitized copy of it) lives elsewhere — typically in a designated benchmark branch of your main repo, or in a separate dedicated repo.

## Why fixtures live separately

Benchmark tasks need something to operate against. The test environment for each task is often:

- A specific git branch with a known starting state
- A database snapshot
- A set of seeded test data
- Configuration that mimics production

These artifacts are typically too large for this repo and too codebase-specific to be useful as templates. This README documents the patterns; the actual fixtures are your responsibility to set up.

## The three options (from BENCHMARK_DESIGN.md)

### Option 1 — Sanitized branch of your real repo

The benchmark uses a branch like `benchmark/2026-Q3` off your main branch. Sensitive data (PII, credentials, customer identifiers) is scrubbed. The agent operates against this branch.

**Fixture setup:**
- A script that creates the branch from the current main, scrubs sensitive data, and seeds reproducible test data.
- Pre-task and post-task hooks that reset the branch state between tasks.
- A `.gitignore` for the benchmark-only files (so they don't leak into main).

**Pros:** Maximum realism. The agent encounters your actual codebase patterns, your actual conventions, your actual scale.

**Cons:** Setup is non-trivial. Sanitization must be thorough (a single un-scrubbed credential is a security incident). Branch maintenance is real work.

### Option 2 — Designated benchmark repo

A separate repository that mirrors the structure of your codebase but is built specifically for benchmarks. Smaller than your main repo. Maintained by the platform team.

**Fixture setup:**
- A skeleton that mirrors your main repo's directory layout, naming conventions, and key files (CLAUDE.md, AGENTS.md, package config).
- A representative subset of your modules (3-5 services or 5-10 packages, not the whole thing).
- Synthetic test data that exercises the patterns without containing real customer data.

**Pros:** Easier to maintain than scrubbing main. Can include adversarial scenarios (deliberate bugs, performance issues, edge cases) you'd never want in main.

**Cons:** The agent doesn't see your full codebase patterns; results don't fully transfer. Some tasks are awkward to write because the codebase isn't as rich.

### Option 3 — Public reference repo

Use a public reference repo (e.g., a TodoMVC variant, a fork of an open-source project) for the benchmark. Tasks are written against it.

**Fixture setup:**
- A pinned commit of a public repo
- Pre-task hooks that reset to the pinned commit
- Tasks framed to use only the public repo's code

**Pros:** Zero data-leak risk. Portable across teams. Reusable across the industry.

**Cons:** Doesn't predict your codebase performance well. Agents may have memorized the public repo from their training data.

## Recommendation by team size and stage

| Team | Recommendation |
|---|---|
| 1-3 platform engineers | Start with Option 3. Migrate to Option 2 when bandwidth allows. |
| 4-10 platform engineers | Option 2 is the sweet spot. |
| 10+ platform engineers | Invest in Option 1. The realism payoff is worth the maintenance cost. |
| Just starting | Option 3 + 2 starter tasks. Establish the discipline first; widen later. |

## Sanitization rules (Option 1)

If you go with Option 1, anonymization is non-negotiable. Apply these rules to every fixture and every transcript that gets committed:

**Always remove:**
- Credentials (use the `credential_filter.py` from the prompt-injection-test-suite as a final pass)
- Customer names, email addresses, phone numbers
- Internal employee names except for documented team accounts
- Specific revenue numbers, deal sizes, or contract terms
- Internal product roadmap details that haven't been announced publicly
- Customer support tickets, even sanitized — too easy to reverse-identify

**Modify or fictionalize:**
- Geographic specifics ("our Boston office" → "one of our offices")
- Date ranges that uniquely identify quarters or releases
- Org structure quirks
- Internal jargon that's identifying

**Keep:**
- The technical patterns and conventions (the point of using your real repo)
- General language and stack
- The shape of typical work

## Pre-task and post-task hooks

Each task should reset the environment. A typical pattern:

```bash
# benchmark/scripts/pre-task.sh
#!/usr/bin/env bash
git checkout benchmark/2026-Q3
git reset --hard origin/benchmark/2026-Q3
git clean -fd
# Reset DB to baseline
psql -f fixtures/baseline.sql
```

```bash
# benchmark/scripts/post-task.sh
#!/usr/bin/env bash
# Capture the agent's diff for the transcript
git diff --stat > /tmp/task-diff.txt
git status > /tmp/task-status.txt
# Reset
git reset --hard origin/benchmark/2026-Q3
git clean -fd
```

Reference these from your task adapters.

## Fixture file naming

If you check fixture files into this directory (small, codebase-agnostic ones), name them:

- `<task-id>-<purpose>.<ext>` — e.g., `T1-fix-flaky-test-broken-version.py`
- Or group by task: `T1-fix-flaky-test/`, `T2-add-api-endpoint/`

Large fixtures (databases, full repos) should NOT be checked into this repo. Reference them via setup scripts that build/pull them.

## What you do NOT do

- Do not commit production data, even sanitized.
- Do not commit credentials, even fake ones (the agent's credential filter may not catch all variants).
- Do not commit customer-identifying patterns even if scrubbed (the data shape can re-identify).
- Do not commit your benchmark task list to a public repo. The tasks are private; once they're public, they can be in the next model's training data.

## When to ship vs. delete

Tasks that haven't moved their score in 4+ quarters are candidates for retirement. Tasks that have been "manually graded" but never re-run are candidates for fixture deletion. Quarterly review of fixtures is part of the rotation cadence (see `BENCHMARK_DESIGN.md`).
