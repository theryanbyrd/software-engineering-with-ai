#!/usr/bin/env bash
# verify — the single command that gates all changes.
# Runs lint + typecheck + format check + tests, in order.
# Fails fast: stops at the first stage that fails.

set -euo pipefail

cd "$(dirname "$0")/.."

echo "▶ Lint"
npm run lint

echo "▶ Typecheck"
npm run typecheck

echo "▶ Format check"
npm run format:check

echo "▶ Tests"
npm test

echo ""
echo "✅ verify passed"
