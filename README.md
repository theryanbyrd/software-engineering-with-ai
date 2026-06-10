# AI Engineering Handbook — Companion Repository

Fork-ready templates, audit scripts, and reference implementations for [_Software Engineering with AI: A Practical Handbook for the Claude Code Era_](https://www.linkedin.com/in/ryanbyrd) by Ryan Byrd.

The book is the strategic frame. This repo is the operating layer. Most of what's here takes about two hours to integrate into a typical TypeScript or Python repo. The full audit suite takes about a day to interpret. The executive-strategic-kit (board deck, ROI calculator, CEO email templates) is designed to be used the week before your next board meeting.

> ⭐ **Star if it saves you a week.** If you fork this and ship faster as a result, that's the goal. Tell me what worked and what didn't via [LinkedIn](https://www.linkedin.com/in/ryanbyrd).

---

## Quickstart — three paths

Pick the one that matches the next thing on your calendar.

### Path 1 — You're a VP of Engineering with a board meeting in 8 weeks

```bash
git clone https://github.com/theryanbyrd/software-engineering-with-ai
cd software-engineering-with-ai

# Audit your main repo to see what you're working with
python3 scripts/ai-readiness-audit.py /path/to/your/main/repo
open audit-report.html

# Then open the executive-strategic-kit
ls executive-strategic-kit/
```

Read [`executive-strategic-kit/90-day-plan.md`](executive-strategic-kit/90-day-plan.md) for the day-by-day plan. The kit has the board deck template (markdown source), the ROI calculator (markdown source), the three CEO email templates (defending the investment, pushing back on a headcount cut, the 11pm podcast clip reply), the canonical security questionnaire answers, and the vendor negotiation scripts. You should have a defensible 90-day plan by end of week.

**Read time:** 2 hours. **Time to first artifact:** same day.

### Path 2 — You're a platform / harness engineer building the foundation

```bash
git clone https://github.com/theryanbyrd/software-engineering-with-ai
cd software-engineering-with-ai

# Fork the appropriate starter kit
cp -r starter-kits/typescript-monorepo /path/to/your/new/repo
cd /path/to/your/new/repo
npm install
npm run verify  # should pass on a fresh clone
```

Then read [`skills/`](skills/), [`subagents/`](subagents/), and [`hooks/`](hooks/). Wire [`scripts/ai-readiness-audit.py`](scripts/ai-readiness-audit.py) into your CI as a GitHub Action so every PR shows a score against the book's standards. The reusable audit workflow is at [`.github/workflows/audit.yml`](.github/workflows/audit.yml) — copy it into your repo.

**Time to working harness:** 5 minutes for the starter kit. **Time to integrated CI audit:** 1 hour.

### Path 3 — You're rescuing a brownfield codebase

```bash
git clone https://github.com/theryanbyrd/software-engineering-with-ai
cd software-engineering-with-ai

# Audit the brownfield repo to see the gaps
python3 scripts/ai-readiness-audit.py /path/to/legacy/repo
```

Read [`docs/legacy-migration/`](docs/legacy-migration/) and Chapter 11 §11.6 of the book ("The brownfield minimum viable harness"). Use [`starter-kits/legacy-bridge/`](starter-kits/legacy-bridge/) as the model for what a strangler-pattern harness looks like.

**Read time:** 3 hours. **Realistic time to working brownfield harness:** 9–12 months. The brownfield problem is harder than the greenfield one. The book is honest about that; this repo is too.

---

## What's inside

The full directory tree, grouped by purpose. Three sentences per area. Click through to the per-directory README for detail.

### Run-now tools

| Directory | What's there |
|---|---|
| [`scripts/`](scripts/) | The audit script and adjacent utilities. `ai-readiness-audit.py` is the most important file in the repo — it scores any codebase against ~25 criteria from the book. Also includes `token-cost-estimator.py`, `slop-detector.py`, `pr-ai-tagger.py`, `llms-txt-generator.py`, and the `cursorrules-to-claude-md.py` migration helper. |
| [`starter-kits/`](starter-kits/) | Fork-ready scaffolds. Three first-class kits — `typescript-monorepo/`, `python-service/`, `legacy-bridge/` — each with a working CLAUDE.md, AGENTS.md, hooks, agents, skills, and a `verify` command. Fork the closest match, run `verify`, and you have a working harness in five minutes. |
| [`benchmarks/`](benchmarks/) | Golden-task evaluations. A small set of repeatable tasks used to detect regressions in models, skills, and CLAUDE.md changes. Run quarterly or on every model release. |

### Templates (book appendices)

| Directory | What's there |
|---|---|
| [`templates/`](templates/) | Single-file templates from the book's appendices. CLAUDE.md, AGENTS.md, the agent-ready issue template (Appendix C), and the PR template for AI-authored code (Appendix D). Copy-paste into a greenfield repo. |
| [`skills/`](skills/) | The twelve starter skills (Appendix E). Add API endpoint, write tests, refactor safely, code review, db migration, dependency upgrade, frontend component, incident fix, observability change, performance review, security review, bug reproduction. Each has its own README and a SKILL.md. |
| [`subagents/`](subagents/) | The starter subagent roster (Appendix F). Planner, test-writer, reviewer — each with tight role definitions, tool allowlists, and the no-self-congratulation clause (Ch 2 §2.1a). |
| [`hooks/`](hooks/) | Starter hook library (Appendix G). Bash firewall, protected-paths enforcement, post-edit format. Each comes with tests and a documented threat model. |
| [`scorecard/`](scorecard/) | The AI-readiness scorecard (Appendix H) as a fillable `ai-readiness.xlsx` — the manual counterpart to `scripts/ai-readiness-audit.py`. Same criteria, categories, and weights. |
| [`checklists/`](checklists/) | The AI code-smell checklist (Appendix I, the seven slop signatures) and the AI-generated-test review checklist (Appendix K). Print-and-keep review aids. |
| [`prompts/`](prompts/) | The prompt pattern library (Appendix J). Durable, model-portable prompt shapes: agent-ready issue, information-requirements, plan→implement→review, independent verification, slop review, task decomposition. |

### Strategic / executive

| Directory | What's there |
|---|---|
| [`executive-strategic-kit/`](executive-strategic-kit/) | The political artifacts. Board deck, ROI calculator, CEO emails, security-questionnaire answers, vendor negotiation scripts, hype-rebuttal table, 11pm-podcast-clip protocol. Designed to be used the week before your next board meeting. Markdown is the source of truth; rendered xlsx/pptx live in `rendered/` for executives who prefer those formats. |
| [`people/`](people/) | Hiring, leveling, and career-ladder materials. JD templates for AI-era roles, the re-leveled promotion rubric, performance-review extensions, and the platform-team charter. |
| [`migration-playbooks/`](migration-playbooks/) | Tool-to-tool migration runbooks. Cursor → Claude Code, Copilot → mixed stack, shadow-AI → approved stack, and the pre-migration checklist. |

### Governance / safety

| Directory | What's there |
|---|---|
| [`prompt-injection-test-suite/`](prompt-injection-test-suite/) | The six canonical prompt-injection test cases (Ch 36–37) as a runnable suite. Includes test cases, fixtures, two runner implementations, CI integration docs, and a response runbook. Run quarterly. |
| [`agent-autonomy-levels/`](agent-autonomy-levels/) | The L1–L5 autonomy ladder (Ch 32) with forbidden categories and the recommended-defaults matrix. |
| [`do-not-automate-catalog/`](do-not-automate-catalog/) | The Do-Not-Automate catalog (Ch 33) by domain. |
| [`vendor-procurement-runbook/`](vendor-procurement-runbook/) | The vendor-review checklist (Ch 38), the data-classification walkthrough, the security-review template, and the questions to ask before signing. |
| [`incident-postmortem-templates/`](incident-postmortem-templates/) | AI-aware postmortem templates (Ch 39). Failure categorization guide, the harness-deficiency checklist, the slop-attribution worksheet. |
| [`ai-coded-app-security-and-resilience/`](ai-coded-app-security-and-resilience/) | The security & resilience gaps AI-coded apps ship (Ch 36.5). Frontend-bundle secrets, misconfigured RLS, missing rate limits, silent failures, offline/throttled networks — with a paste-ready checklist and the verification gates that enforce them. |

### Measurement / metrics

| Directory | What's there |
|---|---|
| [`metrics-and-measurement-infrastructure/`](metrics-and-measurement-infrastructure/) | The six-metric dashboard spec (Ch 31). Lead time, deployment frequency, change failure rate, MTTR, failed-one-shot ratio, per-dev token spend. Includes the triage taxonomy and the predictability metric. |
| [`cost-discipline-runbook/`](cost-discipline-runbook/) | Token-cost operating procedures (Ch 26, 29). Routing discipline, retry control, cost gateway configuration, monthly forecast vs actual. |
| [`failed-one-shot-triage/`](failed-one-shot-triage/) | The four-bucket triage for failed agent attempts (Ch 22, Ch 31). Spec problem, harness problem, model problem, human problem. |
| [`evals-and-benchmarks-runbook/`](evals-and-benchmarks-runbook/) | How to design and run evaluations for your team's specific work (Ch 6 §6.5.2). |

### Workflow / culture

| Directory | What's there |
|---|---|
| [`code-review-craft-workshop/`](code-review-craft-workshop/) | The seven-slop-signatures workshop (Ch 2, Ch 22). Workshop facilitator guide, exercises, and the assessment rubric. |
| [`loop-engineering/`](loop-engineering/) | Designing the system that prompts your agents (Ch 43.7). The five building blocks (automations, worktrees, skills, connectors, sub-agents) plus memory, and a five-day plan to your first loop. |
| [`reviewer-burnout-mitigation/`](reviewer-burnout-mitigation/) | Operational patterns for managing reviewer load when generation cost drops 5x. |
| [`promotion-and-leveling-rubric/`](promotion-and-leveling-rubric/) | The AI-era leveling rubric (Ch 60). Harness contributions count for promotion; verification discipline is a leveling criterion. |
| [`junior-trajectory/`](junior-trajectory/) | How juniors grow in an AI-native team. The four-quarter trajectory and the apprenticeship pairing pattern. |
| [`solutions-engineer-and-tech-pm/`](solutions-engineer-and-tech-pm/) | Role descriptions and workflow patterns for the SE and Tech PM roles in an AI-native team. |
| [`customer-facing-ai-disclosure/`](customer-facing-ai-disclosure/) | The customer-facing AI story (Ch 56). Disclosure decision framework, AI authorship disclosure, security questionnaire answers, the customer-conversation script. |
| [`skip-level-defense/`](skip-level-defense/) | The skip-level conversation kit (Ch 61). What to say when an engineer two levels down asks if their job is safe. |

### Onboarding / curriculum

| Directory | What's there |
|---|---|
| [`ai-tooling-onboarding-curriculum/`](ai-tooling-onboarding-curriculum/) | The four-week onboarding curriculum (Ch 44). Week-by-week reading, assessments, and graduation criteria. |
| [`ai-readiness-audit-walkthrough/`](ai-readiness-audit-walkthrough/) | How to read and act on an audit report from `scripts/ai-readiness-audit.py`. |
| [`legacy-codebase-onboarding/`](legacy-codebase-onboarding/) | How to onboard new engineers (or agents) into a legacy codebase (Ch 11). |
| [`platform-team-charter/`](platform-team-charter/) | The platform team's charter — what they own, what they don't, the harness backlog (Ch 42 §42.4). |

### Reading list / war stories

| Directory | What's there |
|---|---|
| [`reading-list/`](reading-list/) | JSON-driven reading list with auto-prune. Run `scripts/generate.py` to rebuild from the source data. Stale entries are flagged weekly by [`.github/workflows/reading-list-stale.yml`](.github/workflows/reading-list-stale.yml). |
| [`war-stories/`](war-stories/) | Anonymized field reports from real adoption programs. Five stories shipped in v2026.q3; new contributions follow [`war-stories/_TEMPLATE.md`](war-stories/_TEMPLATE.md). |

### Supporting

| Directory | What's there |
|---|---|
| [`docs/`](docs/) | Longer-form guides — the 90-day playbook, legacy-migration walkthrough, measurement-dashboard wiring, certification curriculum, plugin marketplace guide. Some entries are stubbed in v2026.q3 and fill out in v2026.q4. |
| [`examples/`](examples/) | Worked end-to-end examples. [`wild-west-wanted-poster/`](examples/wild-west-wanted-poster/) — a complete greenfield AI SaaS built from scratch (domain, Terraform/AWS, Next.js app, queue worker, Stripe, Gemini, admin, freemium); the book's Ch 47 worked example. [`osticket-brownfield/`](examples/osticket-brownfield/) — the brownfield counterpart: dropping an agent into ~360k lines of legacy PHP (osTicket) to add a high-stakes feature (TOTP 2FA) with an MVH harness, characterization tests, a tiered spec, and an adversarial-review plan. |
| [`tools/`](tools/) | Reusable GitHub Actions, editor configs. |

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
Hooks (Ch 15)                  ░░░░░░░░░░  0/6   ❌
Subagents (Ch 14)              ▓▓▓░░░░░░░  3/8   ⚠️
Cost discipline (Ch 26)        ▓▓▓▓▓░░░░░  5/10  ⚠️
Governance (Ch 32-36)          ░░░░░░░░░░  0/8   ❌

Top 5 actions:
1. Add CLAUDE.md (Ch 6 §6.3) — 5 min
2. Wire pre-bash hook (Ch 15 §15.2) — 30 min
3. Define autonomy levels (Ch 32) — 1 hour
4. Add `verify` script (Ch 7 §7.2) — 1 hour
5. Configure cost gateway (Ch 29 §29.4) — 4 hours
```

The audit script also runs in CI against this repo's own starter kits — see [`.github/workflows/audit.yml`](.github/workflows/audit.yml). The starter kits currently score 88–94%; the published report is regenerated on every PR and available in the workflow artifacts.

---

## Book → folder map

| Book chapter | Lives here |
|---|---|
| Ch 2 — Slop signatures + self-congratulation | [`code-review-craft-workshop/`](code-review-craft-workshop/), [`scripts/slop-detector.py`](scripts/) |
| Ch 6 — Repo Legibility | [`templates/CLAUDE.md`](templates/), [`templates/AGENTS.md`](templates/) |
| Ch 6.6 — Testing the harness | [`benchmarks/`](benchmarks/), [`evals-and-benchmarks-runbook/`](evals-and-benchmarks-runbook/) |
| Ch 7 — Verify Command | [`starter-kits/*/scripts/verify.sh`](starter-kits/) |
| Ch 11 §11.6 — Brownfield MVH | [`starter-kits/legacy-bridge/`](starter-kits/), [`examples/osticket-brownfield/`](examples/osticket-brownfield/) |
| Ch 13 — Skills | [`skills/`](skills/), [`starter-kits/*/.claude/skills/`](starter-kits/) |
| Ch 14 — Subagents | [`subagents/`](subagents/) |
| Ch 15 — Hooks | [`hooks/`](hooks/) |
| Ch 18 — Plugins guide | [`docs/plugin-marketplace.md`](docs/plugin-marketplace.md) |
| Ch 19 — Intake pattern | [`solutions-engineer-and-tech-pm/`](solutions-engineer-and-tech-pm/) |
| Ch 22 — Code review (slop signatures) | [`scripts/slop-detector.py`](scripts/), [`code-review-craft-workshop/`](code-review-craft-workshop/) |
| Ch 26 — Cost discipline | [`scripts/token-cost-estimator.py`](scripts/), [`cost-discipline-runbook/`](cost-discipline-runbook/) |
| Ch 28 — Cost optimization with local LLMs | [`benchmarks/local-llms-current-state/`](benchmarks/local-llms-current-state/) |
| Ch 29 — Cost gateway | [`docs/measurement-dashboards/`](docs/measurement-dashboards/) |
| Ch 30 — Approved tooling matrix | [`executive-strategic-kit/approved-tooling-matrix-template.md`](executive-strategic-kit/approved-tooling-matrix-template.md) |
| Ch 31 — Metrics + attribution toolkit | [`metrics-and-measurement-infrastructure/`](metrics-and-measurement-infrastructure/) |
| Ch 32 — Autonomy ladder | [`agent-autonomy-levels/`](agent-autonomy-levels/) |
| Ch 33 — Do-Not-Automate | [`do-not-automate-catalog/`](do-not-automate-catalog/) |
| Ch 33.5 — Domains where AI is net-negative | [`do-not-automate-catalog/net-negative-domains.md`](do-not-automate-catalog/net-negative-domains.md) |
| Ch 34 — Data classification | [`executive-strategic-kit/data-classification-matrix.md`](executive-strategic-kit/data-classification-matrix.md) |
| Ch 36–37 — Prompt injection | [`prompt-injection-test-suite/`](prompt-injection-test-suite/) |
| Ch 36.5 — Security & resilience gaps in AI-coded apps | [`ai-coded-app-security-and-resilience/`](ai-coded-app-security-and-resilience/) |
| Ch 38 — Vendor risk | [`vendor-procurement-runbook/`](vendor-procurement-runbook/) |
| Ch 39 — Incident response | [`incident-postmortem-templates/`](incident-postmortem-templates/) |
| Ch 44 — Certification curriculum | [`ai-tooling-onboarding-curriculum/`](ai-tooling-onboarding-curriculum/) |
| Ch 47 — Worked end-to-end examples | [`examples/wild-west-wanted-poster/`](examples/wild-west-wanted-poster/) (greenfield), [`examples/osticket-brownfield/`](examples/osticket-brownfield/) (brownfield) |
| Ch 43.6 — The IC perspective (running agents) | [`docs/ic-perspective-running-agents.md`](docs/ic-perspective-running-agents.md) |
| Ch 43.7 — Loop engineering | [`loop-engineering/`](loop-engineering/) |
| Ch 47.5 — AI in non-coding engineering work | [`docs/ai-in-non-coding-engineering-work.md`](docs/ai-in-non-coding-engineering-work.md) |
| Ch 50.5 — What I might be wrong about | [`docs/what-i-might-be-wrong-about.md`](docs/what-i-might-be-wrong-about.md) |
| Ch 51 — 90-day plan | [`executive-strategic-kit/90-day-plan.md`](executive-strategic-kit/90-day-plan.md) |
| Ch 52 — CEO/board kit | [`executive-strategic-kit/board-deck-template.md`](executive-strategic-kit/board-deck-template.md), [`executive-strategic-kit/ceo-emails/`](executive-strategic-kit/ceo-emails/) |
| Ch 53 — Migration playbooks | [`migration-playbooks/`](migration-playbooks/) |
| Ch 54 — ROI calculator | [`executive-strategic-kit/roi-calculator.md`](executive-strategic-kit/roi-calculator.md) |
| Ch 56 — Customer security Q&A | [`executive-strategic-kit/security-questionnaire-answers.md`](executive-strategic-kit/security-questionnaire-answers.md), [`customer-facing-ai-disclosure/`](customer-facing-ai-disclosure/) |
| Ch 60 — JDs and career ladder | [`people/`](people/), [`promotion-and-leveling-rubric/`](promotion-and-leveling-rubric/) |
| Ch 61 — Skip-level defense | [`skip-level-defense/`](skip-level-defense/) |
| Appendix A — CLAUDE.md template | [`templates/CLAUDE.md`](templates/CLAUDE.md) |
| Appendix B — AGENTS.md template | [`templates/AGENTS.md`](templates/AGENTS.md) |
| Appendix C — Agent-ready issue | [`templates/agent-ready-issue.md`](templates/agent-ready-issue.md) |
| Appendix D — PR template | [`templates/pr-template.md`](templates/pr-template.md) |
| Appendix E — 12 starter skills | [`skills/`](skills/) |
| Appendix F — Subagent library | [`subagents/`](subagents/) |
| Appendix G — Hook library | [`hooks/`](hooks/) |
| Appendix H — Readiness scorecard | [`scorecard/ai-readiness.xlsx`](scorecard/) (fillable) + [`scripts/ai-readiness-audit.py`](scripts/ai-readiness-audit.py) (automated) |
| Appendix I — AI code smell checklist | [`checklists/code-smells.md`](checklists/code-smells.md) |
| Appendix J — Prompt pattern library | [`prompts/`](prompts/) |
| Appendix K — AI test review checklist | [`checklists/test-review.md`](checklists/test-review.md) |
| Appendix L — War stories (book version) | [`war-stories/`](war-stories/) |

---

## Releases and errata

Releases are quarterly: `v2026.q3`, `v2026.q4`, etc. Each release maps to a book edition in [`CHANGELOG.md`](CHANGELOG.md). Errata for the printed book also live there. Between quarterly releases, only critical fixes go to `main` — quarterly cadence is what a single maintainer can sustain.

Subscribe to releases (GitHub: Watch → Releases only) for the cadence that won't fill your inbox.

---

## Stack support

**First-class** (CI-tested every release): TypeScript, Python, Next.js (forthcoming in v2026.q4).

**Community** (forks under `starter-kits/community/`, stewarded by named contributors): Java, Spring Boot, Go, Rust, Ruby, .NET, others as contributors emerge.

The patterns transfer across stacks. The plumbing differs. Don't wait for your stack to be first-class — fork the closest match.

---

## Contributing

PRs welcome. See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the quality bar. Specific templates to start from are linked in CONTRIBUTING.md — one of:

- [`skills/_TEMPLATE.md`](skills/_TEMPLATE.md) — new skill
- [`subagents/_TEMPLATE.md`](subagents/_TEMPLATE.md) — new subagent
- [`hooks/_TEMPLATE.sh`](hooks/_TEMPLATE.sh) — new hook (forthcoming)
- [`war-stories/_TEMPLATE.md`](war-stories/_TEMPLATE.md) — new war story
- [`prompt-injection-test-suite/test-cases/_TEMPLATE.md`](prompt-injection-test-suite/test-cases/_TEMPLATE.md) — new prompt-injection test case

Quality bar (summary):

- New skills must pass `scripts/skill-linter.py` and include a working example.
- New hooks must include a `_tests/` file and a documented failure mode.
- War stories follow the template and must be anonymized.
- Reading list entries include a `last-verified` date.
- Anything that touches a book chapter cites the chapter.

---

## License

MIT. Use it. Modify it. Redistribute it. Build a business on top of it. Just don't claim you wrote the book.

---

## Attribution

This repo is the companion to a book that synthesizes a great deal of work by other people — METR, DORA, DX, Faros AI, Sonar, GitClear, Anthropic's documentation team, Jesse Vincent's Superpowers project, Birgitta Böckeler's writing, Sean Goedecke's writing, Simon Willison's writing on prompt injection, and many others credited in the book. The artifacts here are mine to share. The credit for the underlying ideas belongs to the field.

— Ryan Byrd, May 2026
