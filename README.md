# AI Engineering Handbook — Companion Repository

Fork-ready templates, audit scripts, and reference implementations for [_Software Engineering with AI: A Practical Handbook for the Claude Code Era_](https://www.linkedin.com/in/ryanbyrd) by Ryan Byrd.

The book is the strategic frame. This repo is the operating layer. Most of what's here takes about two hours to integrate into a typical TypeScript or Python repo. The full audit suite takes about a day to interpret. The exec kit (board deck, ROI calculator, CEO email templates) is designed to be used the week before your next board meeting.

> ⭐ **Star if it saves you a week.** If you fork this and ship faster as a result, that's the goal. Tell me what worked and what didn't via [LinkedIn](https://www.linkedin.com/in/ryanbyrd).

---

## Quickstart — three paths

Pick the one that matches the next thing on your calendar.

### Path 1 — You're a VP of Engineering with a board meeting in 8 weeks

```bash
git clone https://github.com/ryanbyrd/ai-engineering-handbook
cd ai-engineering-handbook

# Audit your main repo to see what you're working with
python3 scripts/ai-readiness-audit.py /path/to/your/main/repo
open audit-report.html

# Then open the exec kit
ls exec-kit/
```

Read [`docs/90-day-vp-playbook/`](docs/90-day-vp-playbook/) for the day-by-day plan. The exec kit has the board deck template, the ROI calculator, the three CEO email templates (defending the investment, pushing back on a headcount cut, the 11pm podcast clip reply), the canonical security questionnaire answers, and the vendor negotiation scripts. You should have a defensible 90-day plan by end of week.

**Read time:** 2 hours. **Time to first artifact:** same day.

### Path 2 — You're a platform / harness engineer building the foundation

```bash
git clone https://github.com/ryanbyrd/ai-engineering-handbook
cd ai-engineering-handbook

# Fork the appropriate starter kit
cp -r starter-kits/typescript-monorepo /path/to/your/new/repo
cd /path/to/your/new/repo
npm install
npm run verify  # should pass on a fresh clone
```

Then read [`skills/`](skills/), [`agents/`](agents/), and [`hooks/`](hooks/). Wire `scripts/ai-readiness-audit.py` into your CI as a GitHub Action so every PR shows a score against the book's standards.

**Time to working harness:** 5 minutes for the starter kit. **Time to integrated CI audit:** 1 hour.

### Path 3 — You're rescuing a brownfield codebase

```bash
git clone https://github.com/ryanbyrd/ai-engineering-handbook
cd ai-engineering-handbook

# Audit the brownfield repo to see the gaps
python3 scripts/ai-readiness-audit.py /path/to/legacy/repo
```

Read [`docs/legacy-migration/`](docs/legacy-migration/) and Chapter 11 §11.6 of the book ("The brownfield minimum viable harness"). Use [`starter-kits/legacy-bridge/`](starter-kits/legacy-bridge/) as the model for what a strangler-pattern harness looks like.

**Read time:** 3 hours. **Realistic time to working brownfield harness:** 9-12 months. The brownfield problem is harder than the greenfield one. The book is honest about that; this repo is too.

---

## Run the audit on your repo right now

```bash
python3 scripts/ai-readiness-audit.py /path/to/your/repo
open audit-report.html
```

You'll get a scored report against ~25 criteria from the book, grouped by category, with a list of concrete next actions and chapter references. Sample output:

```
AI Readiness Audit — /Users/you/your-repo
Score: 14.5 / 50 (29%)

Repo legibility (Ch 6)         ▓▓░░░░░░░░  2/8   ❌
Verify command (Ch 7)          ▓▓▓▓▓▓░░░░  6/10  ⚠️
Test discipline (Ch 8)         ▓▓▓▓▓▓▓▓░░  4/5   ✅
Harness (Ch 13-15)             ░░░░░░░░░░  0/12  ❌
PR discipline (Ch 21)          ▓▓░░░░░░░░  1/5   ❌
Governance (Ch 30, 34)         ▓░░░░░░░░░  1/10  ❌

Top 5 things to do this week:
1. Create CLAUDE.md at repo root              (Ch 6, Appendix A)
2. Define a `verify` script in package.json   (Ch 7)
3. Create .github/pull_request_template.md    (Appendix D)
4. Add SECURITY.md with AI tooling policy     (Ch 30)
5. Set up .claude/skills/ directory           (Ch 13, Appendix E)

Full report: audit-report.html
```

To run this in CI on every PR:

```yaml
# .github/workflows/ai-readiness.yml
name: AI Readiness Audit
on: [pull_request]
jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: |
          curl -sL https://raw.githubusercontent.com/ryanbyrd/ai-engineering-handbook/main/scripts/ai-readiness-audit.py -o audit.py
          python3 audit.py . --threshold 60 --json > audit.json
      - uses: actions/upload-artifact@v4
        with: { name: audit-report, path: audit-report.html }
```

---

## Book-to-folder map

| Book chapter | Lives here |
|---|---|
| Ch 6 — Repo Legibility | [`templates/CLAUDE.md`](templates/), [`templates/AGENTS.md`](templates/) |
| Ch 7 — Verify Command | [`starter-kits/*/scripts/verify.sh`](starter-kits/) |
| Ch 11 §11.6 — Brownfield MVH | [`starter-kits/legacy-bridge/`](starter-kits/) |
| Ch 13 — Skills | [`skills/`](skills/), [`starter-kits/*/`.claude/skills/`](starter-kits/) |
| Ch 14 — Subagents | [`agents/`](agents/) |
| Ch 15 — Hooks | [`hooks/`](hooks/) |
| Ch 18 — Plugins guide | [`docs/plugin-marketplace.md`](docs/) |
| Ch 22 — Code review (slop signatures) | [`scripts/slop-detector.py`](scripts/) |
| Ch 26 — Cost discipline | [`scripts/token-cost-estimator.py`](scripts/) |
| Ch 29 — Cost gateway | [`docs/measurement-dashboards/litellm-compose/`](docs/) |
| Ch 30 — Approved tooling matrix | [`exec-kit/approved-tooling-matrix-template.xlsx`](exec-kit/) |
| Ch 31 — Metrics + attribution toolkit | [`docs/measurement-dashboards/`](docs/) |
| Ch 34 — Data classification | [`exec-kit/data-classification-matrix.xlsx`](exec-kit/) |
| Ch 36-37 — Prompt injection | [`governance/prompt-injection-test-suite/`](governance/) |
| Ch 39 — Incident response | [`governance/ai-incident-response-runbook.md`](governance/) |
| Ch 44 — Certification curriculum | [`docs/certification-curriculum/`](docs/) |
| Ch 51 — 90-day plan | [`docs/90-day-vp-playbook/`](docs/) |
| Ch 52 — CEO/board kit | [`exec-kit/board-deck-template.pptx`](exec-kit/), [`exec-kit/ceo-emails/`](exec-kit/) |
| Ch 53 — Migration playbooks | [`migration-playbooks/`](migration-playbooks/) |
| Ch 54 — ROI calculator | [`exec-kit/roi-calculator.xlsx`](exec-kit/) |
| Ch 56 — Customer security Q&A | [`exec-kit/security-questionnaire-answers.md`](exec-kit/) |
| Ch 60 — JDs and career ladder | [`people/`](people/) |
| Appendix A — CLAUDE.md template | [`templates/CLAUDE.md`](templates/) |
| Appendix B — AGENTS.md template | [`templates/AGENTS.md`](templates/) |
| Appendix C — Agent-ready issue | [`templates/agent-ready-issue.md`](templates/) |
| Appendix D — PR template | [`templates/pr-template.md`](templates/) |
| Appendix E — 12 starter skills | [`skills/`](skills/) |
| Appendix F — Subagent library | [`agents/`](agents/) |
| Appendix G — Hook library | [`hooks/`](hooks/) |
| Appendix H — Readiness scorecard | [`scripts/ai-readiness-audit.py`](scripts/ai-readiness-audit.py) |
| Appendix L — War stories | [`war-stories/`](war-stories/) |

---

## Repo structure

```
ai-engineering-handbook/
├── README.md                    ← you are here
├── CHANGELOG.md                 ← errata + release notes tied to book editions
├── CONTRIBUTING.md
├── LICENSE                      ← MIT
│
├── starter-kits/                ← fork these as your new project base
│   ├── typescript-monorepo/     ← first-class, CI-tested
│   ├── python-service/          ← first-class
│   ├── nextjs-app/              ← first-class
│   ├── legacy-bridge/           ← brownfield MVH (Ch 11.6)
│   └── community/               ← Java, Go, Rust, etc. with named stewards
│
├── templates/                   ← copy-paste single files (book appendices)
├── skills/                      ← the 12 starter skills
├── agents/                      ← subagent roster
├── hooks/                       ← bash-firewall, protected-paths, etc. (+ tests)
│
├── scripts/                     ← runnable tools
│   ├── ai-readiness-audit.py    ← THE audit. Run this first.
│   ├── token-cost-estimator.py
│   ├── slop-detector.py         ← seven slop signatures from Ch 22
│   ├── pr-ai-tagger.py
│   ├── llms-txt-generator.py
│   └── cursorrules-to-claude-md.py   ← migration helper
│
├── benchmarks/                  ← golden tasks for regression-testing models
├── docs/                        ← guides, dashboards, playbooks
├── exec-kit/                    ← board deck, ROI calc, CEO emails, vendor scripts
├── governance/                  ← incident response, prompt injection tests
├── people/                      ← JDs, career ladder, perf review extensions
├── migration-playbooks/         ← Cursor→CC, Copilot→mixed
├── reading-list/                ← live, dated, JSON + generator
├── war-stories/                 ← anonymized, community-contributed
├── examples/                    ← working repos that use the kit
└── tools/                       ← GH Actions, editor configs
```

---

## Releases and errata

Releases are quarterly: `v2026.q3`, `v2026.q4`, etc. Each release maps to a book edition in `CHANGELOG.md`. Errata for the printed book also live there. Between quarterly releases, only critical fixes go to `main` — quarterly cadence is what a single maintainer can sustain.

Subscribe to releases (GitHub: Watch → Releases only) for the cadence that won't fill your inbox.

---

## Stack support

**First-class** (CI-tested every release): TypeScript, Python, Next.js.

**Community** (forks under `starter-kits/community/`, stewarded by named contributors): Java, Spring Boot, Go, Rust, Ruby, .NET, others as contributors emerge.

The patterns transfer across stacks. The plumbing differs. Don't wait for your stack to be first-class — fork the closest match.

---

## Contributing

PRs welcome. See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the quality bar:

- New skills must pass `scripts/skill-linter.py` and include a working example.
- New hooks must include a `_tests/` file and a documented failure mode.
- War stories follow the [template](war-stories/_TEMPLATE.md) and must be anonymized.
- Reading list entries include a `last-verified` date.
- Anything that touches a book chapter cites the chapter.

---

## License

MIT. Use it. Modify it. Redistribute it. Build a business on top of it. Just don't claim you wrote the book.

---

## Attribution

This repo is the companion to a book that synthesizes a great deal of work by other people — METR, DORA, DX, Faros AI, Sonar, GitClear, Anthropic's documentation team, Jesse Vincent's Superpowers project, Birgitta Böckeler's writing, Sean Goedecke's writing, Simon Willison's writing on prompt injection, and many others credited in the book. The artifacts here are mine to share. The credit for the underlying ideas belongs to the field.

— Ryan Byrd, May 2026
