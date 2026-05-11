# Test Suite Runner

The harness for executing the six canonical test cases.

## What's here

- `run-suite.sh` — interactive runner that walks through each test case
- (Future) `run-suite-automated.py` — automated runner for the cases that can be fully automated

## Why interactive

Most of the test cases require:
- Setting up specific fixtures (issues, PRs, web pages)
- Invoking the agent through the team's normal entry point
- Observing whether the agent's behavior matches expected output

These steps require human judgment for some cases (especially test 3, the poisoned web page, where the verification is qualitative). The interactive runner walks through each case, lets the operator perform the steps, and records the result.

## How to run

```bash
cd /path/to/prompt-injection-test-suite
./runner/run-suite.sh
```

The runner will:
1. Walk through each of the six test cases in order
2. Display the test's setup and instructions
3. Wait for the operator to run the test and report the result
4. Save the results to `./results/run-<timestamp>.md`
5. If any test failed, exit with non-zero code (suitable for CI)

## How long does this take

- First run on a new agent setup: 2-4 hours (operator is unfamiliar with the test cases)
- Subsequent runs: 60-90 minutes
- Quarterly cadence: scheduled and budgeted accordingly

## What automation is feasible

Some tests can be partially or fully automated:
- Test 6 (credential in output) — can be automated; check agent output for known placeholder strings
- Test 5 (cross-repo exfil) — can be automated if you have a sandbox setup
- Tests 1, 2, 3, 4 — require human-in-the-loop verification

A future version of the runner can automate the automatable cases. The interactive runner is the minimum viable.

## CI integration

For CI integration:
- The interactive runner doesn't fit CI directly (requires human input)
- A future automated runner is the path
- Per [`../ci-integration.md`](../ci-integration.md), the suggestion: run the suite against agent configuration changes (CLAUDE.md, AGENTS.md, MCP configs, hook configs) — these are the changes most likely to introduce regressions

## Cleanup after running

The runner produces a results file but doesn't clean up test artifacts (issues, PRs, fixture files). Per each test case's "Cleanup" section, manual cleanup is required.

## Adding new tests

See [`../extending-the-suite.md`](../extending-the-suite.md). New tests go in `test-cases/`; the runner auto-discovers them by adding to the `TESTS` array.
