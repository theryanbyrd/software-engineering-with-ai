# Buddy and Manager Roles

Who does what during onboarding. The curriculum requires explicit ownership; without it, responsibilities slip and the engineer falls through gaps.

## The split

The new engineer's onboarding has two named owners:

- **Buddy:** a senior engineer assigned for the duration of onboarding (typically 30 days, sometimes 60)
- **Manager:** the engineer's actual manager (engineering manager or tech lead, depending on org structure)

The buddy is operational: pair-driving, day-to-day check-ins, surfacing tribal knowledge, reviewing the engineer's work. The manager is structural: 1:1s, certification sign-off, addressing problems the buddy can't solve.

## Buddy responsibilities

### Week 1 — heavy involvement

The buddy is the engineer's primary point of contact. Specifically:

- **Day 1:** check that tools are working; available for questions; brief check-in at end of day
- **Day 2:** runs the harness walk session (2-3 hours morning; available afternoon)
- **Day 3:** reviews the engineer's agent-ready issue; provides substantive feedback
- **Day 4:** reviews the engineer's first PR substantively (60+ minutes); walks through slop signatures
- **Day 5:** ensures the engineer can run the prompt-injection exercises; coordinates with security lead

Time commitment week 1: ~20% of the buddy's week. Not optional time — committed time.

### Weeks 2-4 — moderate involvement

The buddy continues but at lower intensity:

- **Pair-driving sessions** per [`pair-driving-milestones.md`](pair-driving-milestones.md): 1-2 sessions per week
- **PR review:** the buddy is a reviewer on most of the engineer's PRs in week 2; tapers as the team takes over
- **Tribal knowledge surfacing** per [`team-norms-and-tribal-knowledge.md`](team-norms-and-tribal-knowledge.md): ongoing as situations arise
- **Day-by-day availability:** the engineer can DM with questions; the buddy responds within hours

Time commitment weeks 2-4: ~10% of the buddy's week.

### At the cert review

- Provide the buddy's assessment (per [`l1-certification-checklist.md`](l1-certification-checklist.md))
- Specific evidence supporting (or against) sign-off

### Post-day-30

- Buddy duties end at day 30 (or whenever cert sign-off happens)
- The engineer continues to interact with the buddy organically as a team member, but the formal buddy relationship concludes
- The buddy may be a reviewer on the engineer's PRs going forward, but no longer the primary

## Manager responsibilities

### Week 1 — daily check-ins

The manager has a brief check-in with the engineer each day of week 1. Even 15 minutes. Specifically:

- **Day 1 end-of-day:** "How did setup go? Any blockers?"
- **Day 2 end-of-day:** "How was the harness walk? What surprised you?"
- **Day 3 end-of-day:** "How was writing the agent-ready issue?"
- **Day 4 end-of-day:** "First PR — how did review feel?"
- **Day 5 end-of-day:** "How was the security discussion? How are you feeling overall?"

These aren't deep meetings. They're check-ins. Their purpose: catch small problems before they become big ones.

### Weeks 2-4 — mid-week 1:1

In weeks 2-4, the manager has a mid-week 1:1 with the engineer (typically 30-45 minutes). Topics:

- **What's working** — the engineer narrates their experience
- **What's not** — specific blockers, frustrations, confusions
- **What I can help with** — the manager surfaces what they can do (remove blockers, escalate issues, coordinate with adjacent teams)
- **Cert progress** — informal: are we on track for L1 sign-off?

### Cert sign-off

The manager's specific job:

- **Convene the cert review meeting** at end of week 4
- **Make the sign-off decision** — based on the buddy's assessment and the manager's own observation
- **Update the team's certification record**
- **Update tooling permissions** (or coordinate with platform team if they own the permission infrastructure)
- **Notify the team** of cert sign-off

### Intervene when buddy or engineer is struggling

The manager's most important job is catching when something's going wrong:

- **Buddy is over-committed:** if the buddy's other work is preventing them from showing up for pair-driving, the manager addresses it (reassign other work; switch buddies if needed)
- **Engineer is struggling:** if the engineer is significantly behind expected progress, the manager has a direct conversation (in 1:1, not in front of the team)
- **Buddy-engineer mismatch:** if the personality or working-style mismatch is producing friction, the manager arranges a buddy switch

These interventions aren't comfortable. They're the manager's job.

### Time commitment

Manager time: ~5% throughout the 30 days. Less time than the buddy, but more decision authority.

## Hand-off after day 30

After the cert review:

