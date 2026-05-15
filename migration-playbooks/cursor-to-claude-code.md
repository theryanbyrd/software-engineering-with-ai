# Cursor → Claude Code Migration Playbook

The most common migration scenario in 2026: a team has 6-18 months of Cursor investment (`.cursorrules` files, Composer workflows, tab-completion habits) and is exploring Claude Code for agentic work.

**The book's editorial position:** this is not a migration. It's a stack expansion that may converge on Claude Code over 6-9 months, or may settle on a both-tools steady state. Either outcome is fine. The failure mode is forcing convergence too fast.

This playbook covers the parallel-then-converge approach for a 50-200 engineer organization. Adapt timelines for smaller (faster) or larger (slower) teams.

## Who this playbook is for

- VP of Engineering or Engineering Director making the call
- Platform team lead executing the migration
- Senior IC migration champion
- Hiring manager whose team is affected

## Read first

- [`pre-migration-checklist.md`](pre-migration-checklist.md) — gates whether you should start
- [`team-conversation-scripts.md`](team-conversation-scripts.md) §3 — the Cursor migration conversation specifically
- `war-stories/004-the-cursor-migration-mandate.md` — the failure mode this playbook prevents
- Ch 53 §53.2 of the handbook — the editorial framing

## Phase 0 — Preconditions (Week -4 to 0)

Before announcing anything to the team:

1. **Run the pre-migration checklist.** Don't start without 15+ yes answers.
2. **Run the mechanical translation in dry-run mode.** Take 3-5 representative `.cursorrules` files and run `scripts/cursorrules-to-claude-md.py` on them. Review the output with a senior engineer who knows that codebase. The output should be 70%+ usable; if it's lower, the codebase has unusual conventions and you need a custom translation pass.
3. **Identify the migration champion.** A senior IC who has VOLUNTEERED, not been assigned. The champion should be someone who has already been using both tools.
4. **Inventory the existing investment.** How many `.cursorrules` files? How many lines? Which engineers wrote which? Which patterns are most heavily relied on (Composer flows, specific tab-completion habits)?
5. **Brief the CFO.** Dual licensing for two quarters. Specific dollar amount. Acknowledged in writing.
6. **Brief the senior bench (3-5 most senior engineers) individually.** This is the highest-risk step; if a senior engineer is going to push back, you want it before the all-hands.

If any of these steps surfaces a major concern — the senior bench is hostile, the mechanical translation is below 50%, the CFO objects to dual licensing — pause and address before continuing.

## Phase 1 — Parallel introduction (Months 1-2)

### Week 1 — Announcement

**The all-hands message.** See [`team-conversation-scripts.md`](team-conversation-scripts.md) §3 for the verbatim opener. Key elements:

- Frame as additive, not replacement: *"We are adding Claude Code to the stack for agentic workflows; Cursor remains for IDE work."*
- No deadline announced. *"In two quarters we'll review what's working and decide together."*
- Acknowledge the existing investment: *"The patterns we've built in Cursor are not wasted. They translate to the new tool with minor edits."*
- Name the champion. Not the VP, not the platform lead. The senior IC.

### Week 2 — Mechanical translation

The platform team runs `scripts/cursorrules-to-claude-md.py` against the codebase's `.cursorrules` files. The output goes to a branch:

```bash
git checkout -b claude-code/initial-setup
python3 scripts/cursorrules-to-claude-md.py --also-write-agents-md
git add CLAUDE.md AGENTS.md
git commit -m "Initial Claude Code setup from existing .cursorrules"
```

The migration champion reviews. Senior engineers from each team review the part that affects them. PR is merged.

### Weeks 3-4 — Champion onboarding

The migration champion uses Claude Code for one to two weeks on real work (not toy projects). They:

- Identify what works well, what's awkward, what regressed compared to Cursor
- Document their findings in a shared doc
- Iterate on CLAUDE.md / AGENTS.md based on what they learned
- Write up a "first month with Claude Code" note for the team

This is the single most important step. The champion is calibrating the rest of the team's expectations. Their experience becomes the team's expectations.

### Weeks 5-8 — Voluntary adoption

Other senior engineers who want to try Claude Code start. **No pressure on anyone.** The platform team supports questions; the champion answers most of them.

Track:
- How many engineers have tried Claude Code (target: 30-50% of seniors by week 8)
- Which engineers have moved primary work to Claude Code (target: 5-10% by week 8)
- Which `.cursorrules` patterns translated well, which didn't

## Phase 2 — Mid-quarter check-in (Month 3)

### Week 9 — Retro

Migration retro with the affected teams:
- What's working in Claude Code?
- What's missing?
- What will keep you on Cursor for inner-loop work?
- What harness investment would unblock more migration?

Document. Adjust CLAUDE.md / AGENTS.md / hooks based on findings.

### Weeks 10-12 — Harness investment

