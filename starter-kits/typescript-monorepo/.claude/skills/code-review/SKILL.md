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
3. **Run the verify command.** Do not approve a PR that doesn't pass `npm run verify`.
4. **Apply the seven slop signatures:**
   - **Imaginary APIs.** Method calls that don't exist on the imported library. Verify by reading the import.
   - **Confidently wrong.** Logic that looks plausible but doesn't match the actual semantics. Read the called code.
   - **Repetitive boilerplate.** Copy-pasted patterns when an abstraction would be cleaner.
   - **Vestigial code.** Variables defined but unused, conditions always true, dead branches.
   - **Tests that pass without testing.** Tests that mock everything, or that assert on the mock setup itself.
   - **Comment drift.** Comments that no longer match the code.
   - **Scope creep.** Changes outside the stated scope of the PR.
5. **Check architectural invariants** from `CLAUDE.md` §"Architecture invariants".
6. **Check restricted paths** — does this change touch `packages/api/src/auth/` etc.? Flag for CODEOWNER.

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
