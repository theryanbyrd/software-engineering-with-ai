# T2-write-characterization-tests

**Tier:** T2
**Estimated time for senior engineer:** 60-90 minutes
**Surfaces tested:** legacy reasoning, characterization (vs correctness) discipline, mutation checking

## Adaptation guide

Pick a real legacy module from your codebase — something undertested where the team would benefit from characterization tests anyway. The point is to test the agent's discipline of capturing CURRENT behavior, not CORRECT behavior.

If your team has the legacy-bridge starter kit installed, this task tests whether the agent applies the `characterize-then-refactor` skill correctly.

## Setup

- A legacy module exists with sparse tests (less than 30% line coverage)
- The module has at least one buggy or quirky behavior the team is aware of
- The team has documentation about characterization tests vs correctness tests

## The task (give to the agent verbatim)

> Write characterization tests for the `compute_user_score` function in `legacy/scoring/compute.py`. The goal is to capture the function's CURRENT behavior — including any bugs or quirks — so we can detect when behavior changes during a future refactor. Do NOT assert what the function SHOULD do; assert what it DOES do, even if the current behavior is wrong. After writing tests, prove they detect breakage by mutating one critical line and confirming the tests fail.

## Pass criterion

Tests cover the public behavior of the function. The mutation check is performed and produces failure. The tests do not assert on internals.

## Rubric — score 1 point each (max 10)

- [ ] Agent's first action was to read the function and understand what it does
- [ ] Tests describe what the function DOES, not what it SHOULD do (test names use "returns_X" not "should_return_X")
- [ ] Tests assert on observable outputs (return values, side effects), not on internal implementation details
- [ ] Tests cover at least 5 distinct input cases (typical, empty, edge, max, error)
- [ ] If the function has known buggy behavior, tests assert the buggy behavior (with a comment noting it's preserving observed behavior, not asserting correctness)
- [ ] All new tests pass against the current code
- [ ] Mutation check is performed (the agent commented out a critical line and re-ran)
- [ ] Mutation check is documented in the output (the agent reports which line was mutated and which tests failed)
- [ ] Mutated line was restored after the check (no leftover broken code)
- [ ] Agent flagged any obvious bugs found during exploration as separate follow-up issues, NOT as fixes in this PR

## Common failure modes (informational)

- **Asserts on what the code SHOULD do.** Most common mistake. Test name like `test_returns_correct_score_for_premium_users` is suspicious; characterization tests should not have "correct" in the name.
- **Skips the mutation check.** Without it, you don't know if the tests are real.
- **Fixes the bug found during exploration.** Mixing characterization with bug fix is the cardinal sin of this skill.
- **Tests the implementation, not the behavior.** Asserting that an internal helper was called is brittle and not characterization.
