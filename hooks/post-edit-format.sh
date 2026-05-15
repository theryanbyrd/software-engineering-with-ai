#!/usr/bin/env bash
# Post-edit format — runs prettier on edited TS/JS files.
# Best-effort; does not fail the operation if formatter is missing.

set -uo pipefail

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('file_path',''))" 2>/dev/null || echo "")

if [[ -z "$FILE_PATH" ]]; then
  exit 0
fi

# Only format TS/JS files.
case "$FILE_PATH" in
  *.ts|*.tsx|*.js|*.jsx|*.mjs|*.cjs)
    if command -v npx >/dev/null 2>&1; then
      npx prettier --write "$FILE_PATH" >/dev/null 2>&1 || true
    fi
    ;;
esac

exit 0
