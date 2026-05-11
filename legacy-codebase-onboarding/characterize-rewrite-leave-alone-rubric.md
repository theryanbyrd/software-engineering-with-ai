# Characterize, Rewrite, or Leave Alone — Per-Module Decision Rubric

The decision discipline for each module in a brownfield codebase. Direct implementation of Ch 11's choice between characterization (the default), strangler-fig new-alongside-old (when adding functionality), and rewrite (rare, last resort).

The book's framing:

> Avoiding large rewrites. Strangler-fig only. New code lives next to old code, traffic shifts gradually, old code is deleted only after the new path has owned 100% of traffic for a defined soak period.
>
> — Ch 11 §11.4

This file extends that principle into a rubric. The default for almost every module is "characterize and leave alone for now." Rewrite is rare. Strangler-fig is the bridge when new functionality is needed.

## The three choices

### Choice 1 — Characterize

**What it means:** Write golden-master tests against the module's public API. Document its behavior. Don't change the code. Build a safety net.

**When it's right:**
- The module works (mostly)
- The module is touched occasionally (changes happen but not constantly)
- The team plans to keep the module's behavior for the foreseeable future
- The module has unclear or absent documentation

**Cost:** 2-6 weeks per module to reach MVH Level 2.

**Outcome:** Module moves from "scary to touch" to "safe to touch under verify." Behavior is preserved.

### Choice 2 — Strangler-fig (new alongside old)

**What it means:** Build new functionality as a new module that wraps or replaces the legacy module's behavior over time. New code is greenfield-discipline; old code stays as-is until the new path has fully replaced it.

**When it's right:**
- New functionality is needed in this module's domain
- The legacy module's interface is workable enough to wrap, even if its internals are problematic
- The team has time horizon to run both paths in parallel for the soak period (months, not weeks)
- The team can defend the disk space / operational cost of running two paths

**Cost:** Building the new module is normal greenfield cost. The unique cost is the parallel-running operational discipline. Plan 3-9 months for full traffic migration.

**Outcome:** Eventually, the legacy module is deprecated or deleted. The new module owns the domain.

### Choice 3 — Rewrite (the rare option)

**What it means:** Replace the module wholesale, then delete the original.

**When it's right:**
- All four of the following are simultaneously true:
  1. The module's behavior is so fundamentally broken that preserving it is harmful (not just inconvenient — actually harmful)
  2. There is genuinely no path through characterization + strangler-fig that arrives at the same destination faster
  3. The team has the budget (months of focused work, not nights and weekends)
  4. There is an authority who will sign off on the months of feature-delivery slowdown that comes with the rewrite

**When it's wrong (which is most of the time):**
- The module is "messy" or "old" but works. Working code that's hard to read does not justify rewrite.
- The team thinks they "understand" the module well enough to rewrite. They don't. They're underestimating the corner cases.
- The team thinks AI tooling will make the rewrite cheap. It won't. AI tooling makes a rewrite faster to draft and equally slow to verify, debug, deploy, and stabilize.
- A specific feature is hard to add to the existing module. Build it as new (strangler-fig) instead.

**Cost:** 6 months minimum on average. Often much more. Plus the opportunity cost of feature delivery during the rewrite period.

**Outcome:** A new module that does what the team thinks the old module did, plus the bugs the team didn't realize the old module had as features.

## The rubric — score each candidate module

Use this for each module in the codebase. Score 0-3 on each dimension; total tells you the right choice.

### Dimensions

**1. Working / Broken**
- 0: Module works correctly under all conditions the team has tested
- 1: Module works under typical conditions; has known edge cases that produce wrong results
- 2: Module produces visibly wrong results often enough to be a real problem
- 3: Module is fundamentally broken — wrong behavior is the norm, not the exception

**2. Documented / Opaque**
- 0: Module has clear documentation of its public API and invariants
- 1: Module has incomplete documentation; some invariants are documented, others aren't
- 2: Module has no useful documentation; behavior must be inferred from tests or runtime observation
- 3: Module has no documentation, no useful tests, AND nobody alive understands it

**3. Stable / Volatile**
- 0: Module is rarely changed; the changes that happen are surgical
- 1: Module is changed monthly; changes mostly stick
- 2: Module is changed weekly; changes often produce regressions
- 3: Module is changed constantly; nobody is sure what state it's in

**4. Modernizable / Trapped**
- 0: Module is in a stack the team is comfortable with; has reasonable abstractions
- 1: Module uses some legacy patterns or libraries but remains tractable
- 2: Module is in a deprecated stack or framework that the team can't modernize
- 3: Module is in a stack with no community support, no upgrade path, and active CVEs

**5. Replaceable / Embedded**
- 0: Module has a clear, narrow interface; could be replaced behind it
- 1: Module's interface is wide but coherent; replaceable with effort
- 2: Module is deeply embedded; many callers depend on internal details
- 3: Module is the system — replacing it means rewriting most of the codebase

### Scoring

Sum the five dimensions. Score range: 0-15.

| Total | Recommendation |
|---|---|
| 0-3 | **Leave alone with light characterization.** Module is healthy. Don't waste effort. |
| 4-7 | **Characterize.** This is the default zone. Build the golden master, document the behavior, don't change the code unless you have to. |
| 8-11 | **Characterize, then strangler-fig new functionality.** The module needs work but rewrite is too risky. Add new functionality alongside; let the new path mature. |
| 12-15 | **Consider rewrite, with hard skepticism.** This is the rare case where rewrite might be the right answer. Run the rewrite-readiness check below before committing. |

## The rewrite-readiness check

