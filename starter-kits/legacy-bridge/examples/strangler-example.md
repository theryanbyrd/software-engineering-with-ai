# Worked Example — Strangling `getUserPreferences` over 8 Weeks

A realistic walkthrough of brownfield AI work using the strangler pattern. The names are fictional, the structure is real.

## The setup

A 70-engineer SaaS company with a 9-year-old Rails monolith. The `User#preferences` method on the `User` model has grown to ~600 lines, mixes business logic with database access, and has roughly 30% test coverage. Every release introduces small bugs in user preferences. The engineer who wrote it left in 2022.

The team has decided to apply the brownfield bridge to this corner of the codebase first because:

- Recent changes have been disproportionately error-prone (criterion 1 from BROWNFIELD_PLAN.md)
- The original author is gone and the current owner doesn't trust their own changes (criterion 2)
- It's NOT in the auth/billing hot zone, so the cost of mistakes is moderate (anti-criterion: stay out of the hottest zones first)

The goal: build a new `UserPreferencesService` alongside `User#preferences`, prove parity, then migrate writers one at a time. Plan: 8 weeks to first read-traffic migration; full deprecation when the team is ready (probably 12-18 months).

---

## Week 1 — Setup

### Day 1: Selection memo

Owner: Maria. She has 18 months on the codebase, knows preferences "well enough to be dangerous." She gets two days a week for the next 8 weeks for this work.

Selection memo signed off by CTO. Maria's quarterly OKR adjusted to reflect the 40% time commitment.

### Day 2-3: Discovery setup

Maria runs `bash legacy-bridge-scripts/discover.sh`. Output flags:
- 47 files in `app/models/user/` haven't been touched in 18+ months
- 142 TODOs across the user-related code
- No README at module level

She copies the legacy-bridge starter into the repo:
```bash
cp -r legacy-bridge/.claude .
cp -r legacy-bridge/scripts legacy-bridge-scripts
cp legacy-bridge/CLAUDE.md .
cp legacy-bridge/BROWNFIELD_PLAN.md .
```

She customizes `CLAUDE.md`:
- Module Status table: `app/models/user/preferences.rb` listed as L0
- Restricted paths: adds the entire `app/models/user/` to the hard-blocked list initially
- Owner: Maria

### Day 4-5: Module-level README

Maria asks Claude (using the `legacy-explorer` subagent) the first batch of questions:

> "Read `app/models/user/preferences.rb` and tell me: what's the public API? Who calls these methods? Are there any clearly-distinct behaviors I should know about?"

Claude reads the file, runs grep for callers, and returns a structured answer. Maria reviews it. The Q&A goes into a new `docs/modules/user-preferences/README.md` (the first module README that has ever existed).

By end of Week 1: a draft module README, a working CLAUDE.md, and the L0 status acknowledged.

---

## Week 2 — Read-only discovery

Maria runs five more discovery sessions with the `legacy-explorer`:

