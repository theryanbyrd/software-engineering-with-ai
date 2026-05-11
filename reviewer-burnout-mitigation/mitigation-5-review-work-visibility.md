# Mitigation 5 — Review Work Visibility

Recognition of review effort. Per Ch 44 §44.5:

> Make review work visible in performance reviews. If review judgment is a leveling criterion (Chapter 60) but reviews are not tracked or recognized, you are punishing the engineers doing the work. Track review counts, depth, and outcomes. Recognize publicly.

## The problem

Most performance review systems track:
- PRs shipped (visible in commit history)
- Features delivered (visible in product launches)
- Incidents handled (visible in postmortems)

Review work is largely invisible:
- Comments left on PRs (not aggregated)
- Issues caught in review (not tracked)
- Mentorship through review (not recognized)
- Async time reading other engineers' code (not measured)

The result: engineers who do substantial review work appear less productive than engineers who don't. Performance reviews favor the latter.

If the leveling criteria say "demonstrates strong code review judgment" but the data doesn't show review work, the criteria is decorative. Engineers who learn the rules of the game stop reviewing.

## The fix

Track review work explicitly. Recognize it publicly. Connect to performance reviews and promotion criteria.

## What to track

### Review counts

How many PRs the engineer reviewed in the period. Simple metric; available from GitHub / GitLab data.

Threshold for "reviewing meaningfully": >5 reviews per month (varies by team). Below this, the engineer isn't really participating in review.

### Review depth

How substantive the reviews are. Harder to quantify; signals:
- Average comments per review (>3 suggests substantive engagement)
- Reviews that catch issues (caught issues lead to fixes)
- Reviews that change the PR (the author updates code based on the review)

Some teams use a simple proxy: "review with at least one substantive comment that led to a code change." Reviews without this are tracking but lower-leverage.

### Review outcomes

The downstream effect of reviews:
- Issues caught in review that would have shipped (counterfactual; hard to measure precisely)
- Mentorship outcomes (junior authors growing because senior reviewers invested time)
- Pattern propagation (review comments establish team norms)

These are mostly qualitative — discussed in performance reviews rather than computed mechanically.

## How to recognize

### In performance reviews

Specific bullets in performance review templates:
- "Code review activity: X reviews this period"
- "Review depth signal: caught Y substantive issues; comments led to Z code changes"
- "Mentorship through review: specific examples"

The leveling rubric (per `promotion-and-leveling-rubric/`) connects these to specific levels:
- Senior+ engineers expected to review broadly
- Staff engineers expected to set patterns through review
- Lead engineers expected to mentor through review

### In public callouts

When an engineer's review catches a real issue (a bug, a security gap, a design flaw), public recognition:
- In team retro: "X caught the auth issue in PR #Y"
- In Slack channel: "Shoutout to X for the thoughtful review on PR #Z"
- In performance review summary: specific examples

This is cultural work. It costs little; it sends a clear signal that review matters.

### In promotion criteria

If review judgment is a leveling criterion, promotion conversations should reference review evidence:
- "Engineer X is being considered for senior; let's look at their review portfolio"
- Review portfolio: representative reviews showing depth and judgment

Engineers who don't review carefully don't level up. Engineers who do review carefully are recognized.

## Specific metrics to track

### Quarterly per engineer

- Total reviews (count)
- Reviews with substantive comments (count; rough definition)
- Issues caught in review (qualitative; pulled from PR comments)
- Reviewer concentration share (percentage of team reviews this engineer did)

### Quarterly per team

- Total review work distribution (top 3 reviewers' share, per `mitigation-3-round-robin-assignment.md`)
- Average review depth signal
- Engineer satisfaction with review (qualitative; surveys)

## Anti-patterns

### Tracking without recognition

The metrics exist; nobody references them in performance reviews. Decorative.

Mitigation: explicit performance review templates that pull review data.

### Recognition without tracking

Managers say "review is important" but don't measure. Engineers can't tell if their review work matters.

Mitigation: tracking is the precondition. Without data, recognition is rhetorical.

### Vanity metrics

Tracking "review counts" without "review depth." Engineers game by leaving "LGTM" comments on many PRs.

Mitigation: weight depth alongside count. Don't reward volume alone.

### Reviews-as-volume

The team treats review like a unit of production. "How many reviews did you do this quarter?" becomes the question.

Mitigation: the question is "what's your review portfolio look like?" — counts, depth, outcomes, mentorship together.

### Reviews tracked as engineer evaluation, not engineer development

The data is used to compare engineers against each other rather than to develop each engineer's review skill.

Mitigation: data drives development conversations. Manager and engineer review together: "here's where you're strong; here's where you can grow."

### Reviews-only review

The performance review focuses entirely on review work; the engineer's own contribution work is undervalued.

Mitigation: balance. Review is one component of the engineer's contribution, not the whole.

## The cultural shift

Per Ch 44 §44.5, the framing is direct:

> If review judgment is a leveling criterion (Chapter 60) but reviews are not tracked or recognized, you are punishing the engineers doing the work.

The cultural shift required:

- Review is first-class engineering work (not invisible overhead)
- Engineers who review carefully are recognized publicly
- Engineers who avoid review don't level up
- Mentorship through review is part of senior+ engineer expectations

Without this shift, the burnout pattern persists. With it, the team's review capacity scales sustainably.

## Implementation timeline

### Cycle N (next perf review)

- Add review work as explicit performance review category
- Pull review data for each engineer (counts, depth signal)
- Reference in performance review summaries

### Cycle N+1

- Review data is normalized; engineers expect it
- Promotion conversations reference review evidence
- Specific recognition patterns are established (Slack callouts; retro mentions)

### Cycle N+2

- Cultural shift is visible: engineers value review work
- Burnout symptoms decrease (recognition is part of why)
- Hot reviewer concentration drops

This is a multi-quarter shift. Don't expect immediate change. Don't drop the discipline if results aren't immediate.

## Companion artifacts

- `promotion-and-leveling-rubric/` — adjacent (where this connects)
- `promotion-and-leveling-rubric/levels.md` — level criteria including review judgment
- [`mitigation-1-ai-reviewer-subagent.md`](mitigation-1-ai-reviewer-subagent.md) — adjacent
- [`mitigation-3-round-robin-assignment.md`](mitigation-3-round-robin-assignment.md) — adjacent (rotation distributes the work this recognizes)
- Ch 44 §44.5 mitigation 5 — source
