# Failed One-Shot Triage

The Train/Opportunity/Question/Score categorization for failed agent invocations. Direct implementation of Chapter 19 §19.5 ("course corrections as tickets") and Chapter 31 §31.5 ("the seventh metric: failed-one-shot triage ratios") of [_Software Engineering with AI: A Practical Handbook for the Claude Code Era_](https://www.linkedin.com/in/ryanbyrd) by Ryan Byrd, with the retro discipline from Ch 44 §44.4 item 4.

The book's framing:

> Triaging failed one-shots into these four buckets is the single highest-leverage practice for improving an AI-native engineering team's throughput. Do it weekly during retro. Do not let "the AI failed" become the permanent shrug.
>
> — Ch 19 §19.5

This folder operationalizes the discipline.

## What's in here

| File | Purpose |
|---|---|
| [`README.md`](README.md) | Overview, the four buckets, why this discipline matters |
| [`the-four-buckets.md`](the-four-buckets.md) | Train / Opportunity / Question / Score with full descriptions |
| [`triage-process.md`](triage-process.md) | The actual triage workflow — when, how, by whom |
| [`weekly-retro-structure.md`](weekly-retro-structure.md) | The retro section that runs the triage |
| [`tracking-spreadsheet-template.md`](tracking-spreadsheet-template.md) | The shared spreadsheet structure (Ch 31 §31.5: "do not bother building elaborate tooling") |
| [`reading-the-ratios.md`](reading-the-ratios.md) | What the ratios mean over time and what to do about them |
| [`closing-the-loop.md`](closing-the-loop.md) | What happens after triage — turning each bucket into action |

## The four buckets (Ch 19 §19.5 verbatim)

> 1. **Score** — the agent succeeded. Note the tier, the model, the time, the cost. This is your evidence of where the system works.
> 2. **Question** — the failure is a genuine "jagged edge" of current AI capability. The model can't yet do this kind of work reliably regardless of how good the spec is. Flag it; revisit at the next model release; in the meantime, route this work to humans.
> 3. **Opportunity** — the failure was caused by a missing piece of the codebase (an undocumented module, a missing fixture, a contract the agent couldn't find). This becomes a *legibility ticket*: improve the AGENTS.md, add a README, add a fixture, add an ADR. The harness improves; the next attempt at this kind of work succeeds.
> 4. **Train** — the failure was caused by a slop spec, full stop. The PM didn't articulate what they actually wanted. This becomes a *coaching loop*: the assistant flags the gap, the PM upgrades the spec, the team's general spec quality rises over time.

## Why this matters

Per Ch 31 §31.5:

> The ratios over time are the team's harness-maturity signal. A team that is improving will see Train and Opportunity counts fall over months as PMs sharpen and harnesses fill in gaps. Question counts fall stepwise when new models drop. Score counts rise. A team that is stagnating sees the same Train/Opportunity mix month after month — usually because nobody is closing the loop on the failures.

The diagnostic value:
- **Mostly Train** → the issue is Direction (Ch 5). PMs need help with spec quality.
- **Mostly Opportunity** → the issue is Architecture/Legibility (Part II). The harness is missing context.
- **Mostly Question** → the issue is model selection or scope mismatch (Ch 26). Routing or work-type problem.
- **Mostly Score** → the team is working well. Use the saved time to raise autonomy ceiling for that work type (Ch 32, 44).

Without the triage discipline, "the AI failed" becomes the permanent shrug. With it, every failure becomes a specific action — a spec coaching, a harness improvement, a routing fix, or a successful pattern to celebrate.

## Who this is for

- **Engineering managers** running weekly retros
- **Tech leads** advocating for harness improvements
- **PMs** receiving Train coaching feedback
- **Platform team** owning Opportunity work
- **VP of Engineering / CTO** reading the ratios as a leading indicator

## Read first

- Ch 19 §19.5 — proportional rigor and the four buckets
- Ch 31 §31.5 — the seventh metric (ratios over time)
- Ch 44 §44.4 item 4 — "Run the failed-one-shot triage every retro"
- `cost-discipline-runbook/` — adjacent (cost data informs Question vs Opportunity distinction)
- `incident-postmortem-templates/` — adjacent (some failures escalate to postmortems)

## What this folder WILL do

- Establish the four-bucket vocabulary across the team
- Provide the weekly retro structure that runs the triage
- Surface harness gaps systematically (the Opportunity bucket)
- Surface spec quality issues systematically (the Train bucket)
- Build the trend data that distinguishes maturing teams from stagnating ones

## What this folder will NOT do

- Will not work without retro discipline. If the retro doesn't run, the triage doesn't run.
- Will not work as a one-time exercise. The value compounds over weeks; expecting immediate ROI undersells it.
- Will not protect against managers who use it punitively. The triage is harness-focused, not engineer-focused; misuse destroys it.
- Will not eliminate failures. AI failures are normal; the discipline is to learn from them.

## How this folder fits with adjacent material

| Need | Where to look |
|---|---|
| The metric this informs | Ch 31 §31.5 (the seventh metric) |
| Spec quality discipline (Train bucket fix) | Ch 19; `ai-tooling-onboarding-curriculum/` |
| Harness improvements (Opportunity bucket fix) | `starter-kits/`; `governance/`; `skills/` |
| Routing changes (Question bucket fix) | `cost-discipline-runbook/model-routing-rubric.md`; `evals-and-benchmarks-runbook/` |
| Reviewer burnout (related stress on the system) | `reviewer-burnout-mitigation/` |

## The cadence

Weekly. Per Ch 31 §31.5: "Capture this in the standup or weekly review. Do not bother building elaborate tooling for it; a shared spreadsheet works."

The discipline is in the triage itself, not the surface area of the tracking. Don't gold-plate the system.

## Companion artifacts

- `cost-discipline-runbook/` — adjacent (some Question failures are routing failures)
- `evals-and-benchmarks-runbook/` — adjacent (Question failures inform model selection)
- `reviewer-burnout-mitigation/` — adjacent (related stress on the team)
- `incident-postmortem-templates/` — adjacent (some failures escalate)
- Ch 19 §19.5, Ch 31 §31.5, Ch 44 §44.4 item 4 — sources
