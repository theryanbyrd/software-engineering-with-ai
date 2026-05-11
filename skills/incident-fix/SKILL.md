---
name: incident-fix
description: Use during an active or recently-resolved incident. Reproduces the failure, identifies root cause, proposes the fix, and writes a postmortem note. The fix is the secondary deliverable; the postmortem note is the primary one.
allowed_tools: Read, Edit, Write, Bash, Grep
---

# Incident fix

## When to use this skill

There is an active incident (still occurring), a recently-resolved one (the team is in cleanup), or a near-miss that needs forensic understanding.

## Procedure

1. **Stabilize first, learn second.** If the incident is active, the agent's job is to help reproduce and propose, not to ship a fix during the active fire. The on-call human decides what gets shipped during the incident.
2. **Reproduce the failure.** In a test environment if possible. Use the bug-reproduction skill's pattern: write a failing test that captures the exact failure mode.
3. **Identify the root cause.** Read the code in the failure path. Look at the recent diff (likely cause: a recent change). Check for: race conditions, unhandled error paths, missing validation, dependency upgrade side effects, resource exhaustion.
4. **Propose the fix.** Smallest change that resolves the root cause. NOT a refactor. NOT a "while we're in there" cleanup.
5. **Write the postmortem note.** This is required even if the fix is trivial. Format:
```
**Title:** <one-line description>
**Date:** <YYYY-MM-DD>
**Duration:** <minutes/hours, customer-facing>
**Severity:** SEV1/2/3
**Root cause:** <one paragraph>
**Trigger:** <what set it off>
**Resolution:** <what fixed it>
**Detection:** <how we noticed; how should we have noticed faster?>
**Action items:** <list with owners>
**AI authorship of root cause:** <yes/no — if AI authored the offending code, note it; this is a Ch 31 §31.6 disclosure>
```
6. **Run `verify`** including the new failing-test-now-passing.

## Output

- The fix (smallest change that addresses root cause)
- The reproduction test (now passing with the fix applied)
- The postmortem note (markdown, ready to drop in `docs/postmortems/`)

## Forbidden

- Do not refactor while fixing an incident. Single-purpose change.
- Do not skip the postmortem. The note is a deliverable, not optional.
- Do not invent a root cause if you don't have one. "Likely cause" is not a root cause; if uncertain, the postmortem says "investigation pending" and lists what to instrument next.
- Do not bypass verify. Even in an incident, the test must pass.
- Do not blame an individual in the postmortem. Blame the system, the process, the missing safeguard.

## References

- Chapter 39 §39.x — AI-aware incident response
- Chapter 31 §31.6 — AI authorship attribution in postmortems
