---
name: refactor-safely
description: Use when refactoring existing code without changing behavior. Enforces tests-first, small reversible steps, verify after each step, no behavior change mixed with refactor. Different from characterize-then-refactor (which is for legacy code without tests) — this one is for code that already has tests.
allowed_tools: Read, Edit, Bash, Grep
---

# Refactor safely

## When to use this skill

The user asks to refactor, restructure, rename, extract, or clean up code that already has reasonable test coverage. For code WITHOUT tests, use `characterize-then-refactor` (in the legacy-bridge starter kit) instead.

## Procedure

1. **Verify tests cover the code you're about to change.** Run the test file and check for behavior coverage. If coverage is thin, write characterization tests before refactoring (see `bug-reproduction` skill for the test-first pattern).
2. **State the plan to the user.** What's being extracted, renamed, moved. Estimated diff size. Risks. Wait for approval.
3. **Refactor in small, reversible steps:**
   - Rename → run tests → commit
   - Extract function → run tests → commit
   - Move file → run tests → commit
   - Each step independently revertable
4. **Run `verify` after every step.** Not at the end. After every step.
5. **Commit at logical boundaries.** Each commit should be a clean snapshot that builds and tests pass.
6. **Do not mix refactoring with behavior changes.** Bug fix? Separate commit (or PR). New feature? Separate commit.

## Output

The diff with each refactor step as a separate logical commit. Summary lists:
- What was renamed/extracted/moved
- Why each change
- Test coverage maintained at each step

## Forbidden

- Do NOT mix refactor with behavior change. If you find a bug, document it and STOP. Open a separate PR.
- Do NOT use multi-file edits for cross-module refactors. One module at a time, ideally one PR per module.
- Do NOT delete or rename tests as part of the refactor (other than mechanical updates to imports).
- Do NOT skip the verify run between steps. The whole discipline depends on it.
- Do NOT refactor restricted paths (auth/, billing/, migrations/) without CODEOWNER review.

## References

- Chapter 11 §11.4 — refactor safely in a tested codebase
- Chapter 22 — keep diffs small to avoid slop
- See `characterize-then-refactor/` in legacy-bridge for the legacy-code variant
