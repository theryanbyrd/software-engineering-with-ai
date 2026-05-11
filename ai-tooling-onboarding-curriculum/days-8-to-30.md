# Days 8 to 30 — Real Work, Deepening Fluency, L1 Cert

The three weeks after week 1. The structure is less day-by-day and more milestone-driven; the engineer is doing real work, but with explicit checkpoints.

## The shape of weeks 2-4

| Week | Focus | Primary work | Pair-driving |
|---|---|---|---|
| **Week 2** | Stabilize at L1 | 3-5 small PRs at L1 | 2 pair-driving sessions (~2 hours each) |
| **Week 3** | Deepen fluency | 5-7 PRs at L1; first time as reviewer (other engineers' work) | 1 pair-driving session |
| **Week 4** | L1 cert sign-off | 5-7 PRs; cert review at end of week | 1 pair-driving session + cert review |

Total expectation by day 30: 13-19 PRs shipped at L1, with growing breadth and modest growth in size.

---

## Week 2 — Stabilize at L1

### Goal

The engineer is operating productively at L1: the agent suggests, the engineer reviews and approves each edit. PRs are landing; review discipline is internalized.

### Specific work

#### PRs

The engineer ships 3-5 small PRs at L1. Characteristics:
- Tier-3 work (per `do-not-automate-catalog/tier-3-light-human-gate.md`)
- Small in scope (under ~200 lines typically)
- Each PR goes through buddy or team review
- The engineer is using AI tooling at L1 (per-edit approval)

#### Pair-driving (2 sessions)

1. **Session 1 (Monday or Tuesday)** — Reviewing other engineers' PRs
   - Engineer joins a senior engineer for code review of an open PR (not their own)
   - Buddy walks through what they're looking for; engineer asks questions
   - Calibrates the engineer's review intuition

2. **Session 2 (Thursday or Friday)** — Tackling a slightly larger task
   - Engineer pairs with buddy on a Tier-3 task that's larger than week-1 work
   - Pair-driving in the sense that both are working on the same task; the buddy demonstrates patterns the engineer hasn't yet seen

#### Manager 1:1

- Mid-week 1:1 with the manager
- Discuss what's working, what's confusing
- Specific: any blockers in the harness or workflow

### What the engineer should be learning

- The team's cadence of work (when do PRs typically merge; how long between review and merge)
- The team's review style (terse vs. detailed; specific patterns to look for)
- The team's specific anti-patterns (what reviewers reliably catch)
- The team's CLAUDE.md / AGENTS.md content in practice (not just on paper)

### Pass criterion for week 2

- 3-5 PRs landed
- Engineer can describe at least 2 patterns the team specifically watches for
- Engineer's verify-passing rate is high (PRs don't fail verify in CI)

### Common issues in week 2

#### "Engineer's PRs all need significant rework"

Indicates the engineer is over-trusting AI output without applying review discipline. The buddy's review surfaces this.

Mitigation: extra pair-driving sessions; explicit walkthroughs of slop signatures (Ch 22 §22.2); the engineer's review of every line before approving.

#### "Engineer's PRs are very small"

Sometimes appropriate (small tickets); sometimes indicates the engineer is staying in a comfort zone.

Mitigation: by week 3, expect modest scaling — slightly larger tickets, slightly more complex work.

---

## Week 3 — Deepen fluency

### Goal

The engineer is operating fluently at L1 with growing breadth. They're starting to be useful to the team beyond just shipping their own work.

### Specific work

#### PRs

5-7 PRs at L1. Characteristics:
- Mix of bug fixes, small features, refactors
- Some Tier-3 work; possibly first Tier-2 work with explicit reviewer support
- Larger PRs (up to ~400 lines for the largest)

#### First time as a reviewer

By week 3, the engineer should review at least 1-2 other engineers' PRs:
- Initially as a third reviewer (not the primary)
- Reviews are educational: the engineer's reading the diff and noting questions
- Eventually the engineer's review is substantive — catching real issues

#### Pair-driving (1 session)

- One session focused on a specific topic the engineer needs to deepen
- Could be: subagent design, a specific skill the team uses heavily, the team's testing patterns

#### Manager 1:1

