---
name: dependency-upgrade
description: Use when upgrading a dependency (one library, one version). Reads the changelog, runs the change matrix (build, test, smoke), updates the lock file, and produces a one-page upgrade summary. Does NOT do mass upgrades — those are a separate strategic task.
allowed_tools: Read, Edit, Bash, Grep, WebFetch
---

# Dependency upgrade

## When to use this skill

The user asks to upgrade a specific dependency: "bump X to vN," "upgrade React to 19," "we need a security patch on package Y."

## Procedure

1. **Confirm the version target.** If the user said "latest," explicitly check what "latest" is and confirm. Major-version bumps are different from patch bumps; verify intent.
2. **Read the changelog/release notes.** For npm: `npm view PKG@VERSION`. For pip: PyPI release page. For others: GitHub releases. Note breaking changes, deprecations, behavior changes.
3. **Identify code that will need to change.** Search the codebase for usage of the dependency's API. Grep for imports.
4. **State the plan.** Version bump, files that need to change, breaking changes that affect us. Wait for approval.
5. **Update the dependency:**
   - Bump in package.json / pyproject.toml / Gemfile / go.mod
   - Regenerate the lock file (`npm install`, `pip install -e .`, `bundle install`, `go mod tidy`)
   - Update import sites that broke
6. **Run the change matrix:**
   - `verify` (lint + typecheck + tests + format)
   - The full test suite
   - A smoke test of the most affected feature, if applicable
   - If the codebase has integration tests, run them
7. **Output the upgrade summary.**

## Output

```
## Dependency upgrade summary

**Package:** <name>
**Version:** <old> → <new>
**Type:** patch / minor / major

## Changes

- Breaking: <list with files affected>
- Deprecations: <list>
- New behavior we now use: <list, or "none">

## Verification

- [ ] verify passes
- [ ] full test suite passes  
- [ ] smoke test passes (if applicable)
- [ ] no new lint warnings introduced

## Risk assessment

**Affected code paths:** <list>
**Suggested rollback:** revert this PR + `npm install` to restore lock

## Follow-up actions

(Optional — if the upgrade enables new patterns, list opportunities here as separate issues)
```

## Forbidden

- Do not upgrade multiple dependencies at once. One per PR. Mass upgrades hide which package broke what.
- Do not skip reading the changelog. The 30 seconds saved are not worth the surprise.
- Do not skip the smoke test for a major-version bump.
- Do not commit the lock file change without running install in a clean environment first (lock files often have machine-specific differences; resolve before committing).
- Do not upgrade a transitively-pinned dependency by removing the pin. The pin probably exists for a reason.

## References

- Chapter 23 §23.x — supply chain risk
- Chapter 38 §38.x — vendor risk and procurement (for dependency-as-vendor framing)
