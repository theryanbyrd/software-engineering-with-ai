# Python Service Starter — AI-Native

A fork-ready FastAPI service with a working AI engineering harness baked in. Clone, install, and `make verify` should pass.

This starter implements the patterns from chapters 6, 7, 13, 14, 15, 21, and 30 of [_Software Engineering with AI: A Practical Handbook for the Claude Code Era_](https://www.linkedin.com/in/ryanbyrd) by Ryan Byrd.

Sister starter: `../typescript-monorepo/` — same patterns, TypeScript stack.

## Quickstart

```bash
git clone <this repo> my-service
cd my-service
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
make verify     # should pass on a fresh clone
```

In Claude Code or any AGENTS.md-aware tool:

```bash
claude  # picks up CLAUDE.md, AGENTS.md, .claude/skills/, .claude/agents/, .claude/hooks/
```

## What's in the box

```
.
├── CLAUDE.md                # project memory for Claude Code
├── AGENTS.md                # cross-vendor agent guidance
├── llms.txt                 # repo route map
├── SECURITY.md              # security policy + AI tooling disclosure
├── pyproject.toml           # deps, ruff/mypy/black/pytest config
├── Makefile                 # `make verify` runs lint + typecheck + format + test
├── .claude/
│   ├── settings.json        # hooks wiring
│   ├── skills/              # 3 starter skills (Python-flavored)
│   ├── agents/              # planner, reviewer, test-writer
│   └── hooks/               # bash firewall, protected paths, post-edit format
├── .github/
│   ├── pull_request_template.md      # with AI authorship tags
│   ├── CODEOWNERS
│   ├── ISSUE_TEMPLATE/agent-ready.md
│   └── workflows/verify.yml          # CI runs verify on every PR
├── src/starter/
│   ├── shared.py            # pure utilities (formatUsd, Result type)
│   └── api/
│       ├── main.py          # FastAPI app
│       └── orders.py        # example handler with validation
├── tests/
│   ├── test_shared.py
│   └── test_orders.py
└── scripts/
    └── verify.sh            # delegates to Make
```

## Verify what verify does

```bash
make verify
# → lint    (ruff check)
# → format  (black --check, ruff format --check)
# → types   (mypy)
# → test    (pytest)
```

If any stage fails, verify exits non-zero. The CI workflow runs the same command.

## What to customize

- **`CLAUDE.md`** — your team's conventions, restricted paths, forbidden patterns.
- **`AGENTS.md`** — usually mirrors CLAUDE.md content; check both for redundancy.
- **`.claude/skills/`** — add skills for repeated tasks specific to your domain.
- **`.claude/hooks/`** — adjust the bash firewall allowlist for your tools.
- **`.github/CODEOWNERS`** — your team handles, restricted paths.
- **`src/starter/`** — replace with your actual service code.

## Run the audit on this starter to see what "good" looks like

```bash
python3 ../../scripts/ai-readiness-audit.py .
open audit-report.html
```

You should see a high score across all categories — that's the point. Use this as the baseline for what your own forks should look like before you start the harness work.

## Why FastAPI

FastAPI is the most common modern Python service framework as of 2026 and supports everything this starter cares about (typed validation via Pydantic, async, OpenAPI generation). The patterns transfer to Flask, Django, Litestar, etc. — replace `src/starter/api/main.py` with your framework of choice.

## License

MIT.
