#!/usr/bin/env bash
# Bash firewall for legacy codebase — stricter than greenfield.

set -euo pipefail

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('command',''))" 2>/dev/null || echo "")

if [[ -z "$COMMAND" ]]; then
  exit 0
fi

# Greenfield blocks (rm -rf, fork bomb, curl|sh, etc.)
GREENFIELD_BLOCKS=(
  'rm -rf /'
  'rm -rf ~'
  'rm -rf \*'
  ':(){'
  'curl.*\| *(bash|sh)'
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
)

# Legacy-extra blocks: prevent dependency upgrades, schema changes, mass refactors
LEGACY_EXTRA_BLOCKS=(
  'pip install --upgrade'
  'npm update'
  'npm install --save-dev'
  'bundle update'
  'go get -u'
  'cargo update'
  'rake db:migrate'
  'alembic upgrade'
  'flask db upgrade'
  'rails db:migrate'
  'find .* -delete'
  'find .* -exec rm'
  'sed -i.* find'
  'git checkout main --'
  'git reset --hard'
  'git push --force'
)

for pattern in "${GREENFIELD_BLOCKS[@]}" "${LEGACY_EXTRA_BLOCKS[@]}"; do
  if echo "$COMMAND" | grep -qE "$pattern"; then
    echo "BLOCKED by legacy bash-firewall: command matches pattern '$pattern'" >&2
    echo "Legacy mode is restrictive by design. Run this command yourself outside the agent if it's truly needed." >&2
    exit 2
  fi
done

if echo "$COMMAND" | grep -qE 'NODE_ENV=production|--env=production|--prod|RAILS_ENV=production'; then
  echo "BLOCKED by bash-firewall: command targets production environment." >&2
  exit 2
fi

exit 0
