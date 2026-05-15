# Agent-Ready Issue Template

Companion to *Software Engineering with AI* by Ryan Byrd · Appendix C / Chapter 19

Copy the markdown below into your issue tracker's template (Linear, Jira, GitHub Issues). The shape is the contract — agents read it; humans read it; both should get the same answer to "what is this issue asking for?"

```markdown
## Tier
T1 (Simple) | T2 (Inspection) | T3 (Architecting) — pick one

## Objective
One sentence describing the desired outcome in user-visible terms.

## Current behavior
What the system does now. Cite files.

## Desired behavior
What it should do. Be concrete.

## Scope
- In: list specific files, modules, or areas
- Out: explicit non-scope items

## Acceptance criteria
- [ ] Behavior X is true (test: `path/to/test.spec.ts::it('does X')`)
- [ ] Behavior Y is true
- [ ] No existing tests fail
- [ ] No new lint or typecheck errors

## Required tests
Concrete test names or scenarios to add.

## Commands the agent will use
- `pnpm verify`
- `pnpm --filter <pkg> test`

## Risk and blast radius
- Touched areas: <list>
- User-facing? Y/N
- Data-affecting? Y/N
- Reversible? Y/N

## Approval-required checkpoints
- After plan, before implementation
- Before any DB migration
- Before any change to <restricted areas>

## Tool / model
Default: Claude Code, Sonnet 4.6. Escalate to Opus 4.7 if architectural questions arise.
```

## Quality bar

- **A T3 issue cannot one-shot.** If you find yourself wanting to write "the agent should figure out X," upgrade to T3 and add the design conversation upstream.
- **Acceptance criteria must be machine-checkable.** "Looks good" is not a criterion.
- **Scope must list out-of-scope items explicitly.** Without "Out:", agents expand scope to feel useful (Chapter 2 on self-congratulation).
