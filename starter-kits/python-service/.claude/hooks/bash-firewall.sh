#!/usr/bin/env bash
# Bash firewall — blocks dangerous commands before they execute.
set -euo pipefail

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('command',''))" 2>/dev/null || echo "")

if [[ -z "$COMMAND" ]]; then
  exit 0
fi

BLOCK_PATTERNS=(
  'rm -rf /'
  'rm -rf ~'
  'rm -rf \*'
  ':(){'
  'curl.*\| *(bash|sh|python|python3)'
  'wget.*\| *(bash|sh|python|python3)'
  'dd if=.* of=/dev/'
  'mkfs'
  '> /dev/sd'
  'chmod -R 777 /'
  'chown -R'
  'git push --force.*main'
  'git push --force.*master'
  'git push -f.*main'
  'git push -f.*master'
  'pip install.*--break-system-packages'
  'twine upload'
  'python -m twine upload'
)

for pattern in "${BLOCK_PATTERNS[@]}"; do
  if echo "$COMMAND" | grep -qE "$pattern"; then
    echo "BLOCKED by bash-firewall: command matches pattern '$pattern'" >&2
    echo "If this is a genuine need, run it yourself outside the agent." >&2
    exit 2
  fi
done

if echo "$COMMAND" | grep -qE 'ENV=production|--env=production|--prod|PROD=true'; then
  echo "BLOCKED by bash-firewall: command targets production environment." >&2
  exit 2
fi

exit 0
