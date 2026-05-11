# 30-60-90 Day Plan for Brownfield Onboarding

The structured plan for the engineer or tech lead joining a team that owns brownfield code. Direct implementation of Ch 11 §11.6's seven principles, paced realistically.

The plan assumes the engineer arrives with general engineering experience but is new to *this* codebase and possibly new to brownfield work as a discipline. Adjust pace down if either condition is more extreme; do NOT adjust pace up.

## The shape of the 90 days

| Phase | Days | Goal | Output |
|---|---|---|---|
| **Phase A — Listen** | 0-30 | Build the picture; resist the rewrite instinct | Module status tracker filled in; first service picked |
| **Phase B — Characterize** | 30-60 | First service to MVH Level 1-2 | Golden master tests; verify command working; module README |
| **Phase C — Foothold** | 60-90 | First service to MVH Level 2-3; harness in production use | One module under harness; second service identified |

The phase boundaries are soft; some Phase A work continues through Phase C. The named goals are firm.

---

## Days 0-7 — Listen and observe

The week most engineers fail. The temptation: open the codebase, identify problems, start drafting fixes. The discipline: read, ask, document, decide nothing.

### What to do

- **Day 1: Onboarding basics.** Standard new-hire / role-change administrivia. Don't skip. Use the time to get badges, accounts, repo access — don't try to read the codebase yet.
- **Day 2-3: Read the existing documentation.** Whatever exists. README files, design docs, runbooks, postmortems, ADRs (if any). Even if 80% is outdated, the 20% that's accurate is your baseline.
- **Day 3-4: One-on-ones with engineers.** Every engineer who's been on the team for >12 months gets 30 minutes. The questions:
  - "What does this team own? What's adjacent that we don't own?"
  - "What's the part of the codebase you trust most? Least?"
  - "What changed recently that you wish you could un-change?"
  - "If I were going to break something accidentally, where would I most likely break it?"
  - "Who else should I talk to?"
- **Day 5: Run the build, run the tests.** Whatever the verify command is, run it. Note what's flaky, what's slow, what fails on a clean checkout. Don't fix anything yet.
- **Day 6-7: Read code in the modules engineers told you mattered most.** 30-60 minutes per module. Take notes on what you don't understand. Don't try to understand everything.

### What NOT to do

- Don't propose any changes
- Don't volunteer to fix anything you noticed
- Don't open any PRs (except for trivial doc fixes if you really must)
- Don't run the AI agent on the codebase yet — see Day 8 below

### Pass criterion

You can name 3-5 modules, say what each roughly does, and identify at least one engineer who knows it well.

If you can't, the listening was too rushed; extend.

---

## Days 8-14 — Read-only AI sessions

Per Ch 11 §11.6 Principle 5:

> Before letting an agent edit the legacy module, let it answer questions about it for two weeks. "What does this function do? What calls it? What's the test coverage?" These read-only sessions surface harness gaps that matter — missing READMEs, undocumented invariants — before the agent writes a single line.

### What to do

- **Set up a read-only Claude Code or Cursor session** on the codebase. No write access. Configure with the team's existing CLAUDE.md (or AGENTS.md if you're using that). If neither exists, that's already a finding.
- **Run agent Q&A sessions on the modules you read in week 1.** Ask:
  - "What does the [module name] do? Walk me through the public API."
  - "What are the invariants this module assumes about its inputs?"
  - "What other parts of the codebase call into this module?"
  - "What are the failure modes of this module?"
- **Document the agent's gaps.** Where the agent confidently said something wrong (verify against engineers who know the module). Where the agent had to refuse / hedge because it lacked context. These are the harness gaps.
- **Document the agent's surprises.** Things you and the agent both didn't know that turned out to matter. These are the institutional knowledge gaps.

### What NOT to do

- Don't let the agent write code (literally configure permissions to prevent it)
- Don't trust the agent's confident assertions about behavior — verify
- Don't try to "fix" the harness gaps yet; just document

### Pass criterion

You have a list of 5-10 specific harness gaps and 5-10 specific institutional knowledge gaps. The list is the input to Phase B.

---

## Days 14-21 — Module Status Tracker, first pass

Per [`module-status-tracker-template.md`](module-status-tracker-template.md). The first version is your tool for the rest of the 90 days.

### What to do

- **List every module the team owns.** Modules, not files. A module is a coherent unit of code that someone could plausibly own.
- **Score each module's MVH level today** per `starter-kits/legacy-bridge/MVH_LEVELS.md`. Most modules in a brownfield codebase are at Level 0 (off-limits) or Level 1 (mapped, but no tests).
- **Identify the named owner for each module.** If nobody owns it, mark "no owner" — that's a finding.
- **Identify the modules that aren't safe to touch yet.** Your goal in 90 days is NOT to bring all modules to L2; it's to bring 1-2 specific modules to L2. The rest stay at their current level.

