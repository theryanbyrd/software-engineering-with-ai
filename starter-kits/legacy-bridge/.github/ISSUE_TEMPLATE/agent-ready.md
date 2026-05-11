---
name: Agent-ready issue (brownfield)
about: A spec ready for an AI agent in legacy code
labels: agent-ready, brownfield
---

## Goal

<!-- One sentence. -->

## Module(s) involved

- Module: `<name>`
- Current MVH Level (from MVH_LEVELS.md): `<0-4>`
- If the module is at L0, this issue should be a discovery issue, not a change issue.

## Strategy

- [ ] Strangler pattern (preferred for new functionality)
- [ ] Characterize-then-refactor (only if direct legacy edit is required)
- [ ] Read-only discovery (no changes; documentation outcome)

## Acceptance criteria

- [ ] (specific, testable)
- [ ] `legacy-verify.sh <module>` passes
- [ ] Golden master replay passes (or N/A explained)

## Files likely to change

<!-- List paths the agent should expect to touch. -->

## Files NOT to touch

<!-- Restricted paths or out-of-scope areas. -->

## Tests required

<!-- Characterization tests (capturing CURRENT behavior, not CORRECT behavior). -->

## Context links

- Module README: <link>
- Architecture (as known): <link>
- Related discovery notes: <link>

## Notes

<!-- Anything else, including known unknowns. -->
