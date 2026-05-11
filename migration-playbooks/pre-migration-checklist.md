# Pre-Migration Checklist

Run this before ANY tool migration. If you can't get a "yes" on at least 70% of these items, postpone or restructure the migration.

The checklist exists because every war story in [Appendix L of the book](../war-stories/) traces back to a Day 0 conversation that didn't happen. Treat this as the operational equivalent of pre-flight on an aircraft: tedious, occasionally annoying, never optional.

## Section 1 — Strategic clarity (5 items)

- [ ] **The migration has a named executive sponsor.** Not just "the VP of Engineering supports it" — there's a named person whose quarterly OKRs include the migration succeeding.
- [ ] **The "why" is documented and shared with the team in writing.** Not "we should be on the latest tools." Specifically: *"We're consolidating because [X savings / Y capability / Z risk reduction]"*.
- [ ] **The timeline is realistic.** One to two quarters of parallel use, six to nine months total. If your timeline is shorter, see story 004 in war-stories. If you've been told to compress, read [`team-conversation-scripts.md`](team-conversation-scripts.md) §1.
- [ ] **The success criteria are written down.** "Migration is complete when X% of senior engineers have voluntarily moved AND productivity metric Y has not degraded by more than Z."
- [ ] **The reversal criteria are written down.** "If by month N we have not achieved X, we will pause / reverse / pivot." Without explicit reversal criteria, sunk-cost reasoning takes over at month 4.

## Section 2 — People readiness (6 items)

- [ ] **At least one senior IC has volunteered as the migration champion.** Not assigned. Volunteered. The migration without an internal champion fails.
- [ ] **The senior engineers who built the existing tool's investment have been heard.** They've explained what works for them, what they fear losing, and what they need from the new tool. The migration plan addresses these explicitly.
- [ ] **The retention-risk list is current.** Which 3-5 engineers are most likely to leave during the migration? What's the retention play for each? See `people/career-ladder/` for the framing.
- [ ] **The platform team has bandwidth for the migration.** They are not simultaneously running an incident, completing a major harness rebuild, or onboarding new hires.
- [ ] **The team's morale is not in crisis.** A team that's just absorbed a layoff, a reorg, or a major incident should not also absorb a tool migration. If three of these are happening simultaneously, sequence them.
- [ ] **The hiring manager and HR are aligned.** Active hires in the affected teams are briefed on the migration. New hires won't be onboarded onto a tool the team is leaving.

## Section 3 — Financial readiness (4 items)

- [ ] **There is budget for one to two quarters of parallel licensing.** Both old and new tool licensed for the team during overlap. If you can't afford this, you can't afford the migration; see story 005.
- [ ] **The cost dashboard exists and is up to date.** Per-team token spend, per-engineer license costs, dashboard accessible to the migration sponsor. See `exec-kit/`.
- [ ] **The CFO is briefed and in the loop on the dual-tool spend during overlap.** No surprises mid-quarter. Use the [war story 005](../war-stories/005-the-cfo-token-cap.md) as the reference for what happens otherwise.
- [ ] **The cancellation date for the old tool is on the calendar with a 60-day buffer beyond the planned consolidation.** Buffer absorbs slippage.

## Section 4 — Technical readiness (5 items)

- [ ] **The new tool has been security-reviewed.** Procurement complete; data-classification implications understood. See Ch 38 in the book.
- [ ] **The new tool's harness components have been built or are in flight.** CLAUDE.md / AGENTS.md, hooks, skills — the equivalents of what existed in the old tool. Don't expect engineers to ramp on a tool with no harness.
- [ ] **The mechanical translation is done or in flight.** `scripts/cursorrules-to-claude-md.py` (or your team's equivalent) has been run on existing config and the output reviewed by a senior engineer.
- [ ] **The verify command works on both tools.** Engineers can run identical verification regardless of which tool they used to make the change.
- [ ] **A rollback exists for any harness changes.** If a hook or skill turns out to be wrong, you can revert without rolling back the entire migration.

## Section 5 — Communication readiness (3 items)

- [ ] **The first all-hands message is drafted.** What you'll say, who's saying it, when. See [`team-conversation-scripts.md`](team-conversation-scripts.md) §2.
- [ ] **The senior 1:1 cadence is set.** Migration champion meets with each senior engineer in week 1 to hear their concerns. Not a group meeting; individual.
- [ ] **The retro cadence includes migration as a standing item.** Weekly or biweekly retro adds "migration health" as a tracked topic until consolidation is complete.

## Section 6 — Risk acceptance (3 items)

- [ ] **The migration sponsor has acknowledged in writing that the team's productivity may dip 10-20% during overlap.** This is normal. The exec who hasn't acknowledged it will be the exec who panics in week 8.
- [ ] **The plan for "what if a senior engineer leaves" exists.** Specifically: which work would slip, who absorbs it, do we backfill or reabsorb the headcount.
- [ ] **The plan for "what if the new tool releases a regression mid-migration" exists.** Pause criteria, rollback criteria, vendor escalation contact.

---

## Scoring

- **20+ yes:** Proceed. You're as ready as a migration of this kind ever is.
- **15-19 yes:** Proceed with caution. Address the no's that are addressable in the next 2-4 weeks.
- **10-14 yes:** Postpone 4-8 weeks. Use the time to address the gaps.
- **<10 yes:** Do not start. The conditions for success aren't in place; the migration will fail. Use this as the documentation for the conversation with leadership about why.

## What to do with this checklist

Save the completed checklist. When the migration succeeds, the checklist is the artifact that explains why. When the migration struggles, the checklist surfaces which preconditions weren't actually met.

If the checklist score and the eventual outcome diverge wildly (e.g., 22/26 yes but the migration failed), update the checklist for the next migration. The discipline compounds.

## When the executive insists on starting anyway

Sometimes leadership decides to start despite a low checklist score. Push back in writing. Use [`team-conversation-scripts.md`](team-conversation-scripts.md) §1 for the framing. If the decision is made over your objection, document it. You did not prevent the failure; you owned the response when it came.

## Companion artifacts

- [`team-conversation-scripts.md`](team-conversation-scripts.md) — verbatim openers for the conversations referenced above
- `exec-kit/90-day-plan.md` — the broader rollout plan this checklist sits inside
- `war-stories/004-the-cursor-migration-mandate.md` — what happens when this checklist is skipped
- `war-stories/005-the-cfo-token-cap.md` — the budget conversation gone wrong
