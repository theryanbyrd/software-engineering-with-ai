# Executive / Strategic Kit

The political artifacts: scripts, framing, and case studies for upward and outward communication. Direct implementation of Chapter 46 (managing hyped expectations), Chapter 47 (worked end-to-end examples as case studies), and Chapter 52 (the CEO and board conversation kit) of [_Software Engineering with AI: A Practical Handbook for the Claude Code Era_](https://www.linkedin.com/in/ryanbyrd) by Ryan Byrd.

The book's framing:

> The single highest-leverage skill for an engineering leader in 2026 is the ability to push back on hype with evidence, in writing, without being dismissive of the genuine opportunity.
>
> — Ch 46

> The conversations that determine whether your AI strategy succeeds happen mostly outside engineering. This chapter is the script library. Adapt the templates to your voice, your CEO's expectations, and your board's posture. The point is not to read these aloud. The point is that you should not be writing them at eleven pm on a Wednesday.
>
> — Ch 52

This folder is the script library. Adapt to your voice; do not skip the prep.

## What's in here

| File | Purpose |
|---|---|
| [`README.md`](README.md) | Overview, how this differs from `exec-kit/` and `skip-level-defense/` |
| [`hype-rebuttal-table.md`](hype-rebuttal-table.md) | Ch 46 §46.1 — the seven hype claims and the data-backed rebuttals |
| [`realistic-roi-message.md`](realistic-roi-message.md) | Ch 46 §46.2 — the number to commit to, with rationale |
| [`honest-internal-message-to-engineers.md`](honest-internal-message-to-engineers.md) | Ch 46 §46.3 — what lands vs. what builds resentment |
| [`four-slide-board-deck-walkthrough.md`](four-slide-board-deck-walkthrough.md) | Ch 52 §52.1 — what each slide should say (and what NOT to add) |
| [`what-number-do-i-commit-to.md`](what-number-do-i-commit-to.md) | Ch 52 §52.5 — the three-tier commitment framework |
| [`worked-examples-as-case-studies.md`](worked-examples-as-case-studies.md) | Ch 47 §47.1-47.3 — three concrete walkthroughs to tell your CEO |
| [`eleven-pm-podcast-clip-protocol.md`](eleven-pm-podcast-clip-protocol.md) | Ch 52 §52.4 — handling the anxious-CEO ping without relitigating strategy |

## How this differs from `exec-kit/` and `skip-level-defense/`

The repo has three executive-adjacent folders. They serve different purposes:

| Folder | What it is | When to use |
|---|---|---|
| **`exec-kit/`** | Operational templates: board deck PPTX, all-hands deck PPTX, ROI calculator XLSX, security questionnaire, CEO email templates, vendor scripts | Day 0 of rollout; week before board meeting; specific operational moments |
| **`skip-level-defense/`** (Ch 61) | Scripts for when the CEO bypasses you and talks to your reports directly | Specific defensive situations: hostile skip-levels, "no the model release didn't change strategy," briefing your reports for skip-level conversations |
| **`executive-strategic-kit/`** (this folder) | The framing artifacts: hype rebuttals, realistic ROI message, the three-tier commitment framework, worked examples to ground conversations in reality | Ongoing strategic communication: board meetings, CEO 1:1s, all-hands messages, written push-backs |

The exec-kit gives you the templates. Skip-level-defense gives you the defensive scripts. This folder gives you the strategic framing — the substance that goes into all of the above.

## When to use this folder

- **Before a board meeting** — pair with `exec-kit/board-deck-template.pptx`. Read [`four-slide-board-deck-walkthrough.md`](four-slide-board-deck-walkthrough.md) and [`what-number-do-i-commit-to.md`](what-number-do-i-commit-to.md) before populating the deck.
- **When the CEO sends an aggressive AI productivity expectation** — read [`hype-rebuttal-table.md`](hype-rebuttal-table.md) for the specific rebuttal pattern; pair with `exec-kit/ceo-emails/pushing-back-on-headcount-cut.md` if it's an explicit cut conversation.
- **When the CEO sends an 11pm podcast clip** — read [`eleven-pm-podcast-clip-protocol.md`](eleven-pm-podcast-clip-protocol.md); use `exec-kit/ceo-emails/podcast-clip-reply.md`.
- **Before an all-hands or team email** — read [`honest-internal-message-to-engineers.md`](honest-internal-message-to-engineers.md) to calibrate tone before drafting.
- **When asked for a productivity number** — read [`what-number-do-i-commit-to.md`](what-number-do-i-commit-to.md) before committing to anything.
- **When you need to make AI work concrete in a CEO/board conversation** — read [`worked-examples-as-case-studies.md`](worked-examples-as-case-studies.md) for three vivid walkthroughs.

## Who this is for

- **VPs of Engineering** — primary audience; this is the "weekly conversations with the CEO and quarterly with the board" toolkit
- **CTOs** — same conversations, often broader scope
- **Engineering Directors** — when the conversations escalate to your level
- **Heads of Platform** — when the platform team is being squeezed by hype-driven productivity expectations

## Read first

- Ch 46 — managing and tempering hyped expectations
- Ch 47 — three worked end-to-end examples
- Ch 52 — the CEO and board conversation kit
- `exec-kit/README.md` — the operational counterpart
- `skip-level-defense/README.md` — the defensive counterpart

## What this folder WILL do

- Give you data-backed rebuttals to the seven most common AI hype claims
- Give you a defensible ROI commitment with explicit conditions
- Give you a three-tier commitment framework so you don't promise more than you can deliver
- Give you three concrete walkthroughs that ground abstract conversations in reality
- Give you the script for the 11pm podcast-clip moment

## What this folder will NOT do

- Will not substitute for your own judgment about your specific CEO and board
- Will not work if read aloud — adapt to your voice
- Will not produce a number that survives contact with reality if your inputs are wrong (especially if you don't have the dashboard from `metrics-and-measurement-infrastructure/`)
- Will not protect you from a CEO who is actively pushing for a posture you can't defend — at some point the conversation is about whether you stay

## The core principle

Per Ch 52 §52.4 (commenting on the 11pm podcast clip):

> The eleven pm podcast clip is not a real ask. It is the CEO telling you they are anxious. Acknowledge, anchor in your plan, do not relitigate strategy at eleven pm.

Most of the strategic conversations are like this. They are not really requests for new strategy; they are anxiety about whether the existing strategy is working. The discipline is to anchor in the plan, the data, and the named outcomes — not to argue every passing podcast clip on its merits.

## Companion artifacts

- `exec-kit/` — operational templates
- `exec-kit/ceo-emails/` — three CEO email drafts
- `skip-level-defense/` — defensive scripts for skip-level scenarios
- `metrics-and-measurement-infrastructure/` — the dashboard the conversations reference
- `cost-discipline-runbook/leadership-conversation-on-cost.md` — adjacent
- `evals-and-benchmarks-runbook/quarterly-model-lineup-review.md` — adjacent
- Ch 46, Ch 47, Ch 52 — sources
