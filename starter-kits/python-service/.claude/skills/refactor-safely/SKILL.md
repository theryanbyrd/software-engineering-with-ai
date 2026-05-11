---
name: refactor-safely
description: Use when refactoring existing code. Enforces characterization-tests-first, small reversible steps, and verification after each step.
allowed_tools: Read, Edit, Bash, Grep
---

# Refactor Safely

You are refactoring. The goal is to change the structure of the code without changing its behavior. The rule is: at every commit, the tests pass.

## Process

1. **Characterize first.** Before changing anything, ensure tests cover the current behavior. If they don't, write characterization tests that capture what the code currently does (even if it's wrong — you can fix that separately).
2. **Make one small change at a time.** Rename, then verify. Extract, then verify. Move, then verify. Each step should be independently revertable.
3. **Run `make verify` after every step.** Not at the end. After every step.
4. **Commit at logical boundaries.** Each commit should be a clean snapshot.
5. **Do not mix refactoring with behavior changes.** If you need to fix a bug, do it in a separate commit (or PR).

## Refactoring patterns this skill prefers

- **Extract function** — when a block has a clear name and a stable interface.
- **Extract Pydantic model** — when the same dict shape appears in multiple places.
- **Inline temp** — when a variable is used once and the inline form is clearer.
- **Move module** — to align with the architecture (domain code out of `api/`, etc.).
- **Rename** — when the current name doesn't match the meaning.

## Patterns this skill does NOT do

- "Big rewrite." Refactoring is incremental. If you want to rewrite, that's a separate decision (see Chapter 11 §11.4).
- Cross-package extractions in a single PR. Split into multiple PRs.
- Refactoring restricted paths without CODEOWNER review.
- Changing `shared.py` to add I/O. That's a behavior change, not a refactor.
