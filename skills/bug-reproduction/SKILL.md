---
name: bug-reproduction
description: Use when the user reports a bug, a stack trace, or a "this is broken" symptom. Turns a bug report into a failing test. Does NOT fix the bug yet — that's a separate task.
allowed_tools: Read, Edit, Write, Bash, Grep
---

# Bug reproduction

## When to use this skill

The user describes a bug, pastes a stack trace, or says "X is broken." The deliverable from this skill is a failing test, not a fix.

## Procedure

1. **Read the bug report carefully.** What was the input? What was the expected output? What was the actual output?
2. **Identify the affected code.** Use grep on the symptom (a function name, an error string, a stack trace frame).
3. **Understand the trigger.** What input causes the bug? What state? What environment?
4. **Write a test that reproduces it.** The test should:
   - Use realistic inputs from the bug report
   - Assert the EXPECTED behavior (not the buggy behavior)
   - Fail when run against the current (buggy) code
5. **Run the test.** Confirm it fails. Capture the failure output.
6. **Verify the failure mode matches the report.** If the test fails for a different reason than the user described, the reproduction is wrong; refine.
7. **Stop.** Do not fix the bug. Output the failing test and the failure output.

## Output

```
## Reproduction

**Bug:** <one-line summary>
**Reproduction test:** path/to/test.py:test_name
**Failure output:**
```
<actual failure output from running the test>
```

**Next step:** propose a fix. The user will tell you to proceed or not.
```

## Forbidden

- Do not fix the bug in this skill. Reproduction first; fix is a separate skill or task.
- Do not write a test that passes against current code. The whole point is that it fails.
- Do not modify production code in this skill.
- Do not commit the failing test to a branch the user will accidentally merge.

## References

- Chapter 8 §8.x — test-first prompt patterns
- Appendix J — prompt pattern library: "Test-first" pattern
