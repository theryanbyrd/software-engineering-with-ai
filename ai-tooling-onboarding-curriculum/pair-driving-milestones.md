# Pair-Driving Milestones

The structured pair-driving sessions across the 30 days. Pair-driving is the highest-leverage part of onboarding — the new engineer working alongside a senior engineer on real (or near-real) work.

This file is the L4-equivalent companion to `junior-trajectory/pair-driving-guide.md` (which is for early-career engineers building general engineering judgment). The patterns are similar; the goals differ — junior pair-driving builds engineering fundamentals; AI-tooling pair-driving builds harness fluency.

## The schedule across 30 days

| Week | Sessions | Total time | Focus |
|---|---|---|---|
| **Week 1** | 1-2 sessions | 2-4 hours | Tour the harness; first sandbox skill invocation |
| **Week 2** | 2 sessions | ~4 hours | Reviewing other PRs; tackling a slightly larger task |
| **Week 3** | 1 session | ~2 hours | Deepening on a specific topic |
| **Week 4** | 1 session | ~2 hours | Path forward; cert review prep |

Total: 5-6 pair-driving sessions across 30 days, 12-14 hours of senior time invested in the new engineer.

## Why pair-driving

The harness has invariants the codebase alone won't reveal. Reading CLAUDE.md and AGENTS.md gives the engineer the documented part; pair-driving gives the undocumented part — why a particular skill is structured the way it is, what was tried before and rejected, what the team has learned the hard way.

Per Ch 44 §44.1, the day 2 morning is explicitly a senior-led harness walk. The discipline: that's the start, not the only session.

## Session structure

Each session follows roughly this shape:

### Pre-session (10 min)

- Buddy and engineer agree on the topic
- Engineer has a specific question or task in mind
- Buddy has a specific demonstration in mind

If neither has anything specific, that's a signal — the session shouldn't happen until there's a concrete focus.

### During the session (60-120 min typically)

- Both share screens (or co-located equivalent)
- The engineer drives most of the typing — pair-DRIVING, not pair-watching
- The buddy provides context, suggests patterns, asks "why" questions
- Real work or near-real work; not contrived exercises

### Post-session (10 min)

- Quick recap: what did we cover, what's the engineer's next step
- Any specific follow-up reading or practice
- Schedule next session if applicable

## Per-session focus

### Week 1 — Session 1 (Day 2 morning)

**Goal:** the engineer has a working mental model of the harness.

**Topics:**
- Tour `.claude/` directory: skills, subagents, hooks
- Walk through 3-5 most-used skills; engineer invokes one end-to-end
- Walk through standard subagent roster; show one running on a sample PR
- Show one hook firing on a deliberate test
- Walk through verify command: what runs, what catches what

**What good looks like:**
- Engineer asks substantive questions ("why is this skill structured this way?")
- Engineer notices things in the harness ("oh, this is what catches X failure")
- Buddy surfaces tribal knowledge ("we tried Y; it didn't work because Z")

**What to avoid:**
- Buddy lecturing the entire time without engineer driving
- Skipping past the engineer's questions to "cover everything"
- Making the engineer feel they should already know things

### Week 1 — Session 2 (Day 4 afternoon, optional but valuable)

**Goal:** the engineer has shipped or near-shipped their first PR with senior support.

**Topics:**
- Live review of the engineer's draft PR
- Walking through the seven slop signatures (per Ch 22 §22.2) in their diff
- Specific feedback on scope, tests, style, structure

**What good looks like:**
- Engineer catches at least one slop signature themselves before the buddy points it out
- Buddy explains the "why" behind feedback, not just the "what"
- The engineer leaves with concrete revisions to make

### Week 2 — Session 1 (Reviewing other engineers' PRs)

**Goal:** the engineer's review intuition is calibrated against the team's standards.

**Topics:**
- Pick 1-2 open PRs from other team members (with permission from authors)
- Engineer reviews while buddy observes
- Buddy points out things the engineer missed; explains things the engineer noticed but doesn't fully understand the significance of

**What good looks like:**
- Engineer's review surfaces real questions, not nits
- Buddy helps the engineer distinguish "stylistic preference" from "real issue"
- Engineer's questions during review reveal their evolving model of the team's standards

**What to avoid:**
- Pretending to review (going through the motions); review with substance only
- Reviewing the engineer's own PR (covered in week 1 session 2)

### Week 2 — Session 2 (Larger task pairing)

**Goal:** the engineer has worked alongside a senior on a task that's larger than week-1 work.