- Mid-week 1:1
- Specific question: "What blockers are you hitting that I can help with?"
- Specific question: "What's clicking? What's not?"

### What the engineer should be learning

- The team's specific systems (the major services they own; what's where)
- The team's release cadence (when do we deploy; what's the release process)
- The team's incident response (what's on-call like; what was the most recent incident)
- The team's planning rhythm (how do we sprint plan; what's the OKR cadence)

### Pass criterion for week 3

- 5-7 PRs landed
- Engineer has reviewed at least 1-2 PRs as a reviewer
- Engineer's review found at least one substantive issue (not a nit)
- Engineer can describe the team's release process

---

## Week 4 — L1 cert sign-off

### Goal

The engineer earns L1 certification (per `agent-autonomy-levels/certification-gates.md`). The cert is the formal recognition that the engineer can operate productively at L1 without active senior shepherding.

### Specific work

#### PRs

5-7 more PRs at L1. By end of week 4, the engineer's cumulative count should be 13-19 PRs at L1.

#### Cert review (end of week)

The cert review is per [`l1-certification-checklist.md`](l1-certification-checklist.md). The buddy and the manager review:
- Has the engineer met the L1 criteria?
- Are there any specific gaps to address before sign-off?
- If signed off: tooling permissions updated; team notified

#### Pair-driving (1 session)

- Optional, depending on the engineer's needs
- Often: a deeper-than-routine discussion of what comes next (path to L2)

#### Manager 1:1

- Mid-week 1:1
- Cert path discussion: when does L2 start being on the table?
- 30-day retrospective: what worked; what didn't; what to change

### What the engineer should be learning

- The team's promotion criteria (per `promotion-and-leveling-rubric/level-rubric.md`)
- The team's longer-term roadmap
- Specific senior engineers in the org (beyond the immediate team)

### Pass criterion for week 4 (and the 30-day mark)

- L1 cert earned
- 13-19 PRs total at L1
- Engineer is reviewing other engineers' PRs substantively
- Engineer has met the team's seniors via pair-driving sessions
- Engineer can articulate where L2 starts and what would close the gap

---

## What happens at day 30 if the engineer hasn't earned L1

Per `agent-autonomy-levels/raising-and-lowering-autonomy.md`'s discipline applied to certification: the cert isn't earned by tenure; it's earned by demonstrated practice.

If the engineer is short of the criteria:

### "5 days short"

Common. Extend by 1-2 weeks; address the specific gap; sign off.

### "Significantly short"

Less common but happens. The conversation:
- Specific named gaps
- Specific path forward
- Specific re-evaluation date (typically 4-6 weeks out)

### "The engineer isn't ready and won't be"

Rare in mid-career hires; happens occasionally. The hard conversation:
- What's the specific gap?
- Is it addressable?
- If not: this may not be the right fit

This isn't a failure of the curriculum; it's a hiring/role-fit issue surfacing through the curriculum.

---

## What the engineer should be doing AFTER day 30

### Working at L1, with eye toward L2

- Continue shipping at L1
- Track toward the L2 cert criteria (per `agent-autonomy-levels/certification-gates.md`):
  - 30+ AI-assisted PRs at L1 without slop incident (cumulative)
  - Demonstrated skill library use
  - Passed prompt-injection exercises (already done in week 1)

### Contributing back

- The engineer's first month included reading the harness; the next 60-90 days, they should have ideas for harness improvements
- Specifically: things that confused them in week 1 that should be clearer in CLAUDE.md / AGENTS.md
- Or: a skill the team is missing that they're noticing the absence of

### Mentoring the next new hire

- After 90 days, the engineer is ready to be a buddy for the next new hire
- This is the team's onboarding capacity scaling

## Companion artifacts

- [`week-1-curriculum.md`](week-1-curriculum.md) — the first week
- [`l1-certification-checklist.md`](l1-certification-checklist.md) — the day-30 gate
- [`pair-driving-milestones.md`](pair-driving-milestones.md) — pair-driving structure
- [`buddy-and-manager-roles.md`](buddy-and-manager-roles.md) — who does what
- `agent-autonomy-levels/certification-gates.md` — the cert framework
- `promotion-and-leveling-rubric/` — the broader leveling
- Ch 44 §44.1 — source
