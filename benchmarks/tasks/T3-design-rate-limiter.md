# T3-design-rate-limiter

**Tier:** T3
**Estimated time for senior engineer:** 4-6 hours
**Surfaces tested:** architectural reasoning, constraint surface design, observation discipline

## Adaptation guide

T3 tasks score the AGENT'S CONTRIBUTIONS, not the final output. The deliverable is a design document the agent produces during a multi-turn collaboration with the user/grader.

The grader plays the role of a thoughtful but time-constrained tech lead — pushing back on hand-waves, asking for specifics, requesting trade-off analysis. Score on whether the agent participates well, not on whether the agent solo-designs the right thing.

## Setup

- An ADR template exists in your codebase
- An existing rate-limiter (or absence of one) is documented
- The codebase has a public API with documented SLOs

## The task (give to the agent verbatim)

> We need to add rate limiting to our public API. The existing approach (a simple per-endpoint `@throttle` decorator with hard-coded limits) is not flexible enough. Design a replacement that supports: per-customer limits, per-endpoint limits, burst capacity (so legitimate spike traffic isn't penalized), and graceful degradation under load. Produce an ADR. Walk through the design with me. Be specific about: the data store, the algorithm choice (token bucket vs leaky bucket vs fixed window), the failure mode if the data store is down, the deployment plan, and the constraint surfaces (lints, schemas, validators) that prevent future engineers from accidentally bypassing it.

## Pass criterion

The agent produces an ADR (or substantive design document) that addresses all six required topics. The agent engages substantively with at least 3 push-backs from the grader. The agent identifies at least one trade-off or risk it cannot resolve and asks for input.

## Rubric — score 1-3 points each (max 24)

For T3 tasks, dimensions are scored on a 0-3 scale (0=absent, 1=weak, 2=adequate, 3=strong):

- [ ] **Direction framing** (0-3): Does the agent ask about user-facing behavior (what error response do customers see when limited?) before designing internals?
- [ ] **Architecture depth** (0-3): Does the design address the data store, the algorithm, the failure mode, the deployment, the constraint surface?
- [ ] **Evaluation thinking** (0-3): Does the agent propose a way to validate the design works (load test? metric? alert?)
- [ ] **Trade-off articulation** (0-3): Are trade-offs named with specifics, including the rejection of plausible alternatives?
- [ ] **Pushback engagement** (0-3): When the grader pushes back, does the agent engage substantively or capitulate / dismiss?
- [ ] **Honest uncertainty** (0-3): Does the agent flag at least one area where it doesn't have enough info, rather than pretending to know?
- [ ] **Constraint surface design** (0-3): Does the agent propose specific lints, schemas, validators that prevent future bypass — not just "we should be careful"?
- [ ] **Deployment realism** (0-3): Does the deployment plan address rollback, gradual rollout, fallback to current implementation if new system is down?

## How to grade T3 tasks (for the human grader)

- Read the full transcript before scoring. Do not score in real time.
- Score independently of the prior quarter's score. Recency bias.
- Use the prior quarter's transcripts as calibration. The same agent on the same kind of task should produce roughly comparable artifacts unless something changed.
- Don't penalize the agent for declining to commit to a final answer when the grader explicitly asked for trade-offs. "It depends on X, Y, Z" is sometimes the correct senior answer.

## Common failure modes (informational)

- **Solo-designs without engaging.** Agent produces a 2000-word ADR in one turn; never asks a question. This is the most common failure on T3.
- **Capitulates on pushback.** Grader pushes back; agent immediately reverses position without reasoning. Penalize on Pushback engagement.
- **Generic algorithmic answer.** Agent returns the textbook "use a token bucket" answer with no application to your context. Penalize on Architecture depth.
- **No constraint surface.** Agent describes the system but never proposes the lints/schemas/validators that prevent future regression. This is exactly the gap Ch 5 §5.2 names.
