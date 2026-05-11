# TypeScript Monorepo Starter — AI-Native

A fork-ready TypeScript monorepo with a working AI engineering harness baked in. Clone, install, and `npm run verify` should pass.

This starter implements the patterns from chapters 6, 7, 13, 14, 15, 21, and 30 of [_Software Engineering with AI: A Practical Handbook for the Claude Code Era_](https://www.linkedin.com/in/ryanbyrd) by Ryan Byrd.

## Quickstart

```bash
git clone <this repo> my-app
cd my-app
npm install
npm run verify     # should pass on a fresh clone
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
├── .claude/
│   ├── settings.json        # hooks wiring
│   ├── skills/              # 3 starter skills
│   ├── agents/              # planner, reviewer, test-writer
│   └── hooks/               # bash firewall, protected paths, post-edit format
├── .github/
│   ├── pull_request_template.md      # with AI authorship tags
│   ├── CODEOWNERS
│   ├── ISSUE_TEMPLATE/agent-ready.md
│   └── workflows/verify.yml          # CI runs verify on every PR
├── packages/
│   ├── api/                 # example service with tests
│   └── shared/              # example shared library
├── scripts/
│   └── verify.sh            # runs lint + typecheck + test
└── package.json             # workspace config + verify script
```

## Verify what verify does

```bash
npm run verify
# → lint (eslint)
# → typecheck (tsc --noEmit)
# → format check (prettier --check)
# → test (vitest run)
```

If any stage fails, verify exits non-zero. The CI workflow runs the same command.

## What to customize

- **`CLAUDE.md`** — your team's conventions, restricted paths, forbidden patterns.
- **`AGENTS.md`** — usually mirrors CLAUDE.md content; check both for redundancy.
- **`.claude/skills/`** — add skills for repeated tasks specific to your domain.
- **`.claude/hooks/`** — adjust the bash firewall allowlist for your tools.
- **`.github/CODEOWNERS`** — your team handles, restricted paths.
- **`packages/`** — replace with your actual packages.

## Run the audit on this starter to see what "good" looks like

```bash
python3 ../../scripts/ai-readiness-audit.py .
open audit-report.html
```

You should see a high score across all categories — that's the point. Use this score as the baseline for what your own forks should look like before you start the harness work.

## License

MIT.
