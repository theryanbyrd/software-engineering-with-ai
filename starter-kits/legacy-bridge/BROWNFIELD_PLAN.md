# 90-Day Brownfield Plan

**Companion to:** Chapter 11 §11.6 of _Software Engineering with AI_ by Ryan Byrd.

**Important:** the brownfield harness takes 9-12 months to mature, not 3. This 90-day plan brings ONE module to MVH Level 2-3, not the whole codebase. Plan accordingly.

---

## Day 0 — Honest assessment

- [ ] Map the codebase: how many modules, how many lines, how much active development
- [ ] List the engineers who know each part well; flag departures and at-risk knowledge
- [ ] Score the codebase's MVH level today (see `MVH_LEVELS.md`)
- [ ] Set realistic expectations with leadership: "We will bring 1-2 services to MVH Level 2-3 in 90 days. Modernization is a multi-year program."

**Pass criterion:** leadership has signed off on the realistic timeline and there's no expectation that "AI will modernize the codebase by Q4."

---

## Week 1 — Pick the first service (Principle 1)

The selection rubric. Score each candidate service:

| Criterion | Weight | Score 1-5 |
|---|---|---|
| Recent changes have been disproportionately error-prone | 3 | |
| Engineers who know it are scarce or leaving | 3 | |
| Service is a known delivery bottleneck | 2 | |
| Tests exist, even if sparse | 2 | |
| Has a clear external API (testable boundary) | 2 | |
| Is NOT in the auth/billing/payments hot zone | 2 | |

The highest-scoring services are your candidates. Pick **one**, maybe two.

**Avoid:** the most-modified services. They are usually fine without AI help. The flashy "highest impact" target is usually the wrong target.

**Pass criterion:** you have a written selection memo with scores; the service is approved by your CTO or equivalent.

---

## Weeks 2-3 — Establish the golden master (Principle 2)

For your chosen service, capture the input/output behavior in a way that can be replayed.

**For an API service:**
- Record-replay against production-like traffic for 1-2 weeks
- Output: a directory of `inputs/` and corresponding `expected-outputs/`
- Use `legacy-bridge-scripts/golden-master-record.sh <service>`

**For a batch job:**
- Pick representative inputs (small, medium, edge)
- Run against current code; capture outputs as golden files
- Output: `tests/golden/{small,medium,edge}/expected-output.json`

**For a UI:**
- Visual regression tests on key flows
- Output: screenshot baselines via Playwright/Cypress

**Pass criterion:** running `legacy-verify.sh <service>` against the current code passes. Running it against a deliberately-broken version fails. The golden master detects the breakage.

---

## Week 4 — Build verify around the golden master (Principle 3)

`legacy-verify.sh <module>` should run:
1. Whatever lint / static analysis the codebase already has
2. Whatever unit tests exist for this module
3. The golden-master replay
4. Any integration tests that touch this module

The verify command becomes the single gate. Any AI change is gated on it passing.

**Pass criterion:** verify catches regression on the example failures from Week 2-3.

---

## Weeks 5-8 — Read-only AI on the legacy module (Principle 5 + 6)

**This is the highest-leverage step and the one most teams skip.**

For TWO weeks before letting an agent edit the legacy module, let it answer questions about it:

- "What does this function do? Where is it called from?"
- "What's the test coverage on this module?"
- "What are the invariants this code assumes?"
- "What's the failure mode if input X is malformed?"
- "What changes between version Y and current would I need to understand?"

Capture the agent's answers and the corrections from human reviewers as module-level READMEs. After two weeks, you have documentation that didn't exist before.

**Why this works:** read-only sessions surface harness gaps that matter (missing READMEs, undocumented invariants, mystery functions) BEFORE the agent writes a single line.

**Pass criterion:** at least 5 substantive READMEs exist that didn't exist before; the agent's "what does this do" answers are more than 80% accurate against expert review.

---

## Weeks 9-10 — First strangler-pattern change (Principle 4)

Now you can make a real change. The change must be:

- **In a NEW module** (strangler pattern), not in the legacy module
- **Tested against the golden master** of the legacy module
- **Reviewed by a human who knows the legacy code**
- **Under 100 lines diff**
- **Behind a feature flag if it touches production behavior**

This is not where you "modernize" the legacy code. This is where you BUILD ALONGSIDE it. The new module talks to the old; the old code is unchanged.

**Pass criterion:** one strangler-pattern change ships. The team has a worked example of what brownfield AI work looks like.

---

## Weeks 11-12 — Document, retro, plan next module

- [ ] Document the lessons in a brownfield retro
- [ ] Update CLAUDE.md with what you learned
- [ ] Update the Module Status table with the now-known-safe modules
- [ ] Score against `MVH_LEVELS.md` — you should be at Level 2 for this service
- [ ] Pick the next service using the same rubric
- [ ] Brief leadership: honest assessment of what worked, what didn't, what's next

**Pass criterion:** you have a working harness for ONE service. The team knows how to extend it. Leadership has realistic expectations.

---

## What this plan SACRIFICES

- Speed. This is the slow path. Greenfield 90-day plans get to working harness in 30 days; legacy gets there in 90.
- Breadth. You harden one service, not the codebase.
- Heroics. There are no heroics in brownfield. There is patient, unglamorous work.

## What you should NEVER compress

- The 2-week read-only period (Weeks 5-6). This is what most teams skip and most teams regret.
- The golden master step. Without it, you have no observable behavior to protect.
- The honest leadership conversation at Day 0. The political damage of compressed timelines hitting reality at Day 60 is much worse than the discomfort of honesty at Day 0.

## What 90 days does NOT get you

- A modernized codebase. That's a multi-year program.
- Most of the codebase under harness. That's months 4-12 (and beyond).
- Dramatic productivity gains. Realistic 90-day gains in legacy are 5-8% on tier-2 work in the hardened module.

If your leadership expects more than this in 90 days, the conversation that needs to happen is not "how do we go faster" but "what is realistic." Use [`exec-kit/ceo-emails/defending-the-investment.md`](../../exec-kit/ceo-emails/defending-the-investment.md) as a starting point.
