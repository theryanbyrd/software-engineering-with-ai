# Legacy Codebase Autonomy Rule

The "L1/L2 only for first six months in legacy" rule from Ch 11 §11.6 Principle 7. Direct cross-reference between this folder and `legacy-codebase-onboarding/`.

The book's stance:

> Strict autonomy ceiling. Legacy work runs at L1 (suggest only) or L2 (single-file edits with mandatory review) for the first six months. No L3+ in legacy until the harness is proven and the test pyramid is restored.
>
> — Ch 11 §11.6 Principle 7

This rule is non-negotiable for the first six months. After six months, autonomy can be raised — but only against the same criteria that apply to greenfield (per [`raising-and-lowering-autonomy.md`](raising-and-lowering-autonomy.md)).

## Why the legacy ceiling exists

Legacy code has different failure modes than greenfield:

- Tests are sparse or unreliable; PR review is the primary safety net
- Documentation is absent or stale; the agent's context is incomplete
- Invariants are encoded in production behavior, not in code or tests
- Behavior changes can surface weeks later in customer escalations
- The seven slop signatures (per Ch 22 §22.2) are more dangerous in legacy because the surrounding code's correctness is itself uncertain

Running at L3+ in legacy is the canonical pattern that produces the worst-of-both-worlds outcome the book describes:

> The teams that try to compress this end up with the worst of both worlds: slop in legacy code with no safety net.
>
> — Ch 11 §11.6

## The rule, applied

### For the first six months in any legacy module

Regardless of:
- The team's overall autonomy level
- The engineer's certifications
- The model's apparent capability
- Pressure to move faster

Legacy modules run at:
- **L0** (read-only) for the first 2 weeks (per `legacy-codebase-onboarding/30-60-90-day-plan.md` Days 8-14)
- **L1** (suggest only) once a module owner is named and basic mapping is done
- **L2** (single-file edits with mandatory review) once the module is at MVH Level 2 (per `starter-kits/legacy-bridge/MVH_LEVELS.md`)

That's the ceiling for the first six months. No L3+ in any legacy module during this period.

### After six months — what changes

The six-month rule is a floor on patience. After six months, the question becomes whether the harness has earned higher autonomy on a module-by-module basis.

The criteria — same as for greenfield (per [`raising-and-lowering-autonomy.md`](raising-and-lowering-autonomy.md)):

- **L1 → L2:** PR review discipline proven on 30+ AI-assisted PRs without a slop incident, with characterization tests in place
- **L2 → L3:** subagent roster covers the legacy module's specific concerns; review checkpoints automated; observed for 90 days
- **L3 → L4:** strictly within tier-restricted whitelist (docs/tests/types only); CODEOWNERS enforced for the legacy module

The criteria are the same; the threshold is later because legacy gets less reliable verification.

### What "first six months in any legacy module" means

The clock starts when the team begins serious AI-tooling work on the module — typically when the team picks the module per the 30-60-90 plan. Not when the team became aware of the module; not when AI tooling was introduced to the team broadly.

The clock runs per-module, not per-team. Module A might be at L2 after 8 months while module B is still at L1 because module B was picked up later.

If a module's harness regresses (tests decay, ownership lapses), the clock resets. The six-month rule is a floor; the underlying criteria are the gate.

## Why this rule resists pressure

Engineers and managers will push back on this rule with various arguments. The honest responses:

### "We're using AI everywhere else; why is legacy different?"

Per Ch 11 §11.6:

> Modern AI works beautifully in clean, well-typed, well-tested codebases. It is a hazard in old enterprise systems.

The hazard is the absence of safety net. AI tooling at L3+ assumes the harness catches errors. Legacy harness doesn't catch errors at the same rate. Same model + worse harness = worse outcomes.

### "We have characterization tests now"

Characterization tests are necessary but not sufficient for L3+. Per Ch 11 §11.6 Principle 7's reasoning, "no L3+ in legacy until the harness is proven AND the test pyramid is restored." Characterization tests address the verification side; the test pyramid (the layered confidence in unit / integration / system tests) takes longer to restore.

### "Our team is senior; we can handle it"

Per Ch 32 §32.4:

> A team's autonomy level is not the highest level of any individual; it is the level that the team's harness, review discipline, and incident history have earned.

Senior engineers are part of the discipline equation, not a substitute for the harness equation.

### "We have a tight deadline"

The deadline doesn't change the harness. Compressing autonomy timeline produces incidents; the incidents extend the deadline more than the discipline did.

### "Other teams are at L3 in legacy; why aren't we?"

Other teams may be drifting (per [`autonomy-drift-monitoring.md`](autonomy-drift-monitoring.md)). Or they may be earlier in the harness investment that's making L3 work for them. Investigate; don't copy.

## How to communicate the rule

### To engineers

> "We're at L1 (suggest only) in this module for now. Specifically:
> - The agent can read everything; that's already configured
> - The agent suggests changes; you review before applying
> - Single-file edits when we get characterization tests in (probably 4-6 weeks from now)
> - L2 is the goal for the next 6 months
> - L3+ requires the harness to be in a different state; we'll get there but it's a 9-12 month investment, not a quarter
>
> If this feels slow, that's the discipline doing its job. Slow now > incident in 8 weeks."

### To leadership

> "On legacy work, our autonomy ceiling is L1 or L2 for the first six months. This is per Ch 11 of the AI engineering handbook; the data on AI in legacy codebases is consistent across companies — running at higher autonomy in legacy without the harness produces incidents.
>
> What we get from the discipline: characterization tests built up over time, slow but real progress on harness, no incidents from AI-introduced slop in legacy code.
>
> What we'd risk by compressing: per the playbook, the worst-of-both-worlds — slop in legacy with no safety net. The cost of that is months of incident response, not weeks."

### To engineers asking for an exception

> "I won't grant an exception. The reason isn't your competence; it's the harness. Even at your level of skill, AI-authored changes in legacy code without the harness produce incidents at higher rates than greenfield. The six-month floor is a discipline; we hold it as a team.
>
> What I can do: prioritize the harness work that gets us to L2 faster. If we're disciplined on characterization, we hit L2 in 8-10 weeks instead of 6 months. That's the path."

## What this rule will NOT do

- Will not work without leadership backing. Engineers will push back; without leadership defending the rule, it erodes.
- Will not work in cultures that view safety as overhead. Some cultures will treat the rule as obstacle; without cultural alignment, the rule is decorative.
- Will not protect against teams that bypass the rule informally. Mechanical enforcement (per [`forbidden-categories.md`](forbidden-categories.md)) is required for the highest-stakes categories.
- Will not eliminate the difficulty of brownfield modernization. The rule is the floor; the underlying work is still hard.

## Companion artifacts

- [`autonomy-ladder.md`](autonomy-ladder.md) — the broader L0-L5 framework
- [`raising-and-lowering-autonomy.md`](raising-and-lowering-autonomy.md) — the discipline applied to legacy
- `legacy-codebase-onboarding/30-60-90-day-plan.md` — the operational program around this rule
- `legacy-codebase-onboarding/anti-patterns.md` — anti-pattern 5 ("skipping the read-only AI phase") and 6 ("premature MVH promotion")
- Ch 11 §11.6 Principle 7 — source
- Ch 32 — adjacent
