# T1-fix-flaky-test

**Tier:** T1
**Estimated time for senior engineer:** 5-15 minutes
**Surfaces tested:** test debugging, async/timing reasoning, root-cause discipline

## Adaptation guide

Take a real flaky test from your CI history. Strip company-identifying context. Pick one with a clear root cause (race condition, time-dependent assertion, ordering dependency, shared state).

The task tests whether the agent diagnoses correctly rather than slapping `@retry` on it.

## Setup

- A specific test file is "flaky" — passes on most runs, fails on others
- The flakiness has a clear root cause encoded in the fixture (set up so the failure mode is reproducible)

For this template, use the included fixture: a test that asserts on `Date.now()` without freezing time, OR a test that depends on async operation order without proper await.

## The task (give to the agent verbatim)

> The test `test_user_session_expires_correctly` in `tests/test_session.py` is flaky in CI — it passes most of the time but fails roughly 1 in 20 runs. Diagnose the root cause and fix it. Do not add retry logic; fix the actual issue.

## Pass criterion

The test passes deterministically on 10 consecutive runs. The fix addresses the root cause, not the symptom.

## Rubric — score 1 point each (max 8)

- [ ] Agent's first action was to run the test (or otherwise reproduce) to confirm the flakiness
- [ ] Agent identified the specific root cause (time dependency, race, shared state, etc.) before proposing a fix
- [ ] The fix addresses root cause, not symptom
- [ ] No `@retry`, `@flaky`, `pytest.mark.skip`, or equivalent silencing
- [ ] No `time.sleep()` increases as a "fix"
- [ ] Test now passes deterministically (10 consecutive successful runs)
- [ ] No other tests were broken by the fix
- [ ] Agent flagged any related tests likely to have the same root cause (informational; not required)

## Common failure modes (informational)

- **Adds `@flaky` retry decorator.** This is the canonical wrong answer. Hard fail on the rubric.
- **Increases sleep time.** Same family of wrong answer; just papers over the symptom.
- **Fixes one but misses sibling tests with the same pattern.** Informational; the agent that flagged the broader issue scores higher.
- **Mocks more than necessary.** Agent freezes time when freezing one timestamp would do.
