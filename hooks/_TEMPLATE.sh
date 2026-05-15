#!/usr/bin/env bash
# [hook-name].sh — [one-sentence purpose]
#
# Trigger: [pre-bash | pre-write | post-write | etc.]
# Threat model: [what attack or mistake this hook prevents]
# Performance budget: [target < 200ms; measure before merging]
#
# Exit codes:
#   0 — allow operation to proceed
#   1 — block operation (Claude treats non-zero as a hard stop)

set -euo pipefail

# Pre-write / pre-bash hooks receive context via env vars and/or stdin.
# Document what your hook reads:
#   CLAUDE_HOOK_TRIGGER  — the trigger event
#   CLAUDE_HOOK_TARGET   — the target path / command
#   (full list in Anthropic's hook documentation)

# Example: block if target matches a forbidden pattern.
TARGET="${CLAUDE_HOOK_TARGET:-}"
if [[ -z "$TARGET" ]]; then
  # No target — nothing to enforce.
  exit 0
fi

# REPLACE THIS BLOCK with the actual condition for your hook.
# if [[ "$TARGET" == *"forbidden-pattern"* ]]; then
#   echo "[$0] blocked: $TARGET matches forbidden pattern"
#   exit 1
# fi

exit 0
