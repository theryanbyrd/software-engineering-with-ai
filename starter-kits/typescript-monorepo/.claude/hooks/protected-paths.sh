#!/usr/bin/env bash
# Protected paths hook — blocks edits to sensitive paths without explicit approval.
# Reads the proposed file path from stdin (Claude Code PreToolUse hook contract for Edit/Write).

set -euo pipefail

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('file_path',''))" 2>/dev/null || echo "")

if [[ -z "$FILE_PATH" ]]; then
  exit 0
fi

# Paths that always require human approval.
PROTECTED_PATTERNS=(
  '\.github/workflows/'
  'packages/api/src/auth/'
  'packages/api/src/billing/'
  '/migrations/'
  '/infra/'
  'CODEOWNERS'
  '\.env'
  'package-lock\.json'   # auto-managed; manual edits cause drift
)

for pattern in "${PROTECTED_PATTERNS[@]}"; do
  if echo "$FILE_PATH" | grep -qE "$pattern"; then
    echo "BLOCKED by protected-paths: $FILE_PATH is in a restricted area." >&2
    echo "These paths require human review. Ask the user before proceeding." >&2
    exit 2
  fi
done

exit 0