### What NOT to do

- Don't try to bring multiple modules to L2 simultaneously
- Don't promise modernization timelines you can't keep
- Don't pretend the codebase is in better shape than it is in writing

### Pass criterion

Module status tracker exists, lists every module, scores MVH level, names owners or "no owner."

---

## Days 21-30 — Pick the first service

Per Ch 11 §11.6 Principle 1, scored against the rubric in `starter-kits/legacy-bridge/BROWNFIELD_PLAN.md`. Use [`characterize-rewrite-leave-alone-rubric.md`](characterize-rewrite-leave-alone-rubric.md) for the decision discipline.

### What to do

- **Score 3-5 candidate services** using the selection rubric. Most modules score similarly; the differentiating factor is usually the willingness of a specific engineer to be the named owner.
- **Get explicit leadership sign-off** on the chosen service. Use [`first-conversation-with-leadership.md`](first-conversation-with-leadership.md) if you haven't already had this conversation.
- **Identify the named owner.** This is non-negotiable. A module without an owner cannot move beyond L0.
- **Write the 30-day plan for the chosen service.** Specifically: what gets characterized, what gets documented, what counts as Phase B success.

### Pass criterion

One service is chosen, an owner is named, leadership has signed off on the timeline, and you have a written plan for Phase B.

---

## Days 30-45 — Characterize the first service

Phase B begins. The work is unglamorous and the temptation to skip it is highest.

### What to do

- **Establish the golden master.** Per Ch 11 §11.6 Principle 2. For an API service, record-replay against production-like traffic. For a batch job, golden output files. For a UI, visual regression tests on key flows. Use the templates in `starter-kits/legacy-bridge/`.
- **Use AI agents to write characterization tests.** Per Ch 11 Rule Zero: "AI writes observation and characterization tests *before* it writes a refactor." This is the canonical AI-on-legacy use case. Have the agent observe behavior, propose tests that capture it, run them, and verify they catch deliberate breakages.
- **Build the verify command around the golden master.** `legacy-verify.sh <module>` should run unit tests, integration tests, and the golden-master replay.
- **Document the public API of the module.** As a side effect of writing the tests, you've documented the API. Capture it in a module README.
- **Document known invariants.** What does the module assume about its inputs? What guarantees does it make about its outputs? Per Ch 22, behavior preservation requires understanding behavior; characterize, then refactor.

### What NOT to do

- Don't refactor while characterizing. The temptation is real ("the agent already understands this; let me just have it clean up"). Resist. Refactor is Phase C work.
- Don't try for 100% coverage. The book's stance: golden-master coverage of the public API behavior is more important than line coverage.
- Don't promote the module's MVH level until tests actually catch deliberate breakage. Faux-tests are worse than no tests.

### Pass criterion

Module is at MVH Level 1-2: golden master tests cover ≥60% of public API behavior, verify command works, owner can review changes confidently, README exists.

---

## Days 45-60 — Stabilize the harness

The first service has tests; now make sure the harness around it works.

### What to do

- **Run the harness daily.** Every day for two weeks, run the verify command. Note flakes; investigate root causes.
- **Add module-specific CLAUDE.md content.** What does the agent need to know about this module to work in it productively? Invariants, gotchas, the patterns to follow, the things to avoid.
- **Add module-specific hooks if needed.** Per `starter-kits/legacy-bridge/CLAUDE.md`. A bash firewall, legacy-protected-paths, fence-new-violations as appropriate.
- **Try a small AI-assisted change in the module.** Specifically: a small bug fix or a small refactor. Run at L1 or L2 autonomy (per Ch 11 §11.6 Principle 7) — agent suggests, you implement, verify catches issues. The point is to test the harness.

### What NOT to do

- Don't try L3+ autonomy in legacy yet. Ch 11 is explicit: "Strict autonomy ceiling. Legacy work runs at L1 (suggest only) or L2 (single-file edits with mandatory review) for the first six months."
- Don't promote the module to L3 yet even if tests pass. You need 30 days of stable operation under L2 before promotion.

### Pass criterion

The harness is being used in daily work without breaking. At least one small AI-assisted change has shipped through it. The module README has accumulated agent-question-and-answer content as a side effect.

---

## Days 60-75 — First strangler-fig opportunity

Phase C. The first opportunity for new functionality alongside legacy code.

### What to do

