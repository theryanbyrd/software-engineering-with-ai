#!/usr/bin/env bash
# Protected paths hook — blocks edits to sensitive paths without explicit approval.
set -euo pipefail

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('file_path',''))" 2>/dev/null || echo "")

if [[ -z "$FILE_PATH" ]]; then
  exit 0
fi

PROTECTED_PATTERNS=(
  '\.github/workflows/'
  'src/starter/api/auth/'
  'src/starter/api/billing/'
  '/migrations/'
  '/infra/'
  'CODEOWNERS'
  '\.env'
  'pyproject\.toml'    # tooling config — needs human review
)

for pattern in "${PROTECTED_PATTERNS[@]}"; do
  if echo "$FILE_PATH" | grep -qE "$pattern"; then
    echo "BLOCKED by protected-paths: $FILE_PATH is in a restricted area." >&2
    echo "These paths require human review. Ask the user before proceeding." >&2
    exit 2
  fi
done

exit 0
