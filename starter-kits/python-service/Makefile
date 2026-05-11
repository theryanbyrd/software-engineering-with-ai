.PHONY: help install verify lint format format-fix types test run clean

help:
	@echo "Targets:"
	@echo "  install      Install package with dev deps (use in a venv)"
	@echo "  verify       Run lint + format-check + types + test (the gate)"
	@echo "  lint         Ruff lint only"
	@echo "  format       Black + ruff format check (no changes)"
	@echo "  format-fix   Apply formatting"
	@echo "  types        Mypy strict typecheck"
	@echo "  test         Pytest"
	@echo "  run          Start the dev server (uvicorn)"
	@echo "  clean        Remove caches and build artifacts"

install:
	pip install -e ".[dev]"

verify: lint format types test
	@echo ""
	@echo "verify passed."

lint:
	@echo "==> ruff check"
	@ruff check src tests

format:
	@echo "==> black --check"
	@black --check src tests
	@echo "==> ruff format --check"
	@ruff format --check src tests

format-fix:
	black src tests
	ruff format src tests
	ruff check --fix src tests

types:
	@echo "==> mypy"
	@mypy src

test:
	@echo "==> pytest"
	@pytest

run:
	uvicorn starter.api.main:app --reload --port 8000

clean:
	rm -rf .ruff_cache .mypy_cache .pytest_cache build dist *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
