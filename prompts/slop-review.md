# Pattern: Slop Review (first-pass)

**When to use:** As a first-pass filter on any AI-authored PR, before human review — not
as a replacement for it (Ch 14 §14.3, Ch 22). Saves the human 30–40% per PR with no
quality loss observed, *as long as the human still reads the diff*.

**Template:**

```
Review this diff as a skeptical senior reviewer. Check explicitly for the seven AI-slop
signatures and report each with file:line evidence:
1. Tests that mock the implementation rather than behavior
2. Deleted edge cases (null/empty/timeout)
3. Silent error swallowing
4. Weakened validation
5. Removed security checks
6. Unnecessary new abstractions
7. Diff bloat / pattern divergence

Also flag: scope creep beyond the issue, missing tests for new behavior, and any test
that would still pass if the implementation were wrong. Output a checklist with
PASS/FLAG per item and a one-line summary. Do not approve; produce findings only.
```

**References:** Ch 2 §2.2 (the seven signatures), Ch 22 (code review), and
[`../checklists/code-smells.md`](../checklists/code-smells.md) (Appendix I).
