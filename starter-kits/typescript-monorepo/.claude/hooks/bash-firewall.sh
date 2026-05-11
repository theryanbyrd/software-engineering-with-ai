#!/usr/bin/env bash
# Bash firewall — blocks dangerous commands before they execute.
# Reads the proposed bash command from stdin (Claude Code PreToolUse hook contract).
# Exit 0 = allow. Exit 2 = block (Claude sees the stderr message).

set -euo pipefail

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('command',''))" 2>/dev/null || echo "")

# Empty command? Allow (Claude will fail naturally).
if [[ -z "$COMMAND" ]]; then
  exit 0
fi

# Patterns that should never run via agent.
BLOCK_PATTERNS=(
  'rm -rf /'
  'rm -rf ~'
  'rm -rf \*'
  ':(){'                    # fork bomb
  'curl.*\| *(bash|sh)'      # curl pipe to shell
  'wget.*\| *(bash|sh)'
  'dd if=.* of=/dev/'
  'mkfs'
  '> /dev/sd'
  'chmod -R 777 /'
  'chown -R'
  'git push --force.*main'
  'git push --force.*master'
  'git push -f.*main'
  'git push -f.*master'
  'npm publish'
  'pip install.*--break-system-packages'
)

for pattern in "${BLOCK_PATTERNS[@]}"; do
  if echo "$COMMAND" | grep -qE "$pattern"; then
    echo "BLOCKED by bash-firewall: command matches pattern '$pattern'" >&2
    echo "If this is a genuine need, run it yourself outside the agent." >&2
    exit 2
  fi
done

# Production environment guards.
if echo "$COMMAND" | grep -qE 'NODE_ENV=production|--env=production|--prod'; then
  echo "BLOCKED by bash-firewall: command targets production environment." >&2
  exit 2
fi

exit 0
