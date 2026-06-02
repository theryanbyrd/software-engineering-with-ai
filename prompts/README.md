# Prompt Pattern Library (Appendix J)

> Companion to *Software Engineering with AI*, Appendix J. The book points here at
> `/prompts/`. These are durable **prompt patterns** — reusable shapes, not magic
> strings. Treat best-practice prompting as a perishable good and re-evaluate quarterly
> (Ch 1); the *patterns* below are durable, the exact wording is not.

Each file is one pattern: when to use it, the template, and the book reference. Patterns
are model-portable — they encode the discipline (plan before implement, demand
information requirements, verify deterministically), which outlasts any single model.

| Pattern | When to use | Book ref |
|---------|-------------|----------|
| [`agent-ready-issue.md`](agent-ready-issue.md) | Delegating a unit of work to an agent | Ch 19, Appendix C |
| [`information-requirements.md`](information-requirements.md) | Before finalizing a spec — find the gaps | Ch 19 |
| [`plan-implement-review.md`](plan-implement-review.md) | The core inner/outer loop | Ch 20 |
| [`independent-verification.md`](independent-verification.md) | Checking "is it done?" without trusting self-assessment | Ch 2 §2.1a, Ch 7, Ch 8 |
| [`slop-review.md`](slop-review.md) | First-pass review for the seven slop signatures | Ch 2, Ch 22 |
| [`task-decomposition.md`](task-decomposition.md) | Splitting a feature into parallel issues | Ch 20 |

> **Hard rule across all patterns (Ch 2 §2.4):** never ship without a human reading the
> diff. These patterns produce drafts and signals, not merges.

Contributions welcome — follow the shape of the existing files (when-to-use, template,
references) and cite the relevant chapter.
