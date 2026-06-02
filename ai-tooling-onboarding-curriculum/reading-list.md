# Reading List — The First Week

The ordered set of book chapters and internal documents to read in week 1. This is a structured curriculum, not a dump of everything.

## Day 1 reading (priority order)

### Tier 1 — must read

1. **Company CLAUDE.md** — the company-wide context for AI tooling
2. **Team AGENTS.md** — the team-specific agent guidance
3. **The team's published autonomy ladder** — what level for what work

### Tier 2 — should read

4. **`do-not-automate-catalog/tier-1-never-autonomous.md`** — the work the agent doesn't do
5. **`do-not-automate-catalog/tier-2-mandatory-human-gate.md`**
6. **`do-not-automate-catalog/tier-3-light-human-gate.md`**
7. **`agent-autonomy-levels/autonomy-ladder.md`** — the broader framework
8. **`agent-autonomy-levels/forbidden-categories.md`** — the L5 list

### Tier 3 — nice to have

9. **The team's published list of skills** (overview, not deep)
10. **The team's published security policy / SECURITY.md**
11. **Any team-specific onboarding docs**

### What NOT to read on day 1

- Don't read the codebase yet. The engineer doesn't have context to interpret it.
- Don't read about competitor tools or vendor materials.
- Don't read advanced topics (custom subagents, MCP server design, etc.). They come later.

## Days 2-5 reading

Focused on the skills, subagents, hooks the engineer is exercising:

### Day 2 reading

- The README for each skill the engineer is touring
- The team's subagent documentation (or `subagents/` README equivalent)
- The team's hook documentation

### Day 3 reading

- The team's agent-ready issue template / examples
- 2-3 examples of well-written team issues from the last quarter

### Day 4 reading

- The team's PR template
- 2-3 examples of well-merged PRs from the last quarter (positive examples)
- (Optional, if available) 1-2 examples of PRs that needed substantial rework (educational)

### Day 5 reading

- `prompt-injection-test-suite/README.md`
- `prompt-injection-test-suite/test-cases/01-poisoned-issue-body.md` through `06-credential-in-output.md`
- `agent-autonomy-levels/forbidden-categories.md` (re-read with security lens)

## Book chapters (for those with access)

Per the book's framing, certain chapters are most useful in week 1:

### Day 1
- **Ch 1** — the AI-native reality (orientation)
- **Ch 32** — autonomy levels (the framework)
- **Ch 33** — do-not-automate catalog

### Day 2
- **Ch 6** — the harness (CLAUDE.md, AGENTS.md, llms.txt)
- **Ch 7** — verify command
- **Ch 13-15** — skills, subagents, hooks (skim; deep reading later)

### Day 3
- **Ch 19** — agent-ready issues (the canonical guide)

### Day 4
- **Ch 22** — code review and the seven slop signatures
- **Ch 20** — plan/implement/review loop

### Day 5
- **Ch 36** — security threat model
- **Ch 37** — prompt injection exercises

### Days 8-30 reading

By day 30, the engineer should have seen:
- **Ch 20-23** — the broader workflow chapters
- **Ch 31** — the metrics and dashboard
- **Ch 38** — vendor procurement (overview)
- **Ch 41** — adjacent governance
- **Ch 44** — the chapter this curriculum implements (read once the curriculum is internalized; meta-perspective)

Don't try to read all of these in week 1. They come as the engineer encounters relevant work.

## How to read

### Active reading

Don't read passively. While reading:
- Note what you don't understand
- Note what surprises you
- Note things that don't match your prior experience

These notes drive the day-by-day check-ins with the buddy.

### Don't try to memorize

Week 1 is first-pass. The engineer will re-read parts of these documents many times in the first 90 days; memorization isn't the point. Familiarity and "I know where to look" is the point.

### Take time on the harness docs

CLAUDE.md and AGENTS.md repay re-reading. The first pass is orientation; the second pass (in week 2-3) is internalization.

### Skip what you don't need yet

If a section seems advanced or beyond the engineer's current scope, skip it. Mark it for later.

## What this reading list will NOT do

- Will not produce a deeply-knowledgeable engineer in week 1. Depth comes through use.
- Will not work without active engagement. Passive reading produces no retention.
- Will not substitute for the pair-driving sessions. Reading + pair-driving > reading alone.

## Companion artifacts

- [`week-1-curriculum.md`](week-1-curriculum.md) — when each reading happens
- [`pair-driving-milestones.md`](pair-driving-milestones.md) — what's discussed in pair-driving
- [`team-norms-and-tribal-knowledge.md`](team-norms-and-tribal-knowledge.md) — the unwritten content
