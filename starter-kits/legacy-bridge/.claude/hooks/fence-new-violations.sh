#!/usr/bin/env bash
# fence-new-violations.sh — the FENCE pattern.
#
# Legacy code has lots of pre-existing lint/type/style violations.
# We accept them in legacy code but block NEW violations from being added.
#
# This script runs lint/typecheck on the diff for the changed file and
# checks: are there MORE violations now than there were before?
#
# Best-effort: doesn't fail the operation, but warns loudly.

set -uo pipefail

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('file_path',''))" 2>/dev/null || echo "")

if [[ -z "$FILE_PATH" ]] || [[ ! -f "$FILE_PATH" ]]; then
  exit 0
fi

# Only check files we can lint
case "$FILE_PATH" in
  *.py|*.ts|*.tsx|*.js|*.jsx)
    ;;
  *)
    exit 0
    ;;
esac

count_violations() {
  local file="$1"
  local count=0
  
  case "$file" in
    *.py)
      if command -v ruff >/dev/null 2>&1; then
        count=$(ruff check --output-format=concise "$file" 2>/dev/null | wc -l || echo 0)
      fi
      ;;
    *.ts|*.tsx|*.js|*.jsx)
      if command -v npx >/dev/null 2>&1 && [ -f "package.json" ]; then
        count=$(npx eslint --no-color --format=compact "$file" 2>/dev/null | grep -c "Error\|Warning" || echo 0)
      fi
      ;;
  esac
  
  echo "$count"
}

# Get violation count for current (post-edit) version
current_count=$(count_violations "$FILE_PATH")

# Get the previous version from git
prev_count="?"
if command -v git >/dev/null 2>&1 && git rev-parse --git-dir >/dev/null 2>&1; then
  if git show "HEAD:$FILE_PATH" > /tmp/fence-prev-version 2>/dev/null; then
    # Use a temporary file with the same extension for accurate linting
    ext="${FILE_PATH##*.}"
    cp /tmp/fence-prev-version "/tmp/fence-prev.$ext"
    prev_count=$(count_violations "/tmp/fence-prev.$ext")
    rm -f /tmp/fence-prev-version "/tmp/fence-prev.$ext"
  fi
fi

if [ "$prev_count" = "?" ]; then
  exit 0
fi

if [ "$current_count" -gt "$prev_count" ]; then
  echo "" >&2
  echo "⚠  FENCE WARNING: This edit added new lint violations to $FILE_PATH" >&2
  echo "    Before: $prev_count violations" >&2
  echo "    After:  $current_count violations" >&2
  echo "" >&2
  echo "In legacy mode, we accept existing violations but should not add new ones." >&2
  echo "Either fix the new violations or document why they are necessary." >&2
  echo "" >&2
fi

exit 0
