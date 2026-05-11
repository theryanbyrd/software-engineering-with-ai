# PR Review Exercise — Rubric

A 60-90 minute exercise that replaces the LeetCode round for senior engineering interviews. Per Ch 60 §60.5 of _Software Engineering with AI_.

## Purpose

To assess the candidate's code review judgment under realistic conditions. The signals we want:

- Can the candidate identify the seven slop signatures (Ch 22)?
- Do they distinguish blocking from major from minor from nit?
- Can they push back without being unkind?
- Do they catch the things that matter and let the things that don't matter pass?
- Do they ask "should this PR exist at all?" when appropriate?

## Format

The exercise is **async with a debrief**, not live. Live PR review is unrealistic — engineers in production don't review PRs with an interviewer watching.

1. **Send the candidate a real PR** (~150-300 lines diff). Sometimes from your own codebase (sanitized), sometimes from a public open-source project. The PR should be a real one with real flaws, not constructed for the interview.
2. **Give them 90 minutes** to review at their own pace. They can use any tools they normally use, including AI tools.
3. **Schedule a 45-minute debrief** with one interviewer. Walk through their review.

## What the candidate produces

A review document with:

- **Verdict:** approve / request changes / block
- **Findings** organized by severity (blocking / major / minor / nit)
- **Brief justification** for each finding
- **Optional commentary** on the PR overall: should it exist? is it the right size? is the testing strategy sound?

## Grading rubric

We grade on what they CATCH and what they LET SLIDE. The exercise PR has known flaws across multiple categories; we score per category.

### Slop signatures (Ch 22) — 7 categories, 1 point each
Track which the candidate catches:

- [ ] S1 — Imaginary API (a method that doesn't exist on the imported library)
- [ ] S2 — Confidently wrong (logic that looks plausible but doesn't match semantics)
- [ ] S3 — Repetitive boilerplate where abstraction would be cleaner
- [ ] S4 — Vestigial code (unused vars, dead branches, debug prints)
- [ ] S5 — Tests that pass without testing
- [ ] S6 — Comment drift (docstring no longer matches signature)
- [ ] S7 — Scope creep (changes outside the PR's stated scope)

### Severity calibration — 3 points
- **Excellent** (3): Distinguishes blocking from major from minor accurately. The blocking findings are genuinely blocking; the nits are genuinely nits.
- **Good** (2): Mostly correct severity assignments; one or two items inflated or deflated.
- **Weak** (1): Most findings flagged at the same severity (everything blocking, or everything minor).
- **Poor** (0): Severity assignments are random or inverted.

### Should-this-exist judgment — 3 points
- **Excellent**: Asks whether the PR should be three smaller PRs, whether the underlying problem warrants this approach, whether the test infrastructure is the right shape.
- **Good**: Catches at least one structural concern about the PR (size, scope, decomposition).
- **Weak**: Reviews the diff as-given without questioning structure.
- **Poor**: Misses obvious structural problems (e.g., a 600-line PR touching 15 files merged into one diff).

### Tone and pushback — 2 points
- **Excellent**: Pushes back on questionable choices with specifics, without being unkind. Frames suggestions as "consider X" not "you must Y."
- **Good**: Pushes back appropriately, sometimes overly soft.
- **Weak**: Either avoids confrontation entirely or is unnecessarily harsh.
- **Poor**: Hostile or sycophantic.

### Net signal — 2 points
- **Excellent**: We would let this person review our hard PRs without supervision.
- **Good**: We would let them review with light supervision.
- **Weak**: We would not yet trust them as a senior reviewer.
- **Poor**: We would coach this engineer back from "approve" to "request changes" frequently.

**Total possible:** 7 (slop signatures) + 3 (severity) + 3 (judgment) + 2 (tone) + 2 (net) = 17

## Calibration thresholds

- **Strong hire (15-17):** clearly senior. Move to offer.
- **Hire (12-14):** solid. Add positive signal in the architecture round.
- **Weak (9-11):** discuss; depends on what other rounds showed.
- **No (≤8):** not senior-level review judgment.

These thresholds calibrate to your team. Run a few internal engineers through the exercise to set the floor.

## What this rubric will NOT do

- Will not give you a clean rank order across all senior candidates. Two strong candidates will sometimes score within 2 points of each other; the architecture round and harness component conversation are tiebreakers.
- Will not work if your test PRs are too easy. If most candidates score 14+, the PR doesn't have enough real flaws.

## Common failure modes for the interviewer

- **Grading on the candidate's review style instead of substance.** A terse, accurate review beats a verbose, hand-wavy one. Don't reward word count.
- **Penalizing them for missing a finding you only know is a finding because you wrote the test PR.** If the finding is genuinely subtle, weight it less.
- **Confusing the candidate's tooling preference with their judgment.** A candidate who uses Cursor while another uses Claude Code is not the signal; the substance of the review is.

## Sample PRs to use

We recommend rotating among 3-5 different PRs to reduce leak risk. Build a small library:
- One small (50-100 lines) with one clear major flaw and several nits
- One medium (200-300 lines) with multiple slop signatures spread across files
- One large (500+ lines) where the right answer is "this PR should be 4 PRs"
- One refactor PR where the right answer is "this is a refactor; shouldn't be mixed with the bug fix"
- One test-changes PR where the question is whether the tests are now stronger or weaker

Sanitize before use. Remove any company-identifying details.
