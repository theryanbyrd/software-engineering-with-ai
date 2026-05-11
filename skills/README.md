# Skills Library — 12 Starter Skills

The company-standard starter set from Chapter 13 §13.3 and Appendix E of [_Software Engineering with AI: A Practical Handbook for the Claude Code Era_](https://www.linkedin.com/in/ryanbyrd) by Ryan Byrd.

Each skill is a folder with a `SKILL.md` containing the playbook. Drop into your repo's `.claude/skills/` directory (or copy individual ones).

## Layout

```
skills/
├── code-review/SKILL.md
├── write-tests/SKILL.md
├── bug-reproduction/SKILL.md
├── add-api-endpoint/SKILL.md
├── db-migration/SKILL.md
├── security-review/SKILL.md
├── frontend-component/SKILL.md
├── observability-change/SKILL.md
├── performance-review/SKILL.md
├── refactor-safely/SKILL.md
├── incident-fix/SKILL.md
└── dependency-upgrade/SKILL.md
```

## How to use

Skills are invoked by description-matching, not by name. When the user's request matches a skill's description, Claude Code (or any AGENTS.md-aware tool) loads the SKILL.md and follows it.

```bash
# Drop skills into your repo
cp -r skills/* /path/to/your/repo/.claude/skills/

# Or pick the ones you need
cp -r skills/code-review skills/write-tests skills/db-migration /path/to/your/repo/.claude/skills/
```

## The 12 skills

| Skill | When | Output |
|---|---|---|
| [`code-review`](code-review/SKILL.md) | Review a diff or PR | Structured review with severity tags |
| [`write-tests`](write-tests/SKILL.md) | Tests are missing or thin | Behavior-focused tests that fail when code is broken |
| [`bug-reproduction`](bug-reproduction/SKILL.md) | A bug report needs a reproduction | A failing test |
| [`add-api-endpoint`](add-api-endpoint/SKILL.md) | New endpoint needed | Endpoint + tests + docs following conventions |
| [`db-migration`](db-migration/SKILL.md) | Schema change requested | Forward + backward migration + deploy plan |
| [`security-review`](security-review/SKILL.md) | Adversarial review of a diff | Findings with severity, no false confidence |
| [`frontend-component`](frontend-component/SKILL.md) | UI component needed | Component + tests + Storybook (if applicable) |
| [`observability-change`](observability-change/SKILL.md) | Metrics/logs/traces needed | Telemetry added consistently |
| [`performance-review`](performance-review/SKILL.md) | Hot path identified | Profile, hotspots, proposed changes (no premature optimization) |
| [`refactor-safely`](refactor-safely/SKILL.md) | Refactor a working thing | Small reversible steps, tests at each step |
| [`incident-fix`](incident-fix/SKILL.md) | Active or recent incident | Reproduction, root cause, fix, postmortem note |
| [`dependency-upgrade`](dependency-upgrade/SKILL.md) | Bump a dependency | Upgrade + change matrix + verify |

## Skill quality bar

Every skill in this library satisfies these criteria:

1. **Specific trigger.** The `description:` field in frontmatter is precise enough that Claude knows when to invoke. *"When the user asks for a schema change, column add/drop, index change, or data backfill"* — not *"when working with databases"*.
2. **Plan-first procedure.** Every skill's procedure ends with "wait for user approval before writing files" or equivalent. Skills do not silently execute.
3. **Forbidden section.** Each skill has a `## Forbidden` section listing what the skill must NEVER do, regardless of user instruction.
4. **References.** Skills point to the conventions document, the relevant chapter, or the deeper how-to guide.
5. **Output is reviewable.** The output of each skill is small enough that a human can review in <10 minutes.

## Extending the library

To add a new skill, copy [`_TEMPLATE.md`](_TEMPLATE.md) into a new folder. The bar for inclusion in this library is high: the skill must be useful across a wide range of repos, not specific to one team's stack. Team-specific skills should live in your team's repo, not here.

## Pairing with subagents and hooks

These skills work best in combination with:

- The starter subagents (planner, reviewer, test-writer) — see Appendix F
- The starter hooks (bash-firewall, protected-paths, post-edit-format) — see Appendix G

A skill running in the absence of a harness produces faster slop. With the harness, it produces faster reliable work.
