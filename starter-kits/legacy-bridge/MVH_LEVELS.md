# MVH Levels — Brownfield Maturity Rubric

A 4-level scoring rubric for the maturity of your brownfield AI harness on a per-module basis. Use to track progress on each service you bring under harness.

**Important:** these levels are PER MODULE, not per codebase. A typical legacy codebase will have modules at different levels for years. That is fine. Trying to bring the whole codebase to Level 4 simultaneously is the most common brownfield mistake.

---

## Level 0 — Off-limits

**Description:** No tests, no documentation, no characterization. Nobody alive understands the module. Nobody has read it in 18 months.

**AI access:** Read-only exploration sessions only. Agent can be asked questions; agent cannot edit.

**Required to graduate to L1:**
- Identify at least one engineer willing to be the named owner
- Read and document the public API of the module (functions/methods/endpoints exposed)
- Document at least 3 known-or-suspected invariants in the Module Status table
- 2 weeks of read-only exploration sessions documented

---

## Level 1 — Mapped

**Description:** Public API is documented. Owner is named. At least 3 invariants are written down. The module appears in the Module Status table.

**AI access:** L1 (suggest only) on the module. Agent proposes changes; human implements after review.

**Required to graduate to L2:**
- Golden master tests cover at least 60% of the public API behavior
- `legacy-verify.sh <module>` runs and catches deliberate-breakage tests
- At least one human (the owner) can confidently review changes
- README exists at module level with: purpose, entry points, known gotchas

---

## Level 2 — Bridged

**Description:** Golden master tests in place. Verify command works. Owner can review changes. README exists.

**AI access:** L2 (single-file edits with mandatory review). Agent can edit one file at a time. Every change must pass `legacy-verify.sh`. PR size capped at 100 lines.

**Required to graduate to L3:**
- Unit tests cover >40% of the module
- Strangler-pattern in active use: at least one new feature has been built ALONGSIDE the legacy code rather than IN it
- 30 days of L2 operation without a regression escaping verify
- Module-level architecture document exists, even if rough

---

## Level 3 — Hardened

**Description:** Unit tests cover meaningful portions. Strangler pattern in active use. 30 days of clean L2 operation. Architecture documented.

**AI access:** L2 by default; L3 (multi-file changes with review) for explicit ticket-driven work in non-restricted parts of the module. PR size cap relaxed to 200 lines for this module.

**Required to graduate to L4:**
- Unit tests cover >75%
- Mutation testing baseline established (50%+ score)
- ADRs (architecture decision records) exist for major decisions in this module
- Code review backlog from AI changes is sustainably managed (no piling up)
- Module is materially indistinguishable from a greenfield module from the AI's perspective

---

## Level 4 — Greenfield-equivalent

**Description:** Module is now indistinguishable from a greenfield module. Tests are good. Documentation is current. Owner is established. Strangler-pattern complete.

**AI access:** Same as the greenfield starter kit (TS or Python). Default L2, L3 with review, PR cap 400 lines. Standard skills apply.

**At this point:** the module has graduated out of the brownfield bridge. Switch to the greenfield TS or Python starter for this module.

---

## How to use this rubric

### Quarterly assessment

Once per quarter, score each module under bridge in the codebase. Track:

- Module name
- Current MVH level
- Time at this level
- Blockers to next level
- Owner
- Next milestone date

### Realistic timelines

A typical service's progression through these levels:

- L0 → L1: 2-4 weeks (concentrated discovery)
- L1 → L2: 4-8 weeks (golden master + verify infrastructure)
- L2 → L3: 3-6 months (real test coverage takes time)
- L3 → L4: 6-12 months (mutation score, ADRs, full strangler)

**Total:** 12-24 months per service to reach greenfield-equivalence. This is why brownfield is a multi-year program.

### What NOT to do

- Don't move all modules simultaneously. Move one. Then the next.
- Don't aspire to L4 across the whole codebase. Many modules will live at L2 or L3 forever, and that's fine.
- Don't compress timelines because leadership wants progress reports. Compressed timelines on brownfield produce regressions that wipe out months of progress.
- Don't graduate a module to a higher level just because the calendar says so. The criteria are not negotiable.

---

## Sample assessment table

```
| Module           | Current | Days at level | Blocker to next                  | Owner       |
|------------------|---------|---------------|----------------------------------|-------------|
| api/v2/orders    | L3      | 45            | Mutation testing baseline (50%)  | A. Ramirez  |
| legacy/billing   | L1      | 90            | Golden master coverage (60%)     | C. Park     |
| core/scheduler   | L0      | —             | Need owner; nobody assigned      | UNASSIGNED  |
| api/v2/customer  | L4      | 60            | Graduate to greenfield starter   | A. Ramirez  |
```

This table is the artifact you bring to your CTO each quarter. It is honest about progress and honest about what's blocking each module.
