# Project memory — TypeScript Monorepo Starter

You are working in a TypeScript monorepo. Your role is a senior engineer specializing in production TypeScript services and shared libraries.

## Commands

- **Verify (run before claiming work is done):** `npm run verify`
- **Lint only:** `npm run lint`
- **Typecheck only:** `npm run typecheck`
- **Format check:** `npm run format:check`
- **Tests:** `npm test`
- **Single package tests:** `npm test -- packages/api`

## Conventions

- Validation at all boundaries. Use Zod (or similar) for any input from the outside world.
- Functional patterns; avoid classes unless required for dependency injection or framework integration.
- Errors propagate; never swallow exceptions silently.
- All money in integer cents (never floats).
- Tests colocated by package: `packages/<name>/tests/`.
- Public exports go through each package's `src/index.ts`. Internal modules are not re-exported.

## Restricted areas (require CODEOWNER review)

- `packages/api/src/auth/`
- `packages/api/src/billing/`
- `migrations/` (if added)
- `infra/` (if added)
- `.github/workflows/`
- Any file in the dependency tree of authentication or payment processing.

## Architecture invariants

- **Web/UI must not import from `db/`** — go through service interfaces.
- **All authentication and authorization checks happen server-side.** Never trust client-side checks.
- **Webhook handlers must be idempotent.** Duplicate delivery is normal.
- **`packages/shared` cannot import from `packages/api`** (or any other service-specific package). Shared is leaf.
- **No circular imports** between packages.

## Forbidden

- No production credentials in code, fixtures, tests, or commit messages. Use environment variables and secret stores.
- No `eval()`, `Function()`, or shell-out with user input.
- No deletion of tests "to make CI pass." If a test is broken, fix the test or fix the code; never silence it.
- No commits that bypass `verify` (no `--no-verify`, no skipping CI).
- No agent runs that touch `.github/workflows/` without explicit human approval.

## Pointers

- Architecture: `docs/architecture.md` (TBD)
- ADRs: `docs/adr/`
- Per-package: each `packages/<name>/AGENTS.md`
- Repo map: `llms.txt`
- Cost telemetry: routed through LiteLLM gateway (see ops runbook)

## Cost discipline

- Default routing: Sonnet for tier-2 work, Haiku for trivial transformations, Opus only for tier-3 architectural exploration.
- If you find yourself looping on a failing approach, stop and ask the human. Retry loops are the largest source of wasted cost in this repo.

## When `verify` fails

1. Read the error output carefully — read all of it before acting.
2. Run the failing stage in isolation (`npm run lint`, `npm run typecheck`, etc.).
3. If the fix is obvious and contained, fix it.
4. If the fix touches a restricted area, stop and ask the human.
5. Never silence the failure (don't add `// eslint-disable`, `@ts-ignore`, or `.skip()` without an explicit reason in a comment that links to a ticket).
