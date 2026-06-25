#!/usr/bin/env bash
# verify.sh — the single canonical verify command for this kit.
#
# It runs the full gate: lint, typecheck/format, and tests. For brownfield
# repos the heavy lifting is delegated to the adaptive ./legacy-verify.sh,
# which detects whatever the codebase actually supports (eslint / ruff /
# golangci-lint for lint; tsc / mypy for typecheck; pytest / jest / go test
# for tests) and runs it. Keep this file as the one command CI and humans call.
#
#   bash scripts/verify.sh            # whole repo
#   bash scripts/verify.sh api/orders # scope to a module where supported
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"

# Demonstration tests that ship with this kit (characterization examples).
if command -v pytest >/dev/null 2>&1 && [ -d "$HERE/../tests" ]; then
  echo "▶ pytest (characterization examples)"
  pytest -q "$HERE/../tests" || exit 1
fi

# Adaptive lint + typecheck + tests across the host codebase.
exec bash "$HERE/legacy-verify.sh" "$@"