If the rubric says "consider rewrite," answer all five questions before committing:

1. **Have we exhausted strangler-fig?** Could we build the new functionality alongside? In most cases yes. If you haven't tried, the answer is no.

2. **Is the budget signed off?** A rewrite is 6+ months. The product roadmap will slip. The CFO will notice. Has leadership signed off in writing on the slowdown?

3. **Do we know what the module does?** A rewrite needs to preserve behavior the team understands AND change the behavior the team finds problematic. If we don't know what the module does, the rewrite will introduce new bugs to compensate for the old ones.

4. **Do we have a behavior-preservation plan?** Before deletion, the new module must demonstrate the same behavior on the same inputs (with intentional differences clearly documented). Without this plan, "rewrite complete" doesn't actually mean rewrite complete.

5. **Are we starting from "we want to" or "we have to"?** "Want to rewrite" — almost never the right answer. "Have to rewrite" — sometimes. The honest test: if the original engineers came back, could you justify the rewrite to them with reasoning that wouldn't sound like ego?

If any answer is "no" or "I'm not sure," the rewrite is not ready. Default back to characterize + strangler-fig.

## Worked examples

### Example A — A 2010 PHP scheduling system that mostly works

The Ch 11 §11.5 example: medical scheduling system, no tests, central to clinical operations.

Rubric scores:
- Working: 1 (works for typical cases; known edge cases)
- Documented: 3 (no documentation, no tests, ambiguous ownership)
- Stable: 1 (rare changes, mostly stick)
- Modernizable: 2 (PHP 5.x, deprecated framework)
- Replaceable: 1 (narrow API, wrappable)

Total: 8 → **Characterize, then strangler-fig new functionality.**

The book's prescription matches: "spend two weeks writing characterization tests against the appointment-creation flow before changing one line; then strangle the legacy date-handling module behind a new interface."

### Example B — A 2018 Go service with sparse tests

A microservice the team built but tests have decayed; documentation is partial.

Rubric scores:
- Working: 0 (works correctly)
- Documented: 1 (partial)
- Stable: 1 (monthly changes, mostly stick)
- Modernizable: 0 (modern stack)
- Replaceable: 0 (clear interface)

Total: 2 → **Leave alone with light characterization.** Don't waste effort here. The module is healthy enough; spend the time on other modules that need it more.

### Example C — A 2008 Java module that produces wrong results regularly

An older module in a deprecated framework producing incorrect outputs.

Rubric scores:
- Working: 2 (visibly wrong often enough to be a problem)
- Documented: 2 (no useful docs)
- Stable: 2 (weekly changes producing regressions)
- Modernizable: 3 (deprecated framework, no upgrade path, CVEs)
- Replaceable: 2 (deeply embedded)

Total: 11 → **Characterize, then strangler-fig new functionality.**

Even at score 11, the right answer is rarely full rewrite. The wrong-results problem can usually be addressed inside the new strangler-fig module rather than by replacing the legacy module wholesale.

### Example D — A 2005 framework that the entire codebase depends on

The "module is the system" case. A custom-built ORM, framework, or scheduler that's in deprecated stack with no upgrade path.

Rubric scores:
- Working: 1 (works but with edge cases)
- Documented: 2 (sparse)
- Stable: 0 (rarely changed; nobody dares)
- Modernizable: 3 (deprecated stack, CVEs)
- Replaceable: 3 (the whole system depends on this)

Total: 9 → **Characterize, then strangler-fig new functionality.**

Even though "Replaceable" scored 3, the rubric's overall score still says don't rewrite. The system-wide dependency makes rewrite catastrophic. The path is: characterize the existing framework's behavior, build new modules using a modern framework that wrap/coexist with the old one, migrate gradually.

This example is instructive because it shows that even when one dimension is at 3, the rest of the rubric usually says "no rewrite." The rare cases that pass all the rewrite-readiness checks are unusual; assume your case isn't unusual until you've proven it is.

## When the rubric is wrong

The rubric is a heuristic, not an oracle. Specific cases where it can mislead:

- **A module scores low (4-7) but is actively dangerous to operate.** If the module is one bad change away from a SEV-1 incident, the rubric undersells the urgency. Characterize it AND restrict access (see `incident-postmortem-templates/harness-deficiency-checklist.md` Mechanism 5: MCP permission boundary).
- **A module scores high (12+) but rewriting would take 18 months that the team doesn't have.** The "consider rewrite" recommendation is contingent on having budget. If you don't have it, the answer is still characterize + strangler-fig, even though the score suggests rewrite.
- **A module scores middle (8) but the team has unique expertise that's about to retire.** The rubric doesn't capture knowledge-departure risk. Bias toward characterization and documentation when knowledge is leaving.

## What this rubric will NOT do

- Will not turn a "want to rewrite" engineer into a "characterize" engineer. Some engineers are wedded to rewrite; the rubric documents their judgment, doesn't change it.
- Will not make political decisions for you. If a VP has decreed rewrite, the rubric won't reverse that decision — but it can give you the language to push back.
- Will not work in vacuum. A team where every module scores 10+ is a team with a different problem than module-by-module work can solve.

## Companion artifacts

- [`30-60-90-day-plan.md`](30-60-90-day-plan.md) — uses this rubric to pick the first service
- [`anti-patterns.md`](anti-patterns.md) — the rewrite instinct as anti-pattern
- [`module-status-tracker-template.md`](module-status-tracker-template.md) — tracks each module's recommendation
- `starter-kits/legacy-bridge/MVH_LEVELS.md` — the maturity rubric for characterized modules
- Ch 11 §11.4 — the source on avoiding large rewrites
