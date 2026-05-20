# Hooks — Deterministic Enforcement

Companion to *Software Engineering with AI* by Ryan Byrd · Chapter 15 / Appendix G

Hooks are the deterministic enforcement layer beneath Claude Code. Unlike CLAUDE.md (which Claude may ignore) or skill prompts (which the model may reinterpret), hooks are executed by the harness and have no judgment about what they do. They either succeed (exit 0) or fail (exit non-zero, which Claude treats as a hard stop).

| File | Purpose | When it runs |
|---|---|---|
| [`bash-firewall.sh`](bash-firewall.sh) | Block dangerous bash commands (rm -rf /, curl piped to sh, etc.) | Pre-bash |
| [`protected-paths.sh`](protected-paths.sh) | Block edits to sensitive paths (billing/, migrations/, secrets/) | Pre-write |
| [`post-edit-format.sh`](post-edit-format.sh) | Run formatter after every edit | Post-write |

## Installation

Each hook lives in your repo's `.claude/hooks/` directory and is registered in `.claude/settings.json`:

```json
{
  "hooks": [
    {"trigger": "pre-bash", "script": ".claude/hooks/bash-firewall.sh"},
    {"trigger": "pre-write", "script": ".claude/hooks/protected-paths.sh"},
    {"trigger": "post-write", "script": ".claude/hooks/post-edit-format.sh"}
  ]
}
```

Working examples wired into starter kits: [`../starter-kits/typescript-monorepo/.claude/hooks/`](../starter-kits/typescript-monorepo/.claude/hooks/).

## Quality bar for contributing a new hook

A new hook PR must include:

1. A `_tests/<hook-name>.test.sh` that exercises both success and failure paths.
2. A documented failure mode — what does the hook NOT catch? Hooks are deterministic, not omniscient.
3. A description of the threat model the hook addresses (cite the chapter or war story it comes from).
4. Performance characteristics — if it adds more than 200ms to the edit loop, reviewers will push back.
