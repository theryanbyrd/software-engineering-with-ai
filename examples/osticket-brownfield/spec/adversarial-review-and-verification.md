# Adversarial review & verification plan (auth change)

> The book's rule: every code-writing loop gets a separate verifier, and high-stakes work
> gets an adversarial one. For an authentication factor, "it passes" is a claim, not a proof.
> This file is the plan that makes the claim mean something.

## Why this change gets the full treatment
A bug in a webhook is an annoyance. A bug in a second factor is a silent downgrade of every
account's security — and the failure is exactly the kind the dashboard is happy about
(everything "works," logins succeed, and the factor is quietly bypassable). That is the
self-congratulation failure mode (Ch 2 §2.1a) with the highest possible blast radius, so we
verify deterministically and we do not let the maker grade its own homework.

## The maker/checker split
- **Maker** (implementer agent): drafts from `agent-ready-issue-totp-2fa.md`, mechanical parts only.
- **Checker** (reviewer agent, different system prompt + ideally different model, read-only):
  runs the adversarial checklist below against the diff. Treated as one noisy signal.
- **Human (senior):** owns the security-critical 20%, reads every line of the auth path, and
  makes the merge decision. The reviewer agent never approves; it only surfaces.

## The verification pyramid for this feature
1. **Deterministic unit tests — RFC 6238 vectors.** The TOTP function must reproduce the
   published RFC 6238 test vectors exactly. This is the one test that cannot be faked by a
   mock-the-implementation slop test (signature #1): the expected outputs come from the RFC,
   not from our code.
2. **Property tests.** Replay (a consumed step is dead), drift (±1 accepted, ±2 rejected),
   strike lockout, and "secret never leaves the server after enrollment."
3. **Characterization tests (unchanged).** The email-2FA contract in `harness/characterization/`
   must stay green. If it goes red, the change touched something it shouldn't have.
4. **Integration flow.** Dockerized enroll→login→reuse→drift→lockout, scripted with the
   `webapp-testing` skill, returning pass/fail + screenshot/log path.

## Adversarial reviewer checklist (the reviewer agent runs this on the diff)
- [ ] Is the code comparison constant-time? Flag any `==`, `===`, `strcmp`, or early-return on the secret/code path.
- [ ] Can a code be replayed within its valid step? Find the last-consumed-step bookkeeping or fail.
- [ ] Is the drift window exactly ±1 step? Flag any widening "to make a test pass" (slop signature #4, weakened validation).
- [ ] Is the secret encrypted at rest and absent from logs, rendered HTML post-enrollment, and URLs? Grep the diff and a captured trace.
- [ ] Are recovery codes one-time and hashed?
- [ ] Were any existing checks (strikes, lockout, CSRF on the form, session handling) removed or weakened? (slop signature #5)
- [ ] Is the diff confined to the seam, or did it "improve" adjacent auth code? (slop signature #7)
- [ ] Does `send()` leak anything or do anything observable? It must be an inert no-op.

## What would make us stop and not ship
- Any test that asserts the implementation against itself instead of against RFC vectors.
- Any "temporary" widening of the drift window or disabling of strikes.
- A green `verify` with a secret visible anywhere in the captured request/response trace.
- The human reviewer unable to explain the comparison and replay logic line by line.

## Provenance
The PR is tagged `[AI-authored]` with the sections the human verified by hand listed explicitly
(Ch 2 §2.5, the halo effect). Reviewer attention is the scarce resource here; make the
provenance visible so skepticism is calibrated correctly.
