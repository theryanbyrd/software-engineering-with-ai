#!/usr/bin/env bash
# Legacy protected paths — DEFAULT-DENY for most paths.
# Reads the proposed file path from stdin.
#
# In legacy mode, the rule is inverted: paths are restricted unless explicitly
# allowed. Customize the ALLOWED list for your codebase.

set -euo pipefail

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('file_path',''))" 2>/dev/null || echo "")

if [[ -z "$FILE_PATH" ]]; then
  exit 0
fi

# Always-blocked paths (true regardless of legacy/greenfield)
HARD_BLOCKED=(
  '\.github/workflows/'
  'migrations/'
  'infra/'
  'CODEOWNERS'
  '\.env'
  'package-lock\.json'
  'yarn\.lock'
  'Gemfile\.lock'
  'poetry\.lock'
  'Cargo\.lock'
  'composer\.lock'
)

for pattern in "${HARD_BLOCKED[@]}"; do
  if echo "$FILE_PATH" | grep -qE "$pattern"; then
    echo "BLOCKED by legacy-protected-paths: $FILE_PATH is hard-blocked." >&2
    exit 2
  fi
done

# Allowlist for legacy: paths the agent IS allowed to edit
# CUSTOMIZE THIS LIST for your codebase based on Module Status table in CLAUDE.md
ALLOWLIST=(
  '^legacy-bridge-scripts/'
  '^tests/legacy-bridge/'
  '^tests/golden/'
  '^docs/'
  '^CLAUDE\.md$'
  '^AGENTS\.md$'
  '^llms\.txt$'
  # Add more allowlisted paths here as modules graduate to L1+:
  # '^api/v2/orders/'
  # '^api/v2/customer/'
)

for pattern in "${ALLOWLIST[@]}"; do
  if echo "$FILE_PATH" | grep -qE "$pattern"; then
    exit 0  # allowed
  fi
done

# Default-deny
echo "BLOCKED by legacy-protected-paths: $FILE_PATH is not in the allowlist." >&2
echo "" >&2
echo "In legacy mode, paths are restricted by default. To allow editing this path:" >&2
echo "  1. Confirm the module is at MVH Level 1+ in MVH_LEVELS.md" >&2
echo "  2. Add the path to ALLOWLIST in .claude/hooks/legacy-protected-paths.sh" >&2
echo "  3. Update the Module Status table in CLAUDE.md" >&2
echo "  4. Document why this path is now safe to edit" >&2
exit 2
