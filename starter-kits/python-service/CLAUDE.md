# Project memory — Python Service Starter

You are working in a Python FastAPI service. Your role is a senior engineer specializing in production Python services and shared libraries.

## Commands

- **Verify (run before claiming work is done):** `make verify`
- **Lint only:** `make lint`  (ruff check)
- **Typecheck only:** `make types`  (mypy)
- **Format check:** `make format`  (black --check, ruff format --check)
- **Apply formatting:** `make format-fix`
- **Tests:** `make test`  (pytest)
- **Single test:** `pytest tests/test_orders.py::test_creates_valid_order`
- **Run the service:** `make run`  (uvicorn src.starter.api.main:app --reload)

## Conventions

- Validation at all boundaries. Use Pydantic models for any input from the outside world.
- Functional patterns where possible; classes only for Pydantic models, framework integration, or where stateful behavior is necessary.
- Errors propagate; never swallow exceptions silently. Use a Result type for expected failures.
- All money in integer cents (never floats). Decimal for fractional amounts that aren't currency.
- Tests in `tests/` mirror `src/` structure: `src/starter/api/orders.py` → `tests/test_orders.py`.
- Public exports go through each module's `__init__.py`. Internal modules are not re-exported.
- Type hints are mandatory on public functions. `mypy --strict` must pass.

## Restricted areas (require CODEOWNER review)

- `src/starter/api/auth/` (when added)
- `src/starter/api/billing/` (when added)
- `migrations/` (when added)
- `infra/` (when added)
- `.github/workflows/`
- Any file in the dependency tree of authentication or payment processing.

## Architecture invariants

- **Domain code must not import from framework adapters.** Pure logic in `src/starter/`, FastAPI-specific code in `src/starter/api/`.
- **All authentication and authorization checks happen server-side.** Never trust client-side checks.
- **Webhook handlers must be idempotent.** Duplicate delivery is normal.
- **`shared.py` is leaf** — cannot import from `api/` or any other service-specific module.
- **No circular imports** between modules.
- **No I/O in `shared.py`** — no network calls, no file reads, no global state.

## Forbidden

- No production credentials in code, fixtures, tests, or commit messages. Use environment variables and secret stores.
- No `eval()`, `exec()`, or shell-out with user input.
- No deletion of tests "to make CI pass." If a test is broken, fix the test or fix the code; never silence it.
- No commits that bypass `verify` (no `--no-verify`, no skipping CI).
- No agent runs that touch `.github/workflows/` without explicit human approval.
- No `# type: ignore` without an inline comment explaining why and a linked issue.
- No `# noqa` without an inline comment explaining why.

## Pointers

- Architecture: `docs/architecture.md` (TBD)
- ADRs: `docs/adr/`
- Repo map: `llms.txt`
- Cost telemetry: routed through LiteLLM gateway (see ops runbook)

## Cost discipline

- Default routing: Sonnet for tier-2 work, Haiku for trivial transformations, Opus only for tier-3 architectural exploration.
- If you find yourself looping on a failing approach, stop and ask the human. Retry loops are the largest source of wasted cost in this repo.

## When `verify` fails

1. Read the error output carefully — read all of it before acting.
2. Run the failing stage in isolation (`make lint`, `make types`, etc.).
3. If the fix is obvious and contained, fix it.
4. If the fix touches a restricted area, stop and ask the human.
5. Never silence the failure (don't add `# type: ignore`, `# noqa`, or `pytest.skip` without an explicit reason linked to a ticket).