1. **What does `apply_preferences_for_billing` do?** Turns out it's a 90-line method that handles three completely different cases (invoice formatting, payment retries, subscription warnings) based on a `mode:` parameter. Each should be its own method. Documented as known weirdness.
2. **What's the relationship between `User#preferences` and `UserPreferencesAudit`?** They double-write to two tables but with different schemas. Documented; flagged as a future cleanup target.
3. **Why does `serialize_for_email` return three different shapes?** It checks the year of `created_at` — users created before 2019 get one shape, 2019-2022 another, post-2022 a third. This is "preserved for backward compatibility with the v1 API." Confirmed by checking the v1 API docs (which Maria didn't know existed).
4. **What's tested?** Coverage tool says 31%. Claude finds tests for the happy path on `read_preferences` but nothing for `update_preferences`. Tests for the v1 serialization shape are dated 2019 and import a helper that no longer exists; they were silently broken for years.
5. **What invariants are documented?** Three. The other ~25 invariants in the code are not documented anywhere. Maria captures them in the README.

By end of Week 2: the module README is genuinely useful. Twenty-five invariants documented for the first time. Maria knows what she's working with.

---

## Week 3 — Golden master

The decision: capture current behavior of `User#preferences` for the read paths first, since reads are 95% of traffic and far easier to make idempotent.

### Day 1-2: Pick the test surface

Maria identifies 12 distinct read scenarios:
- Default user, no preferences set
- User with all preferences set (legacy 2018 shape)
- User with all preferences set (2020 shape)
- User with all preferences set (current shape)
- User with the v1-API-compatible weird path
- ... 7 more edge cases

### Day 3-4: Record golden master

```bash
bash legacy-bridge-scripts/golden-master-record.sh user-preferences
```

The scaffold is customized to:
- Set up 12 fixture users with known preferences
- Call `User#preferences.read_for_email`, `read_for_billing`, `read_for_admin` on each
- Capture the JSON output to `tests/golden/user-preferences/expected/`

### Day 5: Verify

Maria runs the golden master against the current code: passes (12/12).

She then deliberately breaks the code (comments out the v1-shape fork): the golden master fails for 4 of 12 scenarios. The breakage is detected. The golden master is real.

By end of Week 3: golden master in place, `legacy-verify.sh user-preferences` runs and detects regressions.

---

## Week 4 — Build the new module structure

The new module: `app/services/user_preferences_service/`. Greenfield-style:
- Strict types (Sorbet for Ruby)
- Test coverage target: 90%
- One responsibility per file
- All inputs validated
- Clear public API

The first version implements the simplest read path: `UserPreferencesService.read(user_id)` returns the modern shape only. No legacy compatibility yet.

Maria writes 28 tests for the new service before writing the service code. They're real assertions on expected behavior, not characterization tests — this is greenfield work. All pass.

By end of Week 4: a working new service, but it doesn't handle the legacy shapes yet, so it can't fully replace `User#preferences`.

---

## Weeks 5-6 — Routing layer + parity check

Now the strangler glue.

### The router

`app/services/user_preferences_router.rb`:

```ruby
class UserPreferencesRouter
  def self.read(user_id, mode:)
    # Feature flag controls which implementation handles the call
    if Flipper.enabled?(:new_preferences_read, user_id) && mode == :modern
      UserPreferencesService.read(user_id)
    else
      User.find(user_id).preferences.send("read_for_#{mode}")
    end
  end
end
```

### The parity-check job

A nightly job that:
1. Picks 1000 random user IDs
2. Calls both implementations
3. Compares outputs
4. Reports differences to a dashboard

Week 5: Maria runs parity check. Difference rate: 23%. Most differences are the v1 shape (which the new service doesn't handle yet). Maria adds the v1 shape support to the new service (carefully — characterization tests prove the shape) over 3 days.

Week 6: Difference rate down to 0.4%. The remaining differences are:
- Two users with corrupted data in the legacy table (preferences referring to deleted features)
- A timezone bug in the legacy shape (preferences read at 23:50 PST get marked as next day)

Maria documents these as known divergences. The new service treats both as "fixed" — corrupted data is filtered out, timezones are correct. She adds tests asserting the new behavior.

By end of Week 6: parity-check shows 99.6% match, with documented divergences that are improvements rather than regressions.

---

## Week 7 — First production read traffic

Feature flag enabled for 1% of users. The new service handles their reads.

Day 1: Error rate on `:new_preferences_read` is 0.02%. Within noise.

Day 2: One user reports a bug. Maria checks the logs — turns out the user has a preference value with a non-UTF-8 byte sequence (legacy data corruption). The new service's stricter validation rejects it; the old code would silently include it. Maria adds a fallback that handles this edge case explicitly with a logged warning.

Day 3: Re-deploy. Error rate drops to 0%.

Day 4-5: Ramp to 10% of users. No incidents.

By end of Week 7: 10% of read traffic on the new service. Dashboard shows parity. No customer-facing issues.

---

## Week 8 — Document and plan next phase

Maria writes the migration retrospective:

- **What worked:** The 2-week read-only period was painful but invaluable. The golden master caught two regressions during development that would have shipped otherwise. Parity-check job identified the timezone bug we didn't know we had.
- **What didn't work:** Estimated 4 weeks for golden master + new service. Took 6. The legacy shapes were uglier than expected.
- **What to take to the next module:** Skip nothing. Compress nothing. Document the "improvements" (timezone fix, corrupted-data filtering) as separate items so they can be backported to other systems if useful.

Module Status table in CLAUDE.md updated:
- `app/services/user_preferences_service/` → L4 (greenfield-equivalent)
- `app/models/user/preferences.rb` → L1 (mapped, but still off-limits for direct edit)

Plan for next 6 months:
- Continue ramping new service: 25% → 50% → 100% of read traffic over 6 weeks
- Then start migrating writes: 1% → 10% → 100% over 8 weeks
- Then mark `app/models/user/preferences.rb` as deprecated; legacy code stays in place but new development goes to the new service
- Full deletion of legacy code: probably 12-18 months out, after we're confident no callers remain

By end of Week 8: clean handoff ready. The team has a worked example. The next module starts in Week 9.

---

## Lessons

### Things that worked

1. **Picking a non-hot-zone first.** Preferences are important but not auth or billing. Mistakes were recoverable.
2. **The 2-week read-only period.** Felt slow but surfaced 25 invariants we didn't know about.
3. **Parity check job.** Removed argument about whether the new service was "right" — it just compared outputs.
4. **Feature flag at 1% first.** Caught the UTF-8 issue before it could affect more users.

### Things that didn't work

1. **Initial estimate was 4 weeks.** Realistic timeline is 8. The legacy code is always weirder than expected.
2. **First version of the new service.** Tried to implement v1, v2, and modern shapes simultaneously. Had to refactor in Week 5 to handle one shape per release.
3. **The discover.sh output.** Was useful but not enough for the selection decision. Maria's domain knowledge mattered more than the tool.

### What we'd do differently

- Plan for 8-12 weeks per module from the start. Stop pretending it can be 4.
- Start the parity-check infrastructure earlier (in parallel with golden master, not after).
- Write the module README during the read-only period AND keep updating it weekly. The end-of-Week-2 README was missing things we discovered in Week 5.

### What we will NOT do differently

- The 2-week read-only period. This is the discipline.
- The 100-line PR cap on legacy work. We had to make 11 PRs to ship the new service. The cumulative review time was less than one big PR would have been.
- The sign-off chain at every promotion (L0 → L1 → L2 → L3 → L4). Each level is a real gate; we never skipped one.

---

## Closing thought

The goal was not to "modernize the user preferences system." The goal was to ESTABLISH A PATTERN we can repeat for the next 50 modules in this codebase. The 8 weeks of work on this module is the cost of building that pattern. The next module will be faster — maybe 5 weeks — because the harness, the parity-check job, the golden-master scaffolding, and the team's confidence are now in place.

That's the brownfield bargain: slow first, faster compounding later.
