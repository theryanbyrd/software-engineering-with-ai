---
name: strangler-pattern
description: Use when adding new functionality that interacts with legacy code. Builds the new functionality ALONGSIDE the legacy code, not inside it. Wraps and intercepts rather than modifying.
allowed_tools: Read, Edit, Write, Bash, Grep
---

# Strangler Pattern

You are adding new functionality to a legacy system. The rule is: **you do not edit the legacy code. You build alongside it.**

The strangler pattern (named for the strangler fig vine, which grows around a host tree until the host is no longer needed) lets you migrate functionality gradually without rewriting.

## Process

1. **Identify the seam.** Find the boundary where the legacy code can be intercepted: a public function, an HTTP endpoint, a message queue handler, a database trigger.

2. **Build a new module alongside.** New module has new tests, new code, new conventions (matching the greenfield starters). It does not import or modify legacy code.

3. **Route through the new module.** Add a routing layer (feature flag, config switch, request matcher) that decides whether a given request goes to the legacy implementation or the new one.

4. **Start with reads.** New module handles read traffic first. Legacy still handles writes. Compare outputs in production for a period. Build confidence.

5. **Migrate writes carefully.** Once read parity is proven, route some writes to the new module behind a feature flag. Watch error rates. Reverse the flag immediately if anything looks wrong.

6. **Eventually retire the legacy implementation.** Sometimes "eventually" is years. That is fine. The system runs both implementations during the transition; that's the point.

## What this skill DOES

- Designs the seam: where exactly we intercept
- Creates the new module structure with greenfield conventions
- Sets up the routing/feature-flag layer
- Designs the parity-check for read traffic
- Documents the migration plan in a markdown file

## What this skill does NOT do

- Modify the legacy code in any way (that's a different skill, used carefully).
- Promise a complete migration timeline (these take months to years).
- Skip the parity check (skipping it is how you produce silent regressions).

## Worked example

See [`examples/strangler-example.md`](../../../examples/strangler-example.md) for a worked example of strangling a legacy `getUserPreferences` function over 8 weeks.

## When NOT to use this skill

- For pure bug fixes in legacy code that can't be wrapped (you might need to make a single-file edit instead — see `characterize-then-refactor`).
- When the legacy code is already at MVH Level 4 (then use the greenfield skills).
- When the proposed change is so small that a strangler is overkill. Use judgment.
