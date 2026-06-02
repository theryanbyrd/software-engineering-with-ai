# AI-Generated Test Review Checklist (Appendix K)

> Companion to *Software Engineering with AI*, Appendix K. Canonical version of the
> checklist the book points to at `/checklists/test-review.md`. Use it whenever you
> review tests an agent wrote — which, in an AI-native workflow, is most tests.

The governing principle (Ch 8): in an era when an agent produces plausible-looking code
at high speed, **verification ratifies behavior after code exists.** Tests are the
load-bearing part of that — but agent-written tests are the single most common place
slop hides, because a green suite *looks* like proof. "Tests that mock the
implementation" is the #1 slop signature (Ch 2 §2.2). `verify` passing is **necessary,
not sufficient** (Ch 7).

## The one question that catches most slop

- [ ] **Does this test fail if the implementation is wrong?** Mentally (or actually)
  break the implementation and confirm the test goes red. If it stays green, the test is
  theater. This single check catches the #1 slop signature.

## Behavior, not implementation

- [ ] Test asserts on **observable behavior / outputs / contracts**, not on internal
  calls or on a mock's return value.
- [ ] Mocks are used for **boundaries** (network, clock, filesystem, third-party APIs),
  not for the unit under test.
- [ ] No test imports the function under test and asserts it returns what a mock was told
  to return (slop signature #1).
- [ ] Removing a mock and running against the real collaborator (where cheap) would still
  pass.

## Coverage of the cases that matter

- [ ] **Edge cases preserved** (slop signature #2): `null`/`None`, empty collections,
  boundary values, network timeouts, partial failures — anything the original code or
  spec handled.
- [ ] **Error paths asserted**, not swallowed (slop signature #3): the test proves the
  code *reports* failure, not just that it doesn't throw.
- [ ] Negative/adversarial inputs are tested where the function is security- or
  validation-relevant (slop signatures #4, #5).
- [ ] New behavior in the diff has a test that would have failed before the change.

## Suite health (Ch 7, Ch 8)

- [ ] Tests live under the repo's test directory and run in `verify`.
- [ ] Fast tier (<2 min) and full tier (<10 min) are respected — a 20-minute suite makes
  the inner loop unusable (Ch 7).
- [ ] No flaky/time-dependent assertions (real sleeps, wall-clock, network without a
  fake).
- [ ] Tests are deterministic and independent (no hidden ordering dependencies).
- [ ] Names describe the behavior under test, matching codebase conventions (no diff
  bloat / pattern divergence, slop signature #7).

## Reviewer discipline

- [ ] Treat a suite that looks **too clean** as a red flag — interrogate it harder, not
  less (Ch 2 §2.4).
- [ ] Author can explain every test and why it would catch a regression.
- [ ] PR is tagged `[AI-authored]`; author lists which tests they verified by hand.

## See also

- Code smells (broader): [`code-smells.md`](code-smells.md) (Appendix I)
- `write-tests` skill: [`../skills/write-tests/`](../skills/write-tests/)
- Book chapters: Ch 7 (verify command), Ch 8 (verification pyramid), Ch 21 (PR standards)
