---
name: characterize-then-refactor
description: Use when you must edit legacy code directly. Captures current behavior with characterization tests BEFORE making any change. The rule is no edit without a test that fails on the deliberate-breakage version.
allowed_tools: Read, Edit, Write, Bash, Grep
---

# Characterize, Then Refactor

You must edit legacy code. The rule is absolute: **before you change anything, you write a test that captures what the code currently does.**

The test is called a "characterization test" — its job is not to assert that the code is correct, but to detect any change in behavior. If the code returns a number ending in 7 every other Tuesday, the characterization test asserts that. We don't know if that's right, but we know if we change it.

## Process

1. **Identify the function or behavior under change.** Read it. Map what it does (inputs → outputs, side effects, edge cases).

2. **Write characterization tests.** The tests should:
   - Cover the public API of the function (what callers expect).
   - Cover edge cases visible from the inputs (None, empty, max int, etc.).
   - Cover side effects (file writes, database calls — mock at the boundary).
   - **Not assert correctness.** Assert *current behavior*. If the function returns something wrong but consistent, the test should expect the wrong thing for now.

3. **Run the characterization tests against the current code.** They must all pass. If any fail, the test is wrong (not the code). Fix the test.

4. **Make a deliberate-breakage version.** Comment out a critical line. Run the tests. They should fail. If they pass, the tests are too weak — go back to step 2.

5. **Now you can refactor.** Make small, single-purpose changes. Run the characterization tests after each change. They must continue to pass.

6. **If you discover the code is wrong** (not just the test): stop. Open a separate ticket. Fix it in a separate PR with a test that asserts the correct behavior, with explicit user approval.

## What this skill DOES

- Writes characterization tests against current behavior
- Verifies tests detect deliberate breakage
- Performs small, reversible refactor steps
- Runs tests after each step
- Commits at logical boundaries

## What this skill does NOT do

- Mix bug fixes with refactors (separate PRs)
- Delete or skip tests when they fail
- Change the behavior the characterization test captured without explicit user approval
- Touch more than the module under refactor

## Test framework patterns

### Python (pytest)

```python
def test_characterization_compute_user_score_returns_legacy_format():
    """This captures CURRENT behavior. If the function is buggy, the test
    is buggy too. We're protecting the observed behavior, not the correct
    behavior."""
    result = compute_user_score(user_id="legacy-test-1", date="2024-01-15")
    # Note: this looks weird because the legacy code is weird. We are not
    # asserting correctness, just consistency.
    assert result == {"score": 73, "tier": "B", "raw": [12, 31, 30]}
```

### TypeScript (vitest)

```typescript
describe("characterization: getUserPreferences", () => {
  it("returns the legacy shape with snake_case keys for old users", () => {
    const result = getUserPreferences("legacy-user-id");
    expect(result).toEqual({
      user_id: "legacy-user-id",
      pref_email: true,
      pref_sms: false,
      // legacy bug: returns "yes"/"no" strings instead of bools for some keys
      pref_marketing: "no"
    });
  });
});
```

## Common mistakes

- **Skipping the deliberate-breakage check.** If you don't verify the test detects breakage, you have no test.
- **Asserting on internals.** Characterization tests should assert on observable behavior (return values, side effects), not on private state.
- **Testing too narrowly.** Edge cases matter. The legacy code may have been built around them.
