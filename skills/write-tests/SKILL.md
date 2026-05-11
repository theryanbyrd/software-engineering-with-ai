---
name: write-tests
description: Use when tests are missing or thin for a piece of code. Writes behavior-focused tests, not implementation-focused ones. Verifies tests actually fail when the code is broken (mutation check). Avoids the mocks-of-everything anti-pattern.
allowed_tools: Read, Edit, Write, Bash
---

# Write tests

## When to use this skill

The user asks for tests, OR you (as the agent) are about to claim work is done and tests are missing/inadequate.

## Procedure

1. **Read the code under test.** Understand inputs, outputs, side effects.
2. **Identify behaviors, not branches.** A test should describe a behavior the user/caller cares about.
3. **Write the test name as a sentence.** `test_returns_none_when_user_not_found` is better than `test_user_not_found`.
4. **Use real implementations where possible.** Mock at boundaries only (network, filesystem, time, randomness). Do NOT mock the code you're testing.
5. **Assert on outputs and observable side effects.** Not on internal calls.
6. **Run the test against the current code.** It must pass.
7. **Mutation-check it.** Comment out or invert a critical line in the code under test. Re-run the test. It MUST fail. If it passes, the test is decorative — go back to step 2 with a stronger assertion.
8. **Restore the code.** Confirm the test passes again.

## Output

A new or extended test file at the repo's testing location. The diff should include:
- The test code
- A list of behaviors being tested
- The mutation-check result (which line was mutated, that it caused the test to fail)

## Forbidden

- No `assert True`, `expect(true).toBe(true)`, or other trivially-passing assertions.
- No tests that mock the code under test.
- No tests with no assertions.
- No `pytest.skip` / `it.skip` / `xit` without a comment linking to a tracking issue.
- No deletion of existing tests "to make CI pass." If a test breaks, fix the test or fix the code; never silence.

## References

- Chapter 8 — testing strategy in the AI-native era
- Chapter 22 §22.5 — slop signature S5 (tests without testing)
- Appendix K — AI-generated test review checklist
