#!/usr/bin/env bash
# Post-edit format — runs ruff format + black on edited Python files.
# Best-effort; does not fail the operation if formatters are missing.
set -uo pipefail

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('file_path',''))" 2>/dev/null || echo "")

if [[ -z "$FILE_PATH" ]]; then
  exit 0
fi

case "$FILE_PATH" in
  *.py)
    if command -v ruff >/dev/null 2>&1; then
      ruff format "$FILE_PATH" >/dev/null 2>&1 || true
      ruff check --fix --quiet "$FILE_PATH" >/dev/null 2>&1 || true
    fi
    if command -v black >/dev/null 2>&1; then
      black --quiet "$FILE_PATH" >/dev/null 2>&1 || true
    fi
    ;;
esac

exit 0
