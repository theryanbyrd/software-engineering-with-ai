# Reviewer Cheatsheet — AI Code Smell Quick Reference

Print this. Tape it next to your monitor. Re-read it the first three months after the workshop. The seven signatures from Ch 2 §2.2; the four red flags from Ch 22; the final question.

---

## The Seven Signatures

| # | Signature | Look for |
|---|---|---|
| **S1** | Tests mock the implementation | `assert mock.called_with(...)` instead of asserting on output or side effects. Test passes if function body is `pass`. |
| **S2** | Deleted edge cases | Function shrank. `None` / empty / timeout branches in the old code are absent in the new. Open the original; count branches. |
| **S3** | Silent error swallowing | `except: pass`, `.catch(() => {})`, `if err != nil { return nil }`. Caught exception not logged, not re-raised, not in the return value. |
| **S4** | Weakened validation | Regex got shorter. Required field is now optional. Range widened. Validation expression marked "more permissive." |
| **S5** | Removed security checks | New handler/endpoint without auth, rate limit, CSRF, input sanitization. Decorators on the old endpoint didn't come along. |
| **S6** | Unnecessary new abstractions | Factory for one concrete type. Interface with one impl. Config object with one parameter value. Rule of three not met. |
| **S7** | Diff bloat / pattern divergence | PR > 400 lines or > 10 files. Renames, reformats, or unrelated "improvements" mixed in. Style diverges from the codebase. |

---

## The Four Red Flags (Ch 22)

1. **PR not tagged `[AI-authored]` when the author used AI.** Per Ch 2 §2.4, the tag is the discipline that makes the rest of this work. No tag, no merge.
2. **Author can't explain a line.** Per Ch 2 §2.4 — "definition of done includes 'author can explain every line of the diff.'" If they can't, reject without further review.
3. **CI green, but tests look too clean.** Per Ch 2 §2.5 — "a passing test suite that looks too clean is a red flag." Read the assertions; don't trust the green check.
4. **Diff > 400 lines / > 10 files without prior approval.** Per Ch 2 §2.4 — hard cap. Split it before review.

---

## Before You Approve — The Final Question

> If this ships and breaks production at 3am, which line is the broken one — and is there a test that would have failed if it were wrong?

If you can't answer, you haven't reviewed the PR. Send it back.

Per Ch 2 §2.4:

> Always review the code. Always. This is the one principle that does not have an exception, a tier, an autonomy level, or a "freely delegable" footnote.

---

## Heuristics by Signature (Compact)

- **S1**: Could the implementation be `return None` and the test still pass? → S1.
- **S2**: Open the original. Branch count went down? → S2 until proven otherwise.
- **S3**: Search the diff for `catch`/`except`. Is the error logged or propagated? If neither, → S3.
- **S4**: Validation got shorter. Does the PR description say *why* the loosening is safe? If not, → S4.
- **S5**: New endpoint. Auth? Rate limit? CSRF? Sanitization? If any missing without explanation, → S5.
- **S6**: One concrete impl right now? No dated plan for a second? Removing the abstraction shortens the code? → S6.
- **S7**: Files touched > files the issue justifies? → S7. Stop reading. Ask author to split.

---

## When to Escalate

- **Auth, billing, PII, crypto, deletion** paths → require Tier 1 review per [`../do-not-automate-catalog/tier-1-never-autonomous.md`](../do-not-automate-catalog/tier-1-never-autonomous.md). Loop in CODEOWNERS for those paths.
- **Two or more signatures in one PR** → likely incident-shaped. Don't just leave comments; request a re-write or a pair session.
- **Author of the PR is L0 or L1 certified** → per [`../agent-autonomy-levels/certification-gates.md`](../agent-autonomy-levels/certification-gates.md), they may not have the experience to author this work alone. Senior co-author may be needed.

---

## What This Cheatsheet Won't Save You From

- **A PR you didn't actually read.** Skimming and approving is rubber-stamping. Per Ch 2 §2.6: "rubber-stamp reviews are how good engineering organizations decay quietly."
- **A signature you haven't internalized.** The cheatsheet cues recognition; it does not substitute for it. The exercises in [`exercises/`](exercises/) are where recognition is built.
- **Bugs that don't match any of the seven.** Some bugs are just bugs. Use [`../incident-postmortem-templates/failure-categorization-guide.md`](../incident-postmortem-templates/failure-categorization-guide.md) for the broader taxonomy.

---

*Cheatsheet companion: [`ai-code-smell-checklist.md`](ai-code-smell-checklist.md) is the full reference. Read it once. Re-read it every quarter.*
