# Module Status Tracker — Template

The living document tracking every module the team owns. The Module Status Tracker is the engineering equivalent of a financial register: it tracks the inventory, the state of each, and the planned action.

Update at minimum monthly. The tracker drives the module-by-module decisions and informs leadership conversations.

## How to use this template

1. Copy this file to a location you'll maintain (a shared doc, a wiki page, or `docs/MODULE_STATUS.md` in your repo)
2. List every module the team owns
3. Score each per the columns below
4. Update at minimum monthly; ideally as part of the team's regular cadence

## The fields

| Field | What it captures |
|---|---|
| **Module** | The unit of code. Should match a directory or service that someone could own. |
| **Owner** | A specific engineer's name. "No owner" is a finding. |
| **Lines of code** | Roughly. Within 20% is fine. |
| **MVH Level** | 0-4 per `starter-kits/legacy-bridge/MVH_LEVELS.md` |
| **Rubric score** | 0-15 from `characterize-rewrite-leave-alone-rubric.md` |
| **Recommendation** | Leave alone / Characterize / Strangler-fig / Consider rewrite |
| **In-flight work** | What's currently happening (or "nothing planned") |
| **Last updated** | Date of most recent assessment |

## Template

```
| Module | Owner | LOC | MVH | Rubric | Recommendation | In-flight | Last updated |
|---|---|---|---|---|---|---|---|
| billing-service | @rbyrd | 12,400 | L2 | 7 | Characterize | Adding edge-case golden tests | 2026-05-15 |
| auth-legacy | NO OWNER | 8,200 | L0 | 11 | Characterize, then strangler-fig | None planned | 2026-05-15 |
| reporting-engine | @kchen | 24,000 | L1 | 9 | Characterize, then strangler-fig | Reading only — Phase A complete | 2026-05-15 |
| schedule-2010 | @blee | 18,000 | L0 | 13 | Consider rewrite (failed readiness check; defaulted to characterize+strangler) | Read-only AI sessions ongoing | 2026-05-15 |
| user-prefs | @rbyrd | 3,400 | L3 | 4 | Leave alone with light characterization | None planned | 2026-04-22 |
| api-gateway | @ssmith | 5,800 | L2 | 5 | Characterize | None planned (steady state) | 2026-05-08 |
```

## Common patterns

### Pattern 1 — Most modules are at L0 or L1

Normal for a brownfield codebase. Don't panic. The 30/60/90 plan moves 1-2 modules at a time.

### Pattern 2 — High-rubric-score modules dominate

If multiple modules score 12+, the team has bigger problems than module-by-module work can solve. Talk to leadership about whether wholesale recapitalization (significant team additions, dedicated modernization budget, or a different strategy) is needed.

### Pattern 3 — "No owner" appears multiple times

This is its own problem. Modules without owners can't move beyond L0. The conversation: who's going to own these? Either name owners or accept that the modules stay at L0 indefinitely.

### Pattern 4 — A module's MVH level decreases

Rare but real. Usually means tests have decayed (new code paths added without test updates) or the documented owner left and nobody picked up. Investigate.

### Pattern 5 — A module is at L3+ but rubric score is high

The harness has gotten the module to a usable state, but the underlying code is still problematic. The harness is doing its job — making it safe to work in code that isn't ideal. This is fine. Modernization remains a separate project.

## What this template will NOT do

- Will not stay current without discipline. Schedule the update.
- Will not capture all the relevant data. Add columns as your team needs (e.g., "regulatory scope," "downstream dependencies," "deployment cadence").
- Will not replace the harness work. The tracker is the dashboard; the work is in the modules.

## Companion artifacts

- [`30-60-90-day-plan.md`](30-60-90-day-plan.md) — uses the tracker for service selection
- [`characterize-rewrite-leave-alone-rubric.md`](characterize-rewrite-leave-alone-rubric.md) — produces the rubric column
- `starter-kits/legacy-bridge/MVH_LEVELS.md` — produces the MVH column
- Ch 11 — source
