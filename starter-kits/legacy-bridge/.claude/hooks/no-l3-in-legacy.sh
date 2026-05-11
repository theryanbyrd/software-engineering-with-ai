#!/usr/bin/env bash
# no-l3-in-legacy.sh — refuse multi-file edits (MultiEdit, batch operations)
# in legacy paths. Single-file edits with review are the L2 ceiling.

set -euo pipefail

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('tool_name',''))" 2>/dev/null || echo "")

# Only fire on MultiEdit
if [ "$TOOL_NAME" != "MultiEdit" ]; then
  exit 0
fi

# Get the edits list and check if any path is in legacy
EDIT_PATHS=$(echo "$INPUT" | python3 -c "
import json, sys
d = json.load(sys.stdin)
edits = d.get('tool_input', {}).get('edits', [])
paths = [e.get('file_path', '') for e in edits if isinstance(e, dict)]
# Also check the top-level file_path
top = d.get('tool_input', {}).get('file_path', '')
if top:
    paths.append(top)
for p in paths:
    print(p)
" 2>/dev/null || echo "")

# Legacy directories — customize for your codebase
LEGACY_DIRS=(
  'legacy/'
  'core/'
  'old/'
  'deprecated/'
  'archive/'
  'src/legacy/'
  'lib/legacy/'
)

for path in $EDIT_PATHS; do
  for legacy_dir in "${LEGACY_DIRS[@]}"; do
    if echo "$path" | grep -qE "^${legacy_dir}"; then
      echo "BLOCKED by no-l3-in-legacy: $path is in legacy module." >&2
      echo "Legacy modules are restricted to L1 (suggest only) or L2 (single-file edits with review)." >&2
      echo "Use Edit instead of MultiEdit. One file at a time. Each gets reviewed." >&2
      exit 2
    fi
  done
done

exit 0
