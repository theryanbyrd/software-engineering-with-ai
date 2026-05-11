#!/usr/bin/env bash
# legacy-verify.sh — adaptive verify that does WHATEVER the codebase supports.
# Detects available tools and runs them. Reports clearly what was checked.
#
# Optional first argument: module name (limits scope where possible).
# Without it, runs across the whole repo.
#
# Usage:
#   bash legacy-bridge-scripts/legacy-verify.sh
#   bash legacy-bridge-scripts/legacy-verify.sh api/v1/orders

set -uo pipefail

MODULE="${1:-}"
EXIT=0
PASS=0
SKIP=0
FAIL=0

step() {
  local name="$1"
  shift
  if "$@" 2>/tmp/legacy-verify-stderr.log >/tmp/legacy-verify-stdout.log; then
    echo "  ✅ $name"
    PASS=$((PASS+1))
  else
    echo "  ❌ $name"
    sed 's/^/     /' /tmp/legacy-verify-stderr.log /tmp/legacy-verify-stdout.log | head -10
    FAIL=$((FAIL+1))
    EXIT=1
  fi
}

skip() {
  echo "  ⊘  $1 (not configured)"
  SKIP=$((SKIP+1))
}

echo "▶ Legacy verify"
[ -n "$MODULE" ] && echo "  Module: $MODULE"
echo ""

# ----- LINT -----
echo "Lint:"
if [ -f "package.json" ] && grep -q '"lint"' package.json; then
  step "npm run lint" npm run lint --silent
elif [ -f "pyproject.toml" ] && command -v ruff >/dev/null 2>&1; then
  step "ruff check" ruff check .
elif command -v rubocop >/dev/null 2>&1 && [ -f "Gemfile" ]; then
  step "rubocop" rubocop
elif command -v golangci-lint >/dev/null 2>&1 && [ -f "go.mod" ]; then
  step "golangci-lint" golangci-lint run
else
  skip "lint"
fi

# ----- TYPECHECK -----
echo "Typecheck:"
if [ -f "tsconfig.json" ]; then
  step "tsc --noEmit" npx tsc --noEmit
elif [ -f "pyproject.toml" ] && command -v mypy >/dev/null 2>&1; then
  step "mypy" mypy
else
  skip "typecheck"
fi

# ----- TESTS -----
echo "Tests:"
if [ -f "package.json" ] && grep -q '"test"' package.json; then
  step "npm test" npm test --silent
elif command -v pytest >/dev/null 2>&1 && [ -d "tests" ]; then
  if [ -n "$MODULE" ] && [ -d "tests/$MODULE" ]; then
    step "pytest $MODULE" pytest "tests/$MODULE"
  else
    step "pytest" pytest
  fi
elif command -v go >/dev/null 2>&1 && [ -f "go.mod" ]; then
  step "go test" go test ./...
elif command -v bundle >/dev/null 2>&1 && [ -f "Gemfile" ]; then
  step "bundle exec rspec" bundle exec rspec
else
  skip "tests"
fi

# ----- GOLDEN MASTER -----
echo "Golden master:"
GOLDEN_DIR="tests/golden"
if [ -n "$MODULE" ]; then
  GOLDEN_DIR="tests/golden/$MODULE"
fi
if [ -d "$GOLDEN_DIR" ] && [ -f "$GOLDEN_DIR/replay.sh" ]; then
  step "golden-master replay" bash "$GOLDEN_DIR/replay.sh"
elif [ -d "$GOLDEN_DIR" ]; then
  echo "  ⚠  golden master directory exists but no replay.sh — record one"
  SKIP=$((SKIP+1))
else
  skip "golden master"
fi

# ----- SUMMARY -----
echo ""
echo "Summary: $PASS passed, $FAIL failed, $SKIP skipped"
if [ "$FAIL" -gt 0 ]; then
  echo "FAILED."
  exit 1
fi
if [ "$PASS" -eq 0 ]; then
  echo "WARNING: nothing was actually verified. Configure at least one of: lint, typecheck, tests, golden-master."
  exit 2
fi
echo "PASSED (with $SKIP skipped)."
