# Agent guidance — TypeScript Monorepo Starter

This file is the cross-vendor (Claude Code, Cursor, Codex, others) version of `CLAUDE.md`. The content is largely the same; this file exists so that whatever agent the team uses picks up the same guidance.

## Read this first

Before doing any work in this repo, read:

1. `CLAUDE.md` — full conventions, commands, restrictions, invariants
2. The relevant `packages/<name>/AGENTS.md` for the package you're working in
3. `llms.txt` — repo route map

## Quick reference

- **Verify command:** `npm run verify` (lint + typecheck + format + tests)
- **Stack:** TypeScript, Node 20+, Vitest, ESLint, Prettier, npm workspaces
- **Restricted paths:** `packages/api/src/auth/`, `packages/api/src/billing/`, `migrations/`, `infra/`, `.github/workflows/`
- **Forbidden:** see `CLAUDE.md` § Forbidden

## Plan-then-implement-then-verify

For any non-trivial change:

1. Read the relevant code and tests.
2. State your plan (what files, what changes, what tests).
3. Get approval (from the human if interactive; from the issue spec if agentic).
4. Implement.
5. Run `npm run verify`.
6. If verify fails, fix and re-verify. Don't claim done with a failing verify.

## Default to small PRs

PRs over 400 lines diff are auto-flagged for split. If your change is large, decompose it.
