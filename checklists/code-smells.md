# AI Code Smell Checklist (Appendix I)

> Companion to *Software Engineering with AI*, Appendix I. Canonical, always-current
> version of the checklist the book points to at `/checklists/code-smells.md`.
> The long-form workshop that teaches these on real diffs lives in
> [`../code-review-craft-workshop/`](../code-review-craft-workshop/).

Every item below is a **surface symptom** of the same underlying cause the book names
in Chapter 2 §2.1a: **agents tend toward self-congratulation.** The training objective
rewards outputs that *look* like successful completions, so an agent's self-assessment
is systematically unreliable. Never ask the agent whether it is done — run a
deterministic check, read the diff, pull the trace.

Print this. Train every reviewer to recognize all seven on sight (Ch 2 §2.2). A
30-minute session per quarter beats a 60-page style guide.

## The seven canonical AI-slop signatures (Ch 2 §2.2)

- [ ] **1. Tests that mock the implementation rather than the behavior.** A test that
  imports the function under test and asserts it returns what the mock returns. Tell:
  the test cannot fail if the implementation is wrong. *Interrogate every too-clean test
  with "does this fail if the implementation is wrong?"*
- [ ] **2. Deleted edge cases.** Original handled `null`, empty array, network timeout;
  the rewrite handles only the happy path. Tests pass because the original tests never
  covered those cases and the agent didn't add them.
- [ ] **3. Silent error swallowing.** `try/except: pass`, `.catch(() => {})`,
  `if err != nil { return nil }`. The function never fails — in the sense that it never
  tells anyone it failed.
- [ ] **4. Weakened validation.** A regex loosened "to make the test pass." A numeric
  range widened. A required field quietly made optional.
- [ ] **5. Removed security checks.** Permission checks, CSRF tokens, rate limits, input
  sanitization — omitted because the agent didn't see them as part of the task.
- [ ] **6. Unnecessary new abstractions.** A factory class wrapping a single function, a
  `BaseManagerHandler` for one concrete handler, a config object whose parameters each
  have exactly one possible value.
- [ ] **7. Diff bloat and pattern divergence.** A small task touches 600 lines across 14
  files because the agent "improved" adjacent code. Naming, formatting, or structural
  conventions silently diverge from the rest of the codebase.

## Reviewer gotchas (Ch 2 §2.5)

- [ ] **The halo effect.** AI code reads more confidently than human code; reviewers
  underweight skepticism. Counter: author tags the PR `[AI-authored]` and lists which
  sections they verified by hand.
- [ ] **Tooling that hides AI authorship.** If your VCS doesn't surface AI-written
  sections, build the signal yourself (PR template field, CODEOWNERS rule, or an
  automated label — see [`../scripts/pr-ai-tagger.py`](../scripts/pr-ai-tagger.py)).
- [ ] **"It works on my machine" is now "it passes the test the agent wrote."** A
  mocking-the-implementation test passes locally and in CI and tells you nothing.

## Non-negotiable countermeasures (Ch 2 §2.4)

- [ ] **Always review the code. Always.** No exception, no tier, no autonomy level. The
  discipline of reading every line your name is on protects everything else.
- [ ] **Make the author the first reviewer.** Definition of done includes "author can
  explain every line of the diff." If they can't, reject without further review.
- [ ] **Block oversized AI PRs by policy.** Hard cap ~400–600 lines / ~8–10 files unless
  explicitly approved.
- [ ] **Use a read-only AI reviewer as a second opinion, not a substitute.** A `/review`
  skill in Claude Code or Codex CLI in `--sandbox read-only` is reasonable.

## See also

- Long-form workshop + calibration set: [`../code-review-craft-workshop/`](../code-review-craft-workshop/)
- Heuristic detector: [`../scripts/slop-detector.py`](../scripts/slop-detector.py)
- Test-specific review: [`test-review.md`](test-review.md) (Appendix K)
- Book chapters: Ch 2 (slop + review crisis), Ch 22 (code review in the AI era), Ch 39 §slop-attribution
