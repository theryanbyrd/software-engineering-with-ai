# Executive / Strategic Kit

The political and strategic artifacts for AI engineering at the executive level: scripts, framing, case studies, calculators, decks. Direct implementation of Chapter 46 (managing hyped expectations), Chapter 47 (worked end-to-end examples as case studies), Chapter 51 (the 90-day plan), Chapter 52 (the CEO and board conversation kit), Chapter 54 (mid-size economics), and Chapter 56 (the customer-facing AI story) of [_Software Engineering with AI: A Practical Handbook for the Claude Code Era_](https://www.linkedin.com/in/ryanbyrd) by Ryan Byrd.

This folder is the script library. Adapt to your voice; do not skip the prep.

> Edition note: The legacy top-level `executive-strategic-kit/` folder has been merged into this directory. Binary deliverables (xlsx, pptx) now exist in `rendered/` alongside agent-readable markdown sources of the same content. Edit the markdown, regenerate the binary if you need it. The markdown is the source of truth.

## What's in here

### Strategic narratives and scripts (Ch 46, 47, 52)

| File | Purpose |
|---|---|
| [`realistic-roi-message.md`](realistic-roi-message.md) | The honest-numbers message for boards and executives |
| [`hype-rebuttal-table.md`](hype-rebuttal-table.md) | When the CEO read a Dario interview — line-by-line responses |
| [`eleven-pm-podcast-clip-protocol.md`](eleven-pm-podcast-clip-protocol.md) | What to do when an executive forwards you a podcast clip at 11pm |
| [`honest-internal-message-to-engineers.md`](honest-internal-message-to-engineers.md) | The internal message that does not lie about the rollout |
| [`pushing-back-on-headcount-cut.md`](ceo-emails/pushing-back-on-headcount-cut.md) | Email template for declining the "50% reduction by Q4" ask |
| [`defending-the-investment.md`](ceo-emails/defending-the-investment.md) | Email template for justifying the investment |
| [`podcast-clip-reply.md`](ceo-emails/podcast-clip-reply.md) | Reply template for the forwarded podcast clip |
| [`worked-examples-as-case-studies.md`](worked-examples-as-case-studies.md) | Two case studies you can adapt as your own |
| [`what-number-do-i-commit-to.md`](what-number-do-i-commit-to.md) | The single most-asked exec question |
| [`four-slide-board-deck-walkthrough.md`](four-slide-board-deck-walkthrough.md) | How to talk through the four-slide board update |

### Decks, calculators, matrices (Ch 30, 34, 52, 54)

| File | Use when | Chapter |
|---|---|---|
| [`90-day-plan.md`](90-day-plan.md) | Day 0 of your AI rollout | Ch 51 |
| [`board-deck-template.md`](board-deck-template.md) | Week before your next board meeting | Ch 52 §52.1 |
| [`all-hands-deck-template.md`](all-hands-deck-template.md) | Week 2 all-hands during rollout | Ch 51 §51.3 |
| [`roi-calculator.md`](roi-calculator.md) | Defending the investment to CFO | Ch 54 §54.5 |
| [`data-classification-matrix.md`](data-classification-matrix.md) | Security review with customer | Ch 34, Ch 56 |
| [`approved-tooling-matrix-template.md`](approved-tooling-matrix-template.md) | CISO countersign at Week 1 | Ch 30 |
| [`security-questionnaire-answers.md`](security-questionnaire-answers.md) | Customer security questionnaire arrives | Ch 56 |
| [`vendor-negotiation-scripts.md`](vendor-negotiation-scripts.md) | 60–120 days before vendor renewal | Ch 54 §54.11 |

### Binary renders (optional)

The [`rendered/`](rendered/) subdirectory contains pptx and xlsx versions of the decks and calculators for executives who prefer those formats. **The markdown above is the source of truth** — if you change the model or message, change the markdown and re-render. Do not edit the binaries directly; agents cannot read them and humans cannot diff them.

## How to use this kit

1. **Read the book first** — the kit assumes you've read Part VIII (Chapters 51–61).
2. **Adapt to your voice** — these are templates, not scripts. Use them as a starting point, not as a verbatim source.
3. **Run through `realistic-roi-message.md` before any board meeting** — the most common failure mode is committing to numbers in writing that you can't sustain.
4. **Save your own versions in a private fork** — the templates here will get more strict over time; your edits should not be lost.

## Errata and updates

If you find a template that no longer reflects current reality (vendor terms changed, industry data shifted), open an issue at github.com/theryanbyrd/software-engineering-with-ai with the chapter reference and what's stale. Errata are tracked in `CHANGELOG.md` per release.