- **Buddy duties end.** The buddy returns to ~100% on their normal work.
- **Manager continues.** The 1:1 cadence continues; cert review becomes annual.
- **Engineer continues with the team.** They've shipped 13-19 PRs; they know the harness; they know the team norms; they're operating productively at L1.

The transition isn't dramatic. It's "we're done with the structured onboarding; you're a regular team member."

## Anti-patterns

### Buddy over-committed

The buddy was assigned but is in a critical project; pair-driving sessions are repeatedly canceled.

Mitigation: buddy duties are explicit time. The manager protects the buddy's time during onboarding. If the buddy genuinely can't commit, switch buddies.

### Manager absent

The manager assigned the buddy and disengaged. The engineer's 1:1s don't happen; the manager doesn't notice problems until they're severe.

Mitigation: manager 1:1s are committed time; the cert review is on the calendar from day 1. If the manager can't commit to onboarding, that's a sign to delegate (to a tech lead) or reduce hiring pace.

### Conflicting guidance from buddy and senior peers

The buddy says "we do X this way"; another senior says "actually we do X that way." The engineer is confused.

Mitigation: when conflicting guidance surfaces, the buddy and manager work together to resolve. Often the resolution surfaces a real ambiguity in the team's practice that should be documented or decided.

### Buddy is a reviewer-only, not a partner

The buddy's role becomes "review the engineer's PRs and that's it." No pair-driving, no tribal knowledge, no proactive support.

Mitigation: clarify expectations upfront. Pair-driving sessions are scheduled before they happen, not requested as needed. Tribal knowledge surfacing is ongoing.

### "Buddy by name only"

Someone is named the buddy but doesn't actually engage. The engineer has the title of having a buddy without the substance.

Mitigation: per the platform-team-charter pattern of named ownership: if the buddy isn't actually buddying, that's grounds for a direct conversation. The role isn't ceremonial.

### Manager treats onboarding as the buddy's job entirely

The manager says "the buddy will handle it" and disengages. Problems with the buddy or the engineer don't get caught.

Mitigation: the manager has specific responsibilities (check-ins, 1:1s, cert sign-off). They're not delegable.

## When to switch buddies

Rare but happens. Triggers:

### Schedule conflicts

The buddy's other commitments make pair-driving impossible. After two canceled sessions, evaluate.

### Buddy departure

The buddy leaves the company or transfers teams during the engineer's onboarding. Reassign immediately.

### Mismatch surfaced in week 1

If the buddy-engineer pairing isn't working (personality, working style, expertise mismatch), week 1 is the time to switch. By week 3 it's harder.

### Buddy over-committed beyond expectations

The buddy's role expanded into something they can't carry; the engineer is suffering. Manager addresses; possible switch.

The switch is awkward but recoverable. Better to switch than to let the engineer drift.

## Buddy selection

Who makes a good buddy:

### Good buddies have

- **Recent onboarding experience** — they remember what was hard
- **Solid harness fluency** — they can answer questions about skills, subagents, hooks
- **Time available** — they're not in critical-path work that can't be paused
- **Patience** — onboarding involves explaining things multiple times
- **Honesty** — they'll tell the engineer when something's off, not just be encouraging

### Less-good buddies

- **Senior engineers in the middle of a critical project** — they don't have time
- **Engineers who joined the team less than 6 months ago themselves** — they don't have enough tribal knowledge yet
- **Engineers who don't enjoy explaining** — onboarding requires a particular orientation
- **Engineers with conflicting priorities** — if their performance review depends on shipping, buddy duty competes

### Selection process

The manager picks the buddy with input from the senior engineer pool. The pick is communicated to the new engineer before day 1 — they should know who their buddy is.

## What this structure will NOT do

- Will not work without leadership support for buddy time. If buddy duty is unfunded, the curriculum erodes.
- Will not work in cultures where senior engineers are expected to ship constantly. Onboarding requires senior time; that time competes with shipping.
- Will not work with a poor buddy-engineer match. Switch when needed.
- Will not eliminate the inherent difficulty of joining a new team. The structure reduces avoidable friction; some friction is intrinsic.

## Companion artifacts

- [`week-1-curriculum.md`](week-1-curriculum.md) — the day-by-day buddy+manager involvement
- [`days-8-to-30.md`](days-8-to-30.md) — the broader curriculum
- [`pair-driving-milestones.md`](pair-driving-milestones.md) — pair-driving specifics
- [`team-norms-and-tribal-knowledge.md`](team-norms-and-tribal-knowledge.md) — what the buddy surfaces
- [`l1-certification-checklist.md`](l1-certification-checklist.md) — cert sign-off
- Ch 44 §44.1 — source
