# Migration Playbooks

Senior-engineer-friendly migration playbooks for the most common AI tooling consolidation scenarios. Direct implementation of Chapter 53 of [_Software Engineering with AI: A Practical Handbook for the Claude Code Era_](https://www.linkedin.com/in/ryanbyrd) by Ryan Byrd.

The mechanical translator (`scripts/cursorrules-to-claude-md.py`) handles the file-format conversion. These playbooks are for the harder problem: the team conversation, the timeline, the consolidation decision, the retention risk.

## What's in here

| Playbook | When to use |
|---|---|
| [`cursor-to-claude-code.md`](cursor-to-claude-code.md) | Team has 6+ months of `.cursorrules` investment and is exploring Claude Code |
| [`copilot-to-mixed-stack.md`](copilot-to-mixed-stack.md) | Team has Copilot and is adding agentic tooling alongside it |
| [`shadow-ai-to-approved-stack.md`](shadow-ai-to-approved-stack.md) | Engineers are using personal-account ChatGPT/Claude.ai on company code; bring it into governance |
| [`pre-migration-checklist.md`](pre-migration-checklist.md) | Run before ANY migration. The pre-flight that prevents the failures the war stories document |
| [`team-conversation-scripts.md`](team-conversation-scripts.md) | Verbatim openers for the all-hands, the senior 1:1, the holdout conversation |

## The book's editorial stance — the only stance that works

> Rip-and-replace migrations to a new AI tooling stack mid-stride almost always fail. The team's productivity drops; the engineers who liked the old tool become the loudest critics of the new one; the platform team spends three months on tooling instead of harness investment. By the time the migration is done, the metrics look worse than before, the CEO concludes "AI doesn't work for us," and the program collapses.
>
> The pattern that works: run in parallel for one to two quarters, let the team self-select, converge over six to nine months. The investment in the existing tool is not wasted; the patterns and rules that worked carry over.
>
> — Ch 53 §53.1

Every playbook here applies this principle. If your situation requires rip-and-replace (e.g., the existing vendor lost their security certification and contract is terminated), the playbooks won't fit cleanly — that's a different scenario.

## Read this first

The migration playbooks address the **process and people** side of migration. They assume:

1. You've already decided that migration is the right call (or that running parallel is). The decision-making rubric for that is in the executive-strategic-kit, not here.
2. You have at least one senior engineer who wants the migration. A migration without a senior champion fails regardless of the playbook.
3. You have budget for parallel use. Most playbooks assume one to two quarters of dual licensing. If you can't afford this, see [`pre-migration-checklist.md`](pre-migration-checklist.md) for the Day 0 conversation.
4. You're not in the middle of an active incident, a layoff, or a reorg. Those compound badly with tool migrations.

## What these playbooks WILL do

- Give you a realistic timeline (months, not weeks).
- Tell you what conversations to have, in what order, with what specific framing.
- Identify which engineers are at retention risk during the migration and how to address.
- Give you the "what if it goes wrong" branches.

## What these playbooks will NOT do

- Tell you which tool to pick. That's a separate decision; this is for the migration once decided.
- Replace your security review of the new tool. Procurement comes before migration; see Ch 38.
- Eliminate political risk. Migrations that touch senior engineers' tools are political; the playbook minimizes risk but cannot eliminate it.
- Make a bad decision succeed. If the consolidation is the wrong call, the best-executed migration still ends in dual-tool spend in 18 months when you reverse course.

## How to use

1. **Read [`pre-migration-checklist.md`](pre-migration-checklist.md) first.** If you can't get a "yes" on at least 70% of the items, postpone the migration.
2. **Pick the relevant playbook** based on your starting tool stack.
3. **Read it end-to-end before starting.** The playbook is not a runbook — there's no machine-executable surface — it's a structured decision support guide.
4. **Customize timing to your team.** A 70-engineer team's parallel-use period might be 4 months; a 200-engineer team's might be 9 months.
5. **Track progress against the playbook's milestones.** When you're falling behind, the playbook tells you what's at risk.

## When to step outside the playbook

- **The CEO mandates a faster timeline.** Use [`team-conversation-scripts.md`](team-conversation-scripts.md) for the conversation that pushes back; reference Ch 56 §56.x.
- **A senior engineer threatens to leave over the migration.** Don't proceed until the retention conversation has happened. See `people/career-ladder/` for the framing.
- **The new tool has a regression that breaks the migration.** Pause. Don't push through; vendor regressions cost more than delays.
- **Budget is cut mid-migration.** Use the [war story 005](../war-stories/005-the-cfo-token-cap.md) as your reference for the conversation. Surprise budget caps mid-migration are catastrophic; renegotiate the process, not the budget.

## Companion artifacts

These playbooks reference and pair with:

- `scripts/cursorrules-to-claude-md.py` — the mechanical translator for `.cursorrules` → CLAUDE.md
- `executive-strategic-kit/ceo-emails/` — leadership communication templates
- `war-stories/004-the-cursor-migration-mandate.md` — what happens when you skip the playbook
- `people/jds/senior-engineer-ai-native.md` — the JD that anchors what "good" looks like post-migration
- `prompt-injection-test-suite/` — verify the new tool's harness is at least as secure as the old one before relying on it

## Calibration tip

The playbooks here are calibrated to the most common failure modes. If your migration looks dramatically different (e.g., consolidating from 4 tools to 1, or migrating because of a vendor exit rather than a strategic choice), use these as starting templates and adapt rather than follow verbatim.

— Ryan Byrd
