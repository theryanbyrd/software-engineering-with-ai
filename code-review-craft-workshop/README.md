# Code Review Craft Workshop

A workshop and reviewer-training kit for catching AI-generated code that passes review and breaks production. Direct companion to **Chapter 2 — AI Slop and the Review Crisis**, **Chapter 22 — Code Review in the AI Era**, and **Chapter 43 §43.x — Code review craft** of [_Software Engineering with AI: A Practical Handbook for the Claude Code Era_](https://github.com/theryanbyrd/software-engineering-with-ai) by Ryan Byrd, with the canonical signature list in **Appendix I — AI Code Smell Checklist**.

The book's framing:

> AI slop is the practical name for code that is syntactically correct, plausibly structured, and subtly wrong. It passes review because it looks like the code a reviewer expected to see. The fix is not better models. The fix is a reviewer who has been trained to spot the seven canonical signatures on sight.
>
> — Ch 2

This folder turns that training into a workshop: the AI Code Smell list expanded with worked examples, a facilitator guide for running the live session, a reviewer cheatsheet for the screen edge, and an evaluation rubric so you can tell whether your reviewers actually learned anything.

## What's in here

| File | Purpose |
|---|---|
| [`ai-code-smell-checklist.md`](ai-code-smell-checklist.md) | The seven canonical AI-slop signatures with worked examples for each |
| [`facilitator-guide.md`](facilitator-guide.md) | 90-minute workshop run-of-show, including timing, discussion prompts, and common derailments |
| [`reviewer-cheatsheet.md`](reviewer-cheatsheet.md) | Single-page printable reference — keep next to the monitor |
| [`evaluation-rubric.md`](evaluation-rubric.md) | How to score a reviewer trainee on a calibration diff |
| [`exercises/`](exercises/) | Annotated diffs, each containing one or more smells to spot in a timed exercise |
| [`review-prompts/`](review-prompts/) | Agent-driven review prompt templates (`/review`, `/security-review`) tuned for catching slop |
| [`calibration-set.md`](calibration-set.md) | Twenty real-world diffs scored by the author — use to verify new reviewers track to baseline |

## The book's core stance

Per Ch 22:

> The review process is where AI productivity gains either land in production or evaporate. A team that ships 3× the diffs but reviews them 30% as carefully has not gotten faster. It has shifted the cost from the author to the customer.

Three things follow:

1. **Reviewers need training, not exhortation.** "Be careful" is not a control. A checklist tied to a calibration set is.
2. **The seven signatures are pattern-recognition, not heuristics.** Trainees learn them by spotting them — repeatedly, with feedback — not by reading them.
3. **A junior reviewer who can spot the seven on sight is more valuable than a senior who rubber-stamps.** Per Ch 22 §22.6, this is the leverage point.

## Who this is for

- **Engineering managers** rolling out a code-review-quality initiative
- **Tech leads** running a team-internal workshop after a slop incident
- **Platform / DevEx teams** building reviewer-training infrastructure for org-wide rollout
- **Staff engineers** designing the reviewer-track for the promotion rubric (see [`../promotion-and-leveling-rubric`](../promotion-and-leveling-rubric))

## Related sections in this repo

- [`../evals-and-benchmarks-runbook`](../evals-and-benchmarks-runbook) — mutation testing and behavioral assertions that surface the slop the reviewer misses
- [`../reviewer-burnout-mitigation`](../reviewer-burnout-mitigation) — the operational counter to "the seniors review everything"
- [`../starter-kits`](../starter-kits) — the `/review` slash command and review hooks that bake the checklist into CI

> Early access. The checklist, cheatsheet, and calibration set are the highest-priority files. Exercises will land in batches as field-tested versions are validated against the calibration set.
