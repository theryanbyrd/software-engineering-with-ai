# L1 Certification Checklist

The explicit checklist for L1 cert sign-off at end of 30 days. Per Ch 44 §44.2:

> L1 (per-edit approval). Onboarding week complete. Demonstrated agent-ready issue. One reviewed PR.

This file expands those criteria into a checklist the buddy and manager use at the cert review meeting.

## When the cert review happens

End of week 4 — typically Thursday or Friday of the engineer's fourth week. The review takes 30-45 minutes; sign-off happens that day if the criteria are met.

If the review is delayed (manager out, buddy unavailable), reschedule within a week. Don't let the cert meeting drift; the engineer is in limbo until it happens.

## Who attends

- Engineer
- Buddy
- Manager (engineer's manager)

Optional:
- Platform team representative (if the team has a strong platform team and there are infrastructure questions)
- Senior peer (if a second sign-off is required by the team's process)

## The checklist

### Onboarding week complete (Ch 44 §44.2 criterion 1)

- [ ] **Day 1 reading complete.** Engineer can articulate what's in the team's CLAUDE.md, AGENTS.md, autonomy ladder, do-not-automate catalog, approved tooling matrix.
- [ ] **Day 2 harness walk complete.** Engineer has invoked at least one skill end-to-end, observed a subagent run, and seen at least one hook fire.
- [ ] **Day 3 agent-ready issue complete.** Engineer has written at least one agent-ready issue that the buddy considered shippable as a spec.
- [ ] **Day 4 PR complete.** Engineer has opened (and ideally merged) a Tier-3 PR with senior review.
- [ ] **Day 5 prompt-injection exercises complete.** Engineer has run all six exercises (per `prompt-injection-test-suite/`) and discussed with the team's security lead.

If any of these are incomplete, sign-off is blocked until they're addressed. The "onboarding week" doesn't have to be exactly the first 5 days; it can extend into week 2 if circumstances delayed it (a federal holiday, an unexpected pause). What matters is that the content is covered.

### Demonstrated agent-ready issue (Ch 44 §44.2 criterion 2)

- [ ] **At least one agent-ready issue written by the engineer** that the buddy considers shippable.
- [ ] **At least one agent-ready issue used in production** — the engineer's spec was good enough that someone (the engineer themselves or another team member) used it as the basis for AI tooling work.

The bar isn't "wrote a perfect issue once." The bar is "can produce specs that AI tooling can act on without ambiguity."

### Reviewed PRs (Ch 44 §44.2 criterion 3)

The book says "one reviewed PR" as the L1 criterion. In practice, the engineer should have shipped 5-15 PRs by day 30 (per [`days-8-to-30.md`](days-8-to-30.md)).

- [ ] **At least 5 PRs landed** at L1 by day 30.
- [ ] **All PRs received substantive review** — not rubber-stamped.
- [ ] **No slop incidents** — no PR that landed and produced a real bug attributable to AI-introduced sloppiness.

If the engineer has fewer than 5 PRs, investigate:
- Was the engineer blocked? (platform issues, scope issues)
- Was the work pipeline thin? (not the engineer's fault if there wasn't work to do)
- Was the engineer struggling? (concerning; address)

Fewer PRs isn't disqualifying if there's a clear reason; it's a flag to investigate.

### Demonstrated review discipline

- [ ] **Engineer can identify the seven slop signatures** (per Ch 22 §22.2) in code review — either when they appear in their own code or others'.
- [ ] **Engineer has reviewed at least 1-2 other engineers' PRs** by day 30.
- [ ] **Engineer's reviews surface substantive issues** — not just nits.

This isn't a formal check; it's the buddy's judgment based on observing the engineer's review practice during weeks 2-4.

### Skill library use

- [ ] **Engineer has used at least 3 of the team's skills** in real work.
- [ ] **Engineer can describe when each skill is appropriate** vs. when to skip it.

If the team has fewer than 3 actively-used skills, the criterion adjusts — use however many the team has. The point is fluency with the team's actual harness, not hitting a number.

### Tools and access

- [ ] **All tools working reliably** — the engineer hasn't been blocked by setup issues for more than a day in the past 4 weeks.
- [ ] **Permissions appropriately scoped** — not over-broad, not blocking the engineer's work.

### Cultural integration

These are softer signals; the buddy and manager assess:

- [ ] **Engineer participates in team rituals** — standups, retros, planning, etc.
- [ ] **Engineer asks questions appropriately** — surfaces blockers; doesn't pretend to understand things they don't.
- [ ] **Engineer is starting to be productive at the team's pace** — keeping up with the work cadence.

If cultural integration concerns exist, they're often more important than technical concerns. Address explicitly.

## The cert review meeting structure

### Pre-meeting prep (engineer + buddy)

- Engineer prepares a brief summary: what they shipped, what they learned, what they want to deepen
- Buddy prepares: their assessment of the engineer's progress; specific evidence supporting (or against) sign-off

### Meeting agenda (30-45 min)

1. **Engineer summary** (5-10 min) — what the engineer covers. Not a defensive presentation; an honest summary.

2. **Buddy assessment** (5-10 min) — buddy's perspective. Specific evidence: PRs reviewed, sessions held, what good looks like.

3. **Manager questions** (10 min) — manager has questions for both. Specifically:
   - "What was hardest in the past 30 days?"
   - "What's still confusing?"
   - "Where do you want to focus in the next 60 days?"

4. **Sign-off discussion** (5-10 min) — the actual cert decision. Three possible outcomes:
   - **Sign off** — cert granted, tooling permissions updated, team notified
   - **Sign off with caveats** — cert granted but specific gaps to address in next 30 days
   - **Defer** — cert not yet earned; specific path to re-evaluate (typically 2-4 weeks out)

5. **L2 path discussion** (5 min) — if signed off, brief conversation about what L2 looks like.

### Post-meeting (manager)

If signed off:
- Update the team's certification record
- Update the engineer's tooling permissions to reflect L1 access
- Notify the team (typically a brief Slack message: "X is now L1 certified")
- Schedule the next milestone (informal L2 readiness check at ~60-90 days)

If deferred:
- Document the specific gaps and re-evaluation date
- Communicate to the engineer in a 1:1 (don't let it linger)
- Adjust pair-driving / buddy time as needed

## What to do if criteria aren't met

### "Five days short"

Common. The engineer is close; specific items aren't done. Extend by 1-2 weeks; address the specific gaps; sign off.

Don't make this dramatic. "Let's give it another week to close out [specific things]" is normal.

### "Significantly short"

Less common but happens. The engineer is genuinely behind on the curriculum's expectations.

The conversation:
- Specific named gaps
- Specific path forward
- Specific re-evaluation date (typically 4-6 weeks out)
- Adjustment of buddy / manager support if needed

### "The engineer isn't ready and won't be"

Rare in mid-career hires; happens occasionally. The hard conversation:
- What's the specific gap?
- Is it addressable with more time?
- If not: this may not be the right fit for the role / team

This isn't usually a curriculum failure — it's a hiring or role-fit issue surfacing through the curriculum. The curriculum's job is to surface it; the manager's job is to address it.

## Re-certification cadence

Per Ch 44 §44.2:

> Certifications expire. Review yearly.

After initial cert at day 30:
- **Annual review** of the cert (does the engineer's actual practice still match L1 discipline?)
- **Per-incident review** if the engineer is involved in an AI-tooling-related incident (per `agent-autonomy-levels/certification-gates.md`)

Re-certification is typically a quick check, not a re-run of the full process — unless something has materially changed.

## What this checklist will NOT do

- Will not produce a passing engineer by itself. The criteria require the engineer's actual practice; the checklist verifies it.
- Will not catch every readiness signal. Buddy and manager judgment matter; the checklist supports their judgment, doesn't replace it.
- Will not work without honest assessment. If the buddy or manager fudges criteria to sign off an unready engineer, the cert becomes meaningless.
- Will not eliminate the awkwardness of a "not ready" conversation. The conversation is hard; the checklist makes it specific.

## Companion artifacts

- [`week-1-curriculum.md`](week-1-curriculum.md) — what onboarding-week-complete means
- [`days-8-to-30.md`](days-8-to-30.md) — what 5-15 PRs means in practice
- [`pair-driving-milestones.md`](pair-driving-milestones.md) — what pair-driving covers
- [`buddy-and-manager-roles.md`](buddy-and-manager-roles.md) — who does what at the cert meeting
- `agent-autonomy-levels/certification-gates.md` — the broader cert framework
- Ch 44 §44.2 — source
