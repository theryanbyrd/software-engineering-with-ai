# IC Track Additions

Additions to your existing IC career ladder for the AI-native engineering era. Maps to Chapter 60 §60.1 and Chapter 5 §5.2 of [_Software Engineering with AI_](https://www.linkedin.com/in/ryanbyrd) by Ryan Byrd.

## Three changes that apply across all levels

These are not level-specific; they are signals that get weighted differently as you go up:

1. **Harness contribution.** Has the engineer shipped a skill, hook, subagent, or harness component used by other teams?
2. **Code review judgment.** Does the engineer find the seven slop signatures (Ch 22)? Calibrate diff size? Ask "should this exist at all"?
3. **Direction / Architecture / Evaluation depth.** Which of the three bottleneck disciplines (Ch 5 §5.2) does the engineer demonstrate, and at what depth?

The text below describes how each manifests at each level. Use as additions to your existing scope/impact criteria.

---

## L3 — Engineer (mid-level)

### Harness contribution
- Uses the team's harness fluently. Knows when to invoke which skill. Reports skill bugs back to the platform team with concrete repros.
- Has contributed at least one small improvement (a fix to a hook, a clarification in CLAUDE.md) — not necessarily a new skill from scratch.

### Code review judgment
- Identifies obvious slop signatures (S1 imaginary APIs, S5 tests-without-testing, S7 scope creep) in PRs.
- Asks for clarification when reviewing AI-authored code rather than rubber-stamping.

### Direction / Architecture / Evaluation
- Recognizes which of the three disciplines a piece of work falls into. Knows that "the spec is unclear" is a Direction problem, not "go figure it out yourself."
- Depth in any one discipline is not yet expected at this level.

### Promotion to L4 requires
- The engineer reliably writes agent-ready specs from scratch in <30 minutes for tier-2 work.
- Code review work is trustworthy: senior engineers stop double-checking the L3's reviews.
- A first solo harness contribution (skill, hook, subagent, or substantial CLAUDE.md addition).

---

## L4 — Senior Engineer

### Harness contribution
- Has shipped at least one harness component (skill, hook, subagent, MCP integration) that other engineers use without coaching.
- Treats harness contribution as part of normal work, not as a side project.

### Code review judgment
- Catches all seven slop signatures consistently. Calibrates diff size and scope. Pushes back on PRs that should not have been opened.
- Reviews AI-authored code with the same discipline as human-authored code; sometimes more.

### Direction / Architecture / Evaluation
- **Demonstrates competence in all three disciplines.** Can write a spec, can encode a constraint into a hook, can design an evaluation.
- May not yet have depth in any one — the depth comes at L5.

### Promotion to L5 requires (Ch 60 §60.1 — explicit criteria for the new bottleneck)
- **Harness contribution that crosses team boundaries.** Other teams adopt a skill, hook, or subagent the engineer shipped.
- **Demonstrated depth in one of Direction / Architecture / Evaluation**, with credible competence in the other two.
- **Code review judgment that other senior engineers rely on.** The L4 → L5 line in 2026 includes "people send their hard PRs to this person for review."

---

## L5 — Staff Engineer (or your equivalent — sometimes called Senior Staff or Tech Lead)

### Harness contribution
- Owns a meaningful portion of the team's or org's harness. May have led the design of the skill library, the hook framework, the subagent roster.
- Mentors other engineers in shipping harness contributions.

### Code review judgment
- Sets the bar for the team. Other engineers calibrate to this person's standards.
- Comfortable saying "this PR shouldn't have been opened" with concrete reasoning.

### Direction / Architecture / Evaluation
- **Depth in one discipline; credible competence in the other two.** Can lead a design conversation in their depth area; can hold their own in the other two.
- The discipline-specific senior templates ([Direction](../jds/senior-engineer-direction.md), [Architecture](../jds/senior-engineer-architecture.md), [Evaluation](../jds/senior-engineer-evaluation.md)) describe what L5 depth looks like in each.

### Promotion to L6/L7 (Staff/Principal/Distinguished — your nomenclature)
- **Org-wide impact through one of the three disciplines.** Has shaped how the engineering org thinks about Direction, Architecture, or Evaluation.
- **Has trained the next L5 cohort.** People they coached are now operating at L5.
- **Influences hiring and rubric design.** Not just an IC; shapes how the org grows.

---

## L6/L7 — Staff/Principal/Distinguished Engineer

### Harness contribution
- Architectural responsibility for the harness across multiple teams. Decides what's in shared infrastructure vs. per-team.
- May own the relationship with AI vendors at the technical level.

### Code review judgment
- Reviews are educational. The author learns more from this engineer's review than from any other.
- Sets review-discipline standards for the org.

### Direction / Architecture / Evaluation
- **Org-wide impact through one of the three.** Examples:
  - Direction: led the engineering effort to redefine how the org writes specs in the AI era.
  - Architecture: designed the constraint-surface patterns the org now uses across all critical systems.
  - Evaluation: built the evaluation infrastructure that other teams now adopt.

These engineers are rare and retention-sensitive (Ch 60 §60.4). Their loss is disproportionately costly.

---

## How to discuss these criteria with engineers

The most common failure mode in rolling out new ladder criteria is that engineers don't know what "harness contribution" means concretely. A few specific examples per level — drawn from your team's actual work — are worth more than abstract definitions.

Suggested calibration: in your next quarterly skip-level, ask each engineer in the level under discussion to describe their most recent harness contribution. The shape of the answer tells you whether the criterion has landed.

## What this rubric will NOT do

- Will not magically promote engineers who weren't going to get promoted anyway. The new criteria filter additional, they don't lower the bar.
- Will not protect you against the market premium (Ch 60 §60.2). If the comp doesn't move, the senior bench leaves regardless of the rubric.
- Will not work without the corresponding performance review changes (see [`../perf-reviews/`](../perf-reviews/)).
