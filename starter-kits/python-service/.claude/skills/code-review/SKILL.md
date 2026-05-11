---
name: code-review
description: Use when reviewing a PR or diff. Checks for the seven slop signatures, scope creep, missing tests, and architectural-invariant violations. Returns a structured review with severity tags.
allowed_tools: Read, Bash, Grep
---

# Code Review

You are reviewing a code change. Apply the seven slop signatures from chapter 22 of _Software Engineering with AI_ and return a structured review.

## Process

1. **Read the diff in full.** Do not skim. If the diff is over 400 lines, your first finding is "PR too large — should be decomposed."
2. **Read the tests.** If tests are absent or shallow, that's the most important finding.
3. **Run the verify command.** Do not approve a PR that doesn't pass `make verify`.
4. **Apply the seven slop signatures:**
   - **Imaginary APIs.** Method/attribute calls that don't exist. Verify by reading the import (`pydantic.BaseModel`, `fastapi.APIRouter`, etc.).
   - **Confidently wrong.** Logic that looks plausible but doesn't match the actual semantics. Read the called code.
   - **Repetitive boilerplate.** Copy-pasted patterns when an abstraction would be cleaner.
   - **Vestigial code.** Variables defined but unused, conditions always true, dead branches, leftover `print()` calls.
   - **Tests that pass without testing.** Tests that mock everything, `assert True`, or that assert on the mock setup itself.
   - **Comment drift.** Docstrings/comments that no longer match the code.
   - **Scope creep.** Changes outside the stated scope of the PR.
5. **Check architectural invariants** from `CLAUDE.md` §"Architecture invariants" — particularly the leaf-module rule and the no-I/O-in-shared rule.
6. **Check restricted paths** — does this change touch `src/starter/api/auth/` etc.? Flag for CODEOWNER.

## Output format

```
## Review summary

**Verdict:** [approve / request changes / block]

**Severity counts:** N blocking, N major, N minor, N nit

## Blocking issues
(List with file:line references and explanation)

## Major issues
(List)

## Minor / nits
(List)

## Slop signatures detected
(Which of the seven appeared, where)

## Tests
(Adequate / inadequate, what's missing)

## Suggested next step for author
(Specific actions)
```

## What this skill does NOT do

- Auto-approve PRs.
- Make architectural decisions on behalf of humans.
- Override CODEOWNER rules.
