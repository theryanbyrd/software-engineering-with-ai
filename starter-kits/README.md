# Starter Kits

Fork-ready repos with the book's harness pre-installed: CLAUDE.md, AGENTS.md, a single `verify` command, hooks, and CI wiring. Each kit's README has a quickstart; `verify` passes on a fresh clone — if it doesn't, open an issue, because that defeats the entire point (Ch 7).

| Kit | Stack | Use when |
|---|---|---|
| [`typescript-monorepo/`](typescript-monorepo/) | TS, npm workspaces | Greenfield TS services/libraries |
| [`python-service/`](python-service/) | Python ≥3.11, FastAPI | Greenfield Python service |
| [`legacy-bridge/`](legacy-bridge/) | Stack-agnostic | Brownfield codebases — strangler-pattern harness (Ch 11) |

```bash
cp -r starter-kits/typescript-monorepo /path/to/new/repo && cd /path/to/new/repo
npm install && npm run verify
```