**Topics:**
- A real Tier-3 task that's still bounded but larger than what the engineer has tackled solo
- Pair on planning, implementation, review
- The buddy demonstrates patterns the engineer hasn't seen — particular skill compositions, specific prompting patterns, recovery from a failed first attempt

**What good looks like:**
- Both engineer and buddy contribute to the work
- Engineer asks "why are you doing it this way?" and buddy explains
- Engineer leaves with a pattern they can reuse

### Week 3 — Session 1 (Topic deepening)

**Goal:** the engineer has gone deeper on whatever specific topic matters most for their growth.

**Topics (pick one based on what the engineer needs):**
- **Subagent design** — for engineers heading toward platform team work
- **Specific high-use skill** — for engineers who'll be using a skill heavily
- **Testing patterns** — for engineers whose work touches test-heavy areas
- **Performance / observability** — for engineers in those domains
- **Specific service deep-dive** — for engineers who'll own a particular service

**What good looks like:**
- Topic is specific to the engineer's coming work, not generic
- The session produces a concrete deliverable (a draft skill, a draft test plan, a written summary)

### Week 4 — Session 1 (Path forward)

**Goal:** the engineer and buddy together have a shared plan for the engineer's next 60-90 days.

**Topics:**
- Review of the L1 cert criteria (per [`l1-certification-checklist.md`](l1-certification-checklist.md))
- Discussion: where is the engineer strong? Where are the gaps?
- L2 cert path: what work in the next quarter would build the L2 case?
- Specific next steps: which skills should the engineer learn next; which subagents should they study; what services should they get familiar with

**What good looks like:**
- The engineer leaves with a concrete plan, not a vague one
- The buddy commits to specific support over the next quarter
- The conversation is honest about gaps, not all-positive

## Cross-references to junior-trajectory

The senior engineer running pair-driving for a new mid-career hire applies the same general patterns from `junior-trajectory/pair-driving-guide.md`:

- Engineer drives the typing; buddy provides context
- Real work, not contrived exercises
- Substantive feedback, including challenging feedback
- Specific takeaways per session

The differences for AI-tooling onboarding (vs. junior development):

- Less time on engineering fundamentals; the new hire has them
- More time on team-specific harness patterns
- Less mentorship of professional growth; more mentorship of team integration
- Faster pace overall — the new hire is expected to ship in week 1

## Anti-patterns

### Buddy distracted during the session

Buddy is in Slack, responding to other things. The engineer feels unsupported.

Mitigation: the session is committed time. Slack DnD; calendar block; phone aside.

### Engineer not asking questions

Engineer is intimidated; they nod along but don't engage. The session produces no signal.

Mitigation: buddy explicitly asks "what's not making sense?" multiple times. Creates space for the awkward questions.

### Sessions canceled and not rescheduled

A buddy gets pulled into something urgent; the session is canceled. Then it gets canceled again. Then nobody reschedules.

Mitigation: cancellations are rescheduled within 48 hours. If a buddy can't commit reliably, that's grounds for switching buddies.

### Pair-driving as code review

The session is the engineer showing their work; the buddy critiquing. No actual co-work happens.

Mitigation: pair-driving is co-work. Code review is a different ritual (PR review). The two shouldn't collapse.

### Sessions without specific focus

"Let's just chat about how things are going." Sometimes valuable; usually a missed opportunity.

Mitigation: every session has a specific focus agreed before it starts. "How are things going" is a 1:1 conversation, not a pair-driving session.

### Buddy showing off

Buddy demonstrates impressive techniques; engineer is intimidated rather than empowered.

Mitigation: pair-driving is for the engineer's growth, not the buddy's display. Buddy demonstrates patterns the engineer can use, not patterns that require the buddy's specific experience.

## What pair-driving will NOT do

- Will not work without dedicated buddy time. Senior engineers are already over-committed; pair-driving must be allocated and protected.
- Will not work as a one-time session. The cadence is the discipline.
- Will not substitute for the engineer's own learning. Pair-driving is one input among several.
- Will not work for buddy-engineer mismatches. If the personalities or working styles don't fit, switch buddies (per [`buddy-and-manager-roles.md`](buddy-and-manager-roles.md)).

## Companion artifacts

- [`week-1-curriculum.md`](week-1-curriculum.md) — the broader curriculum
- [`days-8-to-30.md`](days-8-to-30.md) — the broader curriculum
- [`buddy-and-manager-roles.md`](buddy-and-manager-roles.md) — who's the buddy
- [`l1-certification-checklist.md`](l1-certification-checklist.md) — what the sessions build toward
- `junior-trajectory/pair-driving-guide.md` — adjacent (junior-specific patterns)
- Ch 44 §44.1 — source