- **Identify a piece of new functionality the team needs in this module's domain.** Specifically: something that could be built as a NEW module that interfaces with the legacy module, rather than as a change INSIDE the legacy module. Per Ch 11 §11.6 Principle 4: "New functionality goes in a new module with new tests."
- **Build the new module with full greenfield discipline.** AI tooling at full autonomy, comprehensive tests, modern patterns. This is the "new code lives next to old code" pattern from Ch 11 §11.4.
- **Connect the new module to the legacy module via a clear interface.** Specifically: the legacy module's public API is the contract; the new module calls into it (or wraps it).
- **Run both in parallel for a defined period** before making the new module the primary path. The strangler-fig pattern from Ch 11 §11.4: traffic shifts gradually, old code is deleted only after new path has owned 100% of traffic for a defined soak period.

### What NOT to do

- Don't refactor the legacy module to support the new functionality. Make the new functionality work AROUND the legacy module's existing interface.
- Don't delete legacy code yet. The strangler-fig pattern requires soak time; deletion is the last step, not the first.
- Don't claim "modernization" — you've added new code; the legacy is still legacy.

### Pass criterion

A new module exists alongside the legacy module. The new module has its own tests. The legacy module is unchanged but characterized. New functionality is shipping through the new module.

---

## Days 75-90 — Identify service #2 and write the next plan

Phase C continues. The first service is in steady-state operation; the next service is in the on-deck circle.

### What to do

- **Verify the first service is stable.** 30 days of L2 operation without regression escaping verify. If yes, promote to L3 readiness.
- **Update the module status tracker.** Service #1 has moved levels. Note what changed and how long it took.
- **Pick service #2** using the same rubric. Apply lessons learned from service #1.
- **Write the next 90-day plan.** Adjust based on what worked and what didn't.
- **Communicate progress to leadership.** Use [`first-conversation-with-leadership.md`](first-conversation-with-leadership.md) follow-up structure. The honest read: one service moved 1-2 levels; one identified next; this is on track per the realistic timeline.

### What NOT to do

- Don't claim victory. One service at MVH Level 2-3 in 90 days is the realistic outcome; declaring this "we've modernized" sets expectations you can't sustain.
- Don't skip the retrospective. What worked? What didn't? What would you do differently?

### Pass criterion at Day 90

- One service is at MVH Level 2-3 with a named owner, golden master tests, working verify command, module README, demonstrated AI-assisted shipping at L2 autonomy
- A second service is identified for the next 90 days
- The module status tracker is current
- Leadership has been briefed on realistic progress
- The team has built the muscle of "characterize first, refactor second"

---

## What if you fall behind

Falling behind is normal. The brownfield work is harder than greenfield work. The recovery patterns:

### If Phase A (Listen) takes longer than 30 days

- Often means the codebase is more sprawling than expected, OR institutional knowledge is more dispersed than expected
- Don't compress Phase A. Slip the schedule. The cost of skipping Phase A is much higher than the cost of slipping Phase B.

### If Phase B (Characterize) takes longer than expected

- Most common slip. Characterization is harder than it looks; legacy code has hidden coupling.
- Reduce scope. Characterize a smaller surface of the public API. Less coverage now, more iteration later.
- Accept MVH Level 1 instead of Level 2 at Day 60. Aim for Level 2 by Day 90 instead.

### If Phase C (Foothold) doesn't happen

- Sometimes the right answer is "we're still in Phase B at Day 90." That's fine.
- Communicate to leadership early. Don't surprise them at Day 90 with a slip; tell them at Day 60 if Phase C looks unlikely.
- The 90-day plan is a realistic ceiling, not a floor. Some brownfield work doesn't see Phase C until Day 120 or 150.

## What this plan will NOT do

- Will not work without the technical harness from `starter-kits/legacy-bridge/`. The plan is the human program; the kit is the technical scaffold. You need both.
- Will not work for an engineer who arrived expecting to "modernize" the codebase. Recalibrate expectations or part ways.
- Will not work in a culture that doesn't tolerate the unglamorous characterization work. If leadership demands visible feature delivery in week 4, this plan will be sacrificed.
- Will not work without leadership air cover for the 9-12 month realistic timeline.

## Companion artifacts

- [`first-conversation-with-leadership.md`](first-conversation-with-leadership.md) — the timeline-reset conversation
- [`characterize-rewrite-leave-alone-rubric.md`](characterize-rewrite-leave-alone-rubric.md) — the per-module decision
- [`anti-patterns.md`](anti-patterns.md) — the failure modes to avoid
- [`module-status-tracker-template.md`](module-status-tracker-template.md) — the living tracker
- [`reading-order.md`](reading-order.md) — what to read in week 1
- `starter-kits/legacy-bridge/` — the technical scaffold
- Ch 11 — the source
