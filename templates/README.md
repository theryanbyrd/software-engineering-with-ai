# Templates — Copy-paste single files (Book Appendices A–D)

This directory holds the canonical single-file templates referenced in the book's appendices. Each file is intended to be copied into a new repository as a starting point and then customized.

| File | Maps to | Purpose |
|---|---|---|
| [`CLAUDE.md`](CLAUDE.md) | Appendix A | Project memory for Claude Code — universally-applicable rules |
| [`AGENTS.md`](AGENTS.md) | Appendix B | Cross-vendor agent instructions (Codex, Cursor, Devin, etc.) |
| [`agent-ready-issue.md`](agent-ready-issue.md) | Appendix C | Ticket structure for issues an agent will implement |
| [`pr-template.md`](pr-template.md) | Appendix D | PR description template for AI-authored code |

Working examples of all four templates customized to a real stack live in [`../starter-kits/typescript-monorepo/`](../starter-kits/typescript-monorepo/) and [`../starter-kits/python-service/`](../starter-kits/python-service/). When the templates here disagree with the starter kit, the starter kit is the canonical source — these standalone files are meant for copy-paste into greenfield repos.

## How to use

1. Read the book's Appendix A–D (and Chapter 6 for context on what CLAUDE.md and AGENTS.md should and shouldn't contain).
2. Copy the relevant file into your repository's root.
3. Customize the bracketed `[PLACEHOLDER]` sections.
4. Run [`../scripts/ai-readiness-audit.py`](../scripts/ai-readiness-audit.py) against your repo and iterate.
