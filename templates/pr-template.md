# PR Template — AI-Authored Code

Companion to *Software Engineering with AI* by Ryan Byrd · Appendix D / Chapter 21

Copy into `.github/PULL_REQUEST_TEMPLATE.md` (or your platform's equivalent).

```markdown
## What this PR does
<!-- One paragraph -->

## Tier and authorship
- [ ] Tier (T1 / T2 / T3): _____
- [ ] AI authorship: human-only | AI-assisted | AI-authored-reviewed | AI-authored-unreviewed (last is forbidden)
- [ ] Model used (if AI-assisted/authored): _____
- [ ] Author can explain every line of the diff

## Linked issue
<!-- Link to the agent-ready issue (Appendix C) -->

## Acceptance criteria from the issue
- [ ] All items from the issue's acceptance criteria are met
- [ ] All new behavior is covered by tests
- [ ] No existing tests were weakened to make new tests pass

## Slop signatures check (Ch 2)
- [ ] No tests mock the implementation they're testing
- [ ] No deleted edge cases (null, empty, timeout)
- [ ] No silent error swallowing
- [ ] No weakened validation
- [ ] No removed security checks
- [ ] No unnecessary new abstractions
- [ ] Diff size proportional to scope; no scope creep

## Blast radius
- User-facing? Y/N
- Data-affecting? Y/N
- Reversible? Y/N
- Feature-flagged? Y/N

## Reviewer notes
<!-- Anything that needs extra reviewer attention. Cite files. -->
```

## Quality bar

- An AI-authored PR with no slop-signatures-check section is incomplete. Reviewers may close-without-review.
- "AI-authored-unreviewed" is not a valid value. Reviewing your own AI's output is the minimum bar (Chapter 2 §2.4).
- The diff size cap from CLAUDE.md applies to AI-authored PRs without exception.
