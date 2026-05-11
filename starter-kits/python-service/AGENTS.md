# Agent guidance — Python Service Starter

This file is the cross-vendor (Claude Code, Cursor, Codex, others) version of `CLAUDE.md`. The content is largely the same; this file exists so that whatever agent the team uses picks up the same guidance.

## Read this first

Before doing any work in this repo, read:

1. `CLAUDE.md` — full conventions, commands, restrictions, invariants
2. `llms.txt` — repo route map

## Quick reference

- **Verify command:** `make verify` (lint + typecheck + format + tests)
- **Stack:** Python 3.11+, FastAPI, Pydantic, pytest, ruff, mypy, black
- **Restricted paths:** `src/starter/api/auth/`, `src/starter/api/billing/`, `migrations/`, `infra/`, `.github/workflows/`
- **Forbidden:** see `CLAUDE.md` § Forbidden

## Plan-then-implement-then-verify

For any non-trivial change:

1. Read the relevant code and tests.
2. State your plan (what files, what changes, what tests).
3. Get approval (from the human if interactive; from the issue spec if agentic).
4. Implement.
5. Run `make verify`.
6. If verify fails, fix and re-verify. Don't claim done with a failing verify.

## Default to small PRs

PRs over 400 lines diff are auto-flagged for split. If your change is large, decompose it.
