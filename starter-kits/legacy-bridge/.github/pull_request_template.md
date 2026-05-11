## What

<!-- One-paragraph description. -->

## Why

<!-- Why this change, why now. Link to ticket. -->

## Module(s) and MVH level

- Module: `<module-name>` — current MVH Level: `<0/1/2/3/4>` (per `MVH_LEVELS.md`)
- Owner: `<name>`

## Strategy used

- [ ] Strangler pattern (built alongside legacy)
- [ ] Characterize-then-refactor (direct edit with tests)
- [ ] Read-only discovery (no code changes; documentation only)

## AI authorship

- [ ] `ai:none` — entirely human-written
- [ ] `ai:assisted` — significant AI authorship; reviewed in detail
- [ ] `ai:authored` — primarily AI-generated; double-reviewed
- [ ] `ai:agent` — produced by an autonomous agent run

## Brownfield-specific verification

- [ ] `bash legacy-bridge-scripts/legacy-verify.sh <module>` passes
- [ ] Golden master replay passes (or N/A — module is at L0/L1)
- [ ] Characterization tests added or updated for changed legacy code (or N/A — no legacy code touched)
- [ ] Diff is under 100 lines (or decomposition is justified below)
- [ ] No new `# type: ignore`, `// @ts-ignore`, or similar
- [ ] No silenced/skipped/deleted tests
- [ ] Module Status table in `CLAUDE.md` updated if invariants discovered
- [ ] No paths outside the allowlist touched

## Risks

<!-- What might break? What's the rollback? Is the change behind a feature flag? -->

## What's still UNKNOWN

<!-- This section is brownfield-specific. List anything you read in the legacy
     code that you DID NOT fully understand. The reviewer will help you
     fill gaps before merging. -->

## Reviewer notes

<!-- Anything to flag for the reviewer. -->
