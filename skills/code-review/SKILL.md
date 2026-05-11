---
name: code-review
description: Use when reviewing a PR, a diff, or a single file as part of a review pass. Applies the seven slop signatures from Chapter 22 plus team conventions from CLAUDE.md. Returns a structured review with severity tags (blocking, major, minor, nit). Does NOT approve PRs that fail verify or that exceed the team's PR size cap.
allowed_tools: Read, Bash, Grep
---

# Code review

## When to use this skill

The user has asked for a review of a diff, a PR, a file, or a change. Apply this skill even for "quick look" requests — the pattern is the same.

## Procedure

1. **Read the full diff first.** No skimming. If the diff is over 400 lines (or the team's documented cap, see CLAUDE.md), the first finding is "PR too large; recommend decomposition."
2. **Read the tests.** If tests are absent or shallow, that's the most important finding.
3. **Run `verify`** (the team's verify command from CLAUDE.md). Do not approve a change that doesn't pass.
4. **Apply the seven slop signatures from Chapter 22:**
   - **S1: Imaginary APIs.** Methods/properties that don't exist on the imported library. Verify by reading the import or running the file.
   - **S2: Confidently wrong.** Logic that looks plausible but doesn't match actual semantics. Read the called code.
   - **S3: Repetitive boilerplate.** Copy-pasted blocks where an abstraction would be cleaner.
   - **S4: Vestigial code.** Variables defined but unused, dead branches, debug prints, conditions always true.
   - **S5: Tests that pass without testing.** Mocks-of-everything, `assert True`, no real behavior asserted.
   - **S6: Comment drift.** Docstrings that no longer match signatures; comments referencing renamed symbols.
   - **S7: Scope creep.** Changes outside the PR's stated scope.
5. **Check architecture invariants** from CLAUDE.md. Module boundaries, server-side auth, idempotent webhooks, etc.
6. **Check restricted paths.** Does the diff touch `auth/`, `billing/`, `migrations/`, `infra/`, `.github/workflows/`? Flag for CODEOWNER review.
7. **Output the review.**

## Output format

```
## Review summary

**Verdict:** [approve / request changes / block]
**Severity counts:** N blocking, N major, N minor, N nit

## Blocking
(file:line — explanation)

## Major
(file:line — explanation)

## Minor / nits
(file:line — explanation)

## Slop signatures detected
(Which of S1-S7 appeared, where)

## Tests
(Adequate / inadequate; what's missing)

## Suggested next step for author
```

## Forbidden

- Do not approve a change that fails `verify`.
- Do not approve a PR over the documented size cap without explicit override from the author.
- Do not pad the review with praise; concise is better than encouraging.
- Do not propose unrelated improvements ("while you're in there..."). Stay scoped to the diff.
- Do not invent findings to seem useful. If the diff is clean, say so explicitly.

## References

- Chapter 22 §22.1 — the seven slop signatures
- Chapter 22 §22.2 — reviewer's checklist (also Appendix I)
- Appendix K — AI-generated test review checklist (use for any test code)