Based on the retro, the platform team builds the missing harness components: skills the team needs, hooks for protected paths, subagents for repeated workflows. This is the work that makes the second quarter of parallel use productive.

## Phase 3 — Steady state assessment (Months 4-6)

### Month 4 — Usage assessment

Honest data on usage patterns:

- What % of the team uses Claude Code for outer-loop / agentic work? (Target: 60%+ for senior engineers; 40%+ overall)
- What % of the team uses Cursor for inner-loop / IDE work? (Likely still 60%+; this is normal)
- Are there tasks that nobody is doing well in either tool? (Surface these for the platform team)
- What's the productivity delta vs. pre-migration baseline? (Should be flat or up; significantly down means investigate)

### Months 5-6 — The convergence decision

By month 6, you have data. The decision tree:

**Path A — Most senior engineers prefer Claude Code for everything (40-50% of cases):**
The convergence decision is easy. Cursor stays available for inner-loop work for 3 more months as a transition; cancel after consolidation.

**Path B — Engineers split: Cursor for inner-loop, Claude Code for outer-loop (40-50% of cases):**
This is the most common steady state. Keep both. Optimize licensing: Cursor for everyone (cheaper), Claude Code Max for senior tier and platform team. Plan to revisit annually.

**Path C — Engineers prefer Cursor and don't want Claude Code (5-10% of cases):**
The migration didn't take. Don't force it. Reverse course gracefully — keep Cursor as primary, retain Claude Code seats only for the platform team and the engineers who want it. Document why for next time.

**Path D — Engineers split with significant minority preferring neither (5% of cases):**
Investigate. Often signals a deeper problem (harness inadequate, team's work doesn't suit the tooling category, hostile rollout). Pause migration, address root cause, decide later.

## Phase 4 — Consolidation (Months 7-9)

Only if Path A. If Path B/C/D, the playbook ends here and you settle into the appropriate steady state.

For Path A:

### Month 7 — Communicate the consolidation timeline

*"We'll be sunsetting Cursor licenses on [date in month 9]. Engineers who need an extension should talk to [migration champion]."*

Provide extensions liberally. The 3-5 engineers who need extra time during this phase are the engineers who feel pressured by the timeline; pressure produces the resignations the playbook is trying to avoid.

### Month 8 — Cancel new Cursor seats; allow renewal grace

New hires don't get Cursor seats by default. Existing seats renew on their normal cycle.

### Month 9 — Final consolidation

Cancel remaining Cursor seats. Total elapsed time: 9 months from announcement.

## Variants

### Smaller team (10-30 engineers)

Compress timelines: Phase 1 in 1 month, Phase 2 by month 2, decision by month 4, consolidation by month 6 if Path A.

### Larger team (200+)

Stretch timelines: Phase 1 in 3 months (one team at a time), Phase 2 by month 5, decision by month 8, consolidation 12-18 months from announcement.

### High senior turnover risk

If 2+ senior engineers have signaled they would consider leaving over a tool migration, do not consolidate. Stay on Path B (parallel) indefinitely. The cost of dual licensing is much less than the cost of senior departures.

## What to do if it goes wrong

### Productivity drops 15%+ in Phase 1

- Pause adoption push for 2 weeks
- Run the retro early
- Identify the missing harness components and build them before resuming
- Communicate transparently to the team and to leadership

### A senior engineer announces they'll leave over the migration

- Hold the conversation immediately, in person if possible
- Listen first, then respond. Often the resignation threat is signaling deeper concerns
- Be willing to delay the migration timeline for this engineer specifically — extensions on Cursor access, role flexibility, etc.
- Use the senior IC retention play from `people/career-ladder/` — comp parity, public credit, internal mobility

### The CFO panics about dual licensing in month 4

- Bring the data: per-team adoption, productivity baseline, comparison to story 005
- Renegotiate the process, not the budget. If overlap needs to extend by 2 months, get explicit acknowledgment with a re-baselined target

### A new model release changes the calculus mid-migration

- Don't pivot. Announce that the assessment in month 4 will incorporate the new model
- A migration that pivots every time a new model drops fails because nothing converges

## What this playbook will NOT do

- Will not make a top-down mandate succeed. If the migration is forced, the playbook prevents some failures but cannot prevent the senior departures or the productivity dip.
- Will not work if the team is simultaneously dealing with a major incident, layoff, or reorg. Sequence carefully.
- Will not generate ROI in year one. Tool migrations are infrastructure investment; the payoff is in year two when the consolidated stack is faster than dual.

## Companion artifacts

- `scripts/cursorrules-to-claude-md.py` — mechanical translator
- [`team-conversation-scripts.md`](team-conversation-scripts.md) — verbatim conversation openers
- `war-stories/004-the-cursor-migration-mandate.md` — what happens without this playbook
- `executive-strategic-kit/ceo-emails/` — leadership communication during migration
- `benchmarks/` — verify the new tool's quality on your work before consolidating
