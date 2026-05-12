# Review Prompts — Agent-Driven Review Templates

Prompts that drive an AI reviewer subagent to scan PRs for the seven slop signatures. Drop into `.claude/commands/` as slash commands (`/review`, `/security-review`), or wire into a CI pre-merge check.

Per Ch 22 §22.3:

> 1. **Automated tier:** AI reviewer subagent runs on every PR. Outputs structured findings. Cheap (Sonnet 4.6 or Haiku 4.5 for short PRs).
> 2. **Human tier:** Always required. The human reads the diff, runs the code locally if it's non-trivial, asks the author to explain anything unclear.
>
> The AI reviewer is a floor, not a ceiling. Never let an AI-only review approve a merge to main.

These prompts are the floor. The human is the ceiling. Workshop attendees train to *be* the ceiling; these prompts let the floor catch the routine cases so the ceiling can focus on the structural ones.

## What's in here

| File | Purpose |
|---|---|
| [`general-review.md`](general-review.md) | The default reviewer — scans for all seven signatures, structured output |
| [`security-review.md`](security-review.md) | The security-focused reviewer — runs on auth/billing/PII/crypto paths, deeper on S4 and S5 |

Additional prompts (test-review, validation-review, migration-review) will land in batches as field-tested versions are validated.

## How to use these

### As a slash command

Copy the prompt body into `.claude/commands/review.md` (or `security-review.md`). Then in any session:

```
/review
```

Claude Code reads the local diff (typically `git diff main...HEAD`) and produces a structured findings report.

### As a CI subagent

For automated review on PR open, wire the prompt into a subagent that runs on the PR event. The Anthropic Analytics API or the Anthropic Batch API are both viable; pick whichever your team's CI uses. The agent reads the diff, runs the prompt, and posts the findings as a PR comment.

Per Ch 26 §26.1, the model selection:

| PR characteristic | Model |
|---|---|
| Short PR, low-stakes path | Haiku 4.5 |
| Standard PR | Sonnet 4.6 |
| Security/billing/auth path | Opus 4.7 — per Ch 26 §26.1, "Security review — Opus 4.7 — recall and instruction-following" |

The cost discipline is documented in [`../../cost-discipline-runbook/`](../../cost-discipline-runbook/).

### As a Codex CLI sandbox reviewer

Per Ch 2 §2.4:

> Use a read-only AI reviewer agent as a second opinion, not a substitute for human review. Codex CLI in `--sandbox read-only` is a reasonable choice for this; so is a `/review` skill in Claude Code.

The prompts here work in both. Codex's `--sandbox read-only` mode is appropriate if your team standardizes on it; the prompts are model-portable.

## What these prompts will NOT do

- **Approve a PR.** The AI reviewer reports findings. Approval is a human decision per Ch 22 §22.3. The team's CI gating should never permit an AI-only approval.
- **Replace the human reviewer.** Per Ch 22 §22.3, the agent is a floor. A team that uses AI review to skip human review is shipping AI slop on the AI's own approval. The book is unambiguous: this is the bad pattern.
- **Catch what's missing.** AI reviewers are better at flagging what's *present* (a suspicious `try/catch`, a regex that got shorter) than what's *absent* (a missing security decorator). S5 is hardest for AI reviewers; humans must own that signature most.
- **Reason about the team's specific conventions.** The prompts ground on the seven signatures from Ch 22 §22.2, which are language-agnostic. Team-specific conventions (your naming rules, your error-handling style) should be added in your `CLAUDE.md` / `AGENTS.md`, which the prompts reference.

## Tuning the prompts

The prompts in this directory are general. Tune them for your team:

1. **Reference your CLAUDE.md.** Add a line like "Apply the conventions in `CLAUDE.md` and `AGENTS.md` in this repo. If the diff diverges from those conventions, flag the divergence as a finding."
2. **Reference your Tier-1 paths.** Per [`../../do-not-automate-catalog/tier-1-never-autonomous.md`](../../do-not-automate-catalog/tier-1-never-autonomous.md), enumerate the paths that get extra scrutiny.
3. **Calibrate against your calibration set.** Per [`../calibration-set.md`](../calibration-set.md), run the prompts against your calibration diffs and compare to the reference comments. Tune until the agent's findings align with the senior reviewer's findings.
4. **Eval the prompt.** Per [`../../evals-and-benchmarks-runbook/`](../../evals-and-benchmarks-runbook/), the prompts are themselves eval-able artifacts. Build the eval; refine the prompt; ship it.

## When the AI reviewer disagrees with you

A common pattern: the agent flags a finding the human reviewer disagrees with. Three responses:

1. **Agent is right; human was about to miss.** The agent caught something subtle. Thank the floor for being a floor.
2. **Agent is wrong; flagging a non-smell.** Add the false positive to the prompt's known-anti-patterns section. The prompt gets sharper over time.
3. **Both are reasonable; team needs to decide.** Bring it to the code-review office hours per [`../../reviewer-burnout-mitigation/mitigation-4-review-office-hours.md`](../../reviewer-burnout-mitigation/mitigation-4-review-office-hours.md). The discussion calibrates the team's standard.

Per Ch 22 §22.3, the AI's findings are inputs to the human review, not substitutes.

## Companion artifacts

- [`../ai-code-smell-checklist.md`](../ai-code-smell-checklist.md) — the signatures the prompts ground on
- [`../facilitator-guide.md`](../facilitator-guide.md) — the workshop where engineers learn to surpass the AI reviewer
- [`../../starter-kits/`](../../starter-kits/) — the `/review` slash commands and hooks that wire these into CI
- [`../../evals-and-benchmarks-runbook/`](../../evals-and-benchmarks-runbook/) — how to evaluate these prompts as artifacts
- [`../../reviewer-burnout-mitigation/mitigation-1-ai-reviewer-subagent.md`](../../reviewer-burnout-mitigation/mitigation-1-ai-reviewer-subagent.md) — the operational role this fills
- Ch 22 §22.3, Ch 26 §26.1 — sources
