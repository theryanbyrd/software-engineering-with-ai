# Legacy Bridge — Brownfield Minimum Viable Harness

A starter kit for the engineer who inherited a 200K LOC codebase from 2015 and was just told to "use AI to modernize it."

This is fundamentally different from the greenfield starters. It does not assume you can run `make verify` and have it pass on day one. It assumes the opposite: that nothing currently passes, that the build is fragile, that the tests are sparse or wrong, and that the engineers who knew the code best left two years ago.

This starter implements the seven principles from chapter 11 §11.6 ("The brownfield minimum viable harness") of [_Software Engineering with AI: A Practical Handbook for the Claude Code Era_](https://www.linkedin.com/in/ryanbyrd) by Ryan Byrd.

## Read this first

> Plan for nine to twelve months to feel comfortable, not three. The teams that try to compress this end up with the worst of both worlds: slop in legacy code with no safety net.
>
> — Ch 11 §11.6

This starter exists because most AI engineering content assumes greenfield conditions that 80% of working engineers don't have. If you fork the TypeScript or Python starter into your 12-year-old Rails monolith, you will spend two weeks fighting it before you realize the assumptions don't hold.

This kit makes different assumptions:

- **You don't have full test coverage and you won't get it.**
- **Your build is held together by tribal knowledge.**
- **Some of your dependencies are end-of-life.**
- **There are subsystems nobody alive understands.**
- **You can't refactor your way out of this in a quarter.**
- **Your CEO still expects AI productivity gains.**

The brownfield bridge gives you a path from where you are to a place where AI can help, without pretending the path is short.

## The seven principles

Each is implemented as actual artifacts in this starter:

| # | Principle | Where it lives |
|---|---|---|
| 1 | Pick 1-2 high-leverage services | [`BROWNFIELD_PLAN.md`](BROWNFIELD_PLAN.md) — the selection rubric in week 1 |
| 2 | Establish a golden master | [`scripts/golden-master-record.sh`](scripts/golden-master-record.sh) |
| 3 | Build `verify` around the golden master | [`scripts/legacy-verify.sh`](scripts/legacy-verify.sh) — adapts to what you have |
| 4 | Strangler-pattern the AI work | [`.claude/skills/strangler-pattern/`](.claude/skills/strangler-pattern/) |
| 5 | Read-only AI for legacy first | [`.claude/skills/read-only-discovery/`](.claude/skills/read-only-discovery/) + [`.claude/agents/legacy-explorer.md`](.claude/agents/legacy-explorer.md) |
| 6 | AI-assisted documentation as side effect | [`.claude/skills/read-only-discovery/`](.claude/skills/read-only-discovery/) — captures Q&A as READMEs |
| 7 | Strict autonomy ceiling | [`.claude/hooks/no-l3-in-legacy.sh`](.claude/hooks/no-l3-in-legacy.sh) + heavy restricted-paths |

## Quickstart

```bash
# 1. Copy this starter into your legacy repo (additive — doesn't touch existing code)
cp -r starter-kits/legacy-bridge/.claude /path/to/your/legacy/repo/
cp -r starter-kits/legacy-bridge/scripts /path/to/your/legacy/repo/legacy-bridge-scripts/
cp starter-kits/legacy-bridge/CLAUDE.md /path/to/your/legacy/repo/CLAUDE.md
cp starter-kits/legacy-bridge/AGENTS.md /path/to/your/legacy/repo/AGENTS.md
cp starter-kits/legacy-bridge/BROWNFIELD_PLAN.md /path/to/your/legacy/repo/

# 2. Run discovery — see what's actually in the repo
cd /path/to/your/legacy/repo
bash legacy-bridge-scripts/discover.sh

# 3. Pick your first service (use the rubric in BROWNFIELD_PLAN.md)
# 4. Record the golden master for that service
bash legacy-bridge-scripts/golden-master-record.sh <service-name>

# 5. Now you have a verify command that means something
bash legacy-bridge-scripts/legacy-verify.sh <service-name>
```

In Claude Code:

```bash
claude  # picks up the brownfield-flavored CLAUDE.md, with much heavier restrictions
```

The first thing you should ask Claude:

> "Read the codebase and tell me which 2-3 services match the criteria in BROWNFIELD_PLAN.md week 1. Don't change anything. Just answer the question."

## What's different from the greenfield starters

| Greenfield starter | Legacy bridge |
|---|---|
| `verify` runs lint + typecheck + tests | `legacy-verify` runs whatever passes today + golden-master |
| Restricted paths: `auth/`, `billing/` | Restricted paths: **everything by default**, opt-in to specific modules |
| Autonomy: L2 default, L3 with review | Autonomy: **L1 (suggest only) for first 6 months** in legacy code |
| Skills: code-review, write-tests | Skills: strangler-pattern, characterize-then-refactor, read-only-discovery |
| PRs: <400 lines | PRs in legacy: <100 lines, with golden-master diff attached |
| CLAUDE.md: full conventions | CLAUDE.md: documents what's UNKNOWN as much as what's known |

## What this starter does NOT promise

- **It will not modernize your codebase.** Modernization is a multi-year program; the harness is a precondition for it.
- **It will not give you greenfield productivity in legacy.** Realistic gains in well-instrumented legacy modules are 5-8% on tier-2 work. Above that requires investment we cannot ship in a starter kit.
- **It will not make your CEO patient.** Use [`exec-kit/ceo-emails/defending-the-investment.md`](../../exec-kit/ceo-emails/defending-the-investment.md) for that conversation, and be honest about timelines.
- **It will not survive contact with a "rewrite from scratch" decision.** If your leadership is pushing for a rewrite, that's a different book and a different starter (and probably a different leadership team).

## What this starter is honest about

The brownfield approach is the harder approach. The greenfield starter takes 30 minutes to set up; this one takes weeks to bring online for any single service. The book is honest about this and so is the starter.

**This starter scores ~63% on the AI readiness audit, deliberately.** Legacy work cannot satisfy all greenfield checks (no central `verify` command, lower test density, more restricted paths). Aiming for a 92% score on a brownfield repo is wrong — it would mean smoothing over the real constraints. If your audit climbs from 63% → 75% over six months as modules graduate to higher MVH levels, that's the success metric.

Read the [BROWNFIELD_PLAN.md](BROWNFIELD_PLAN.md) before you do anything else. If the timeline doesn't work for your situation, that tells you something important about whether AI tooling is currently the right investment for your team.

## License

MIT.
