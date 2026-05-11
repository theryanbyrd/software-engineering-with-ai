# The 18-Month Junior Curriculum

The four-phase program for developing a junior engineer from "can read a diff" to "can lead a small design and contribute to the harness." Direct implementation of Ch 42 §42.3.

The phases are not 4.5 months each. They overlap. A junior in phase 3 is still doing phase 2 work, just with new responsibilities added. The numbers below are when the new phase's work *starts*, not when the previous phase ends.

## The four phases

| Phase | Months | Focus | Exit criterion |
|---|---|---|---|
| **1. Review discipline** | 0-6 | Reading code critically; recognizing patterns; spotting slop | Can review an agent-authored PR and find issues a senior would find, with calibrated severity |
| **2. Small features** | 4-12 | Shipping T1 work end-to-end; writing the spec, the code, the tests, the docs | Can ship a T1 feature solo without senior intervention |
| **3. Harness contribution** | 9-15 | Contributing to the team's skills, hooks, CLAUDE.md investment | Has shipped a harness component used by other engineers |
| **4. First solo design** | 12-18 | Owning a small design end-to-end with senior review | Has led a small (T2) design that's now shipped and operating |

The exit criteria are not boxes to check; they're observable signals the manager assesses against the [`calibration-rubric.md`](calibration-rubric.md).

---

## Phase 1 — Review discipline (months 0-6)

The most important phase. Skipping this phase produces engineers who never develop pattern recognition; they remain dependent on senior validation indefinitely.

### Why this comes first

Per Ch 42 §42.1, the high-value engineer profile in 2026 starts with code review intuition. Engineers who can spot the seven slop signatures in seconds run productive AI sessions; those who can't either reject everything or accept everything. Junior engineers who skip the review-first phase end up in the latter category.

### What the junior actually does

#### Months 0-2: Foundation

- **Read code daily.** 30-60 minutes per day reading the codebase. Not in PRs; in the existing code. The mentor assigns specific modules. The junior writes a one-paragraph summary of each: what does this do, what's the contract, what's confusing.
- **Shadow senior reviews.** The junior reads every PR review the senior writes for 4-6 weeks. Not as a reviewer; as a reader. After each, the junior writes 2-3 bullets: what did the senior catch that I'd have missed, what would I have flagged that the senior didn't, what was the severity calibration.
- **Daily verify discipline.** The junior runs the team's `verify` command on every change they touch (their own and others'). They learn the verify failure modes by feel.
- **Read the seven slop signatures (Ch 22) weekly for six weeks.** Yes, weekly. The signatures don't internalize on first read; they internalize through repetition and example.

#### Months 3-4: Active reviewing

- **First reviews on agent-authored PRs.** Specifically agent-authored, not human-authored. The junior reviews PRs the senior has already reviewed; the senior reviews the junior's review. Two-pass discipline.
- **Specific assignments:** review for slop signatures S1 (imaginary API), S5 (tests-without-testing), and S7 (scope creep) in the first month; expand to all seven by end of month 4.
- **Weekly review cohort.** A 30-minute meeting where the junior, mentor, and one other senior walk through 2-3 PRs from the week. The junior reviews live; the seniors push back; everyone calibrates.

#### Months 5-6: Trusted reviewer at the L3 bar

- **Reviews count as a real review now.** PRs no longer need a senior secondary review on what the junior reviewed (for L3-eligible PRs).
- **The junior catches things in advance of the senior at least once a month.** This is the threshold for "review discipline is real." Document it when it happens.
- **The junior can articulate why a review is good or bad without checking the slop signature list.** The signatures have moved from explicit to implicit knowledge.

### What the manager and mentor do

- **Mentor reviews every code-review the junior does for the first 8 weeks.** Yes, every one. The investment is heavy; the payoff is durable.
- **Manager protects 30-60 min/day for code-reading time.** Without protected time, the junior spends every minute on tickets and never builds depth.
- **Manager runs the 1:1 cadence weekly.** See [`manager-1on1-playbook.md`](manager-1on1-playbook.md). Skipping the 1:1 in the first 6 months is the failure mode that kills the program.

### Exit criterion (end of phase 1)

The junior can review an agent-authored PR with the same discipline as a senior would. Specifically:

- Identifies the slop signatures that are present, with calibrated severity
- Asks "should this PR exist at all?" when appropriate
- Pushes back constructively, with specifics
- Does not rubber-stamp; does not over-flag; calibrates well
- Net signal: senior engineers stop double-checking the junior's reviews on T1 work

### What goes wrong in phase 1

- **The junior is given too many tickets.** Ticket pressure crowds out reading time. Manager fixes this by reducing the junior's ticket load by 40-50% during phase 1, not by asking the junior to "be more efficient."
- **The mentor is not available.** Mentors who are themselves on-call rotation, leading a separate team, or interviewing heavy cannot mentor a junior. Manager either reassigns the mentor or pauses the program.
- **The junior plateaus on slop detection.** They can find S1 (imaginary API) easily but never spot S6 (comment drift) or S7 (scope creep). The mentor adds targeted exercises — pull a PR with S6 and ask the junior to review without telling them what to look for.
- **The junior over-flags.** Every PR comes back with 15 comments, 12 of which are nits. The mentor coaches: "What's the one thing you would block this PR for?" forces calibration.

---

## Phase 2 — Small features (months 4-12)

Phase 2 starts overlapping with phase 1. The junior keeps reviewing while now also shipping.

### What the junior actually does

#### Months 4-6: First solo T1 work

- **The first ticket is a T1 from the team's actual backlog.** Not a contrived "first task." A real one, where the senior would have done it in 1-2 hours.
- **The junior writes the spec themselves.** Yes, they write the spec, even though it's a small task. Writing the spec builds the Direction muscle.
- **The senior reviews the spec before the junior implements.** This is where Direction discipline lands. The senior pushes back on the spec; the junior revises.
- **The junior implements with light agent assistance.** Specifically: the junior is encouraged to use the agent for the parts they understand well, not for the parts that are new. (Counterintuitive but correct — agent acceleration on familiar work is safer than agent acceleration on unfamiliar work.)
- **The junior runs verify, writes tests, opens the PR, gets reviews, ships.**

#### Months 6-9: Multiple T1s; first T2

- **Multiple T1 features per quarter.** The junior is doing 2-3 T1 features per sprint, with progressively less hand-holding.
- **First T2 attempt.** A small T2 (the easy end of the tier — clear scope, well-understood pattern, low blast radius). The senior is more involved here; this is the bridge to T2 work.
- **First incident participation.** The junior is on call for low-severity issues with the mentor. Owns at least one minor incident end-to-end including writing the postmortem.

#### Months 9-12: Trusted T2 contributor

- **T2 features regularly.** The junior is a real contributor to the team's T2 throughput.
- **The junior writes the spec, often without senior pre-review.** They've internalized what an agent-ready spec looks like.
- **The junior is comfortable using the agent for genuinely new work.** They know how to tell when the agent is wrong; they know when to push back; they know when to check.

### What the manager and mentor do

- **Senior owns spec-review discipline for the first 6 months of phase 2.** Spec review is where Direction is taught; without it, juniors learn to write code but not specs.
- **Manager assigns first incident carefully.** A real incident, low severity, with the mentor available. Not a contrived "let's pretend this is broken" exercise.
- **Manager protects against the over-tickets failure mode.** Some junior engineers, once they ship one T1, ship 5 in a week. This produces velocity but not depth. The manager pulls back ticket load and creates space for harness work in phase 3.

### Exit criterion (end of phase 2)

- The junior can ship a T1 feature solo without senior intervention beyond the standard PR review.
- The junior writes specs that don't require multiple revisions before agent work begins.
- The junior is contributing meaningfully to T2 features with senior collaboration.
- The junior has owned at least one incident and written its postmortem.

---

## Phase 3 — Harness contribution (months 9-15)

Phase 3 is where the AI-native engineering signature appears. The junior contributes to the team's harness — skills, hooks, subagents, CLAUDE.md investment, MCP integrations.

### Why this matters

The L3 → L4 promotion criterion includes harness contribution per `people/career-ladder/ic-track-additions.md`. Engineers who never contribute to harness in their first 18 months tend to never contribute at all. Building the muscle in phase 3 is what makes L4 promotion realistic.

### What the junior actually does

#### Months 9-11: First contribution

- **Bug-fix on existing harness.** A skill that's giving wrong output. A hook that's overly aggressive. A CLAUDE.md section that's outdated. The junior fixes one of these with senior review.
- **Write a SKILL.md for an unwritten skill.** The team has a recurring task that's not yet a skill; the junior writes it following the canonical shape (Ch 13 §13.4 / `skills/db-migration/SKILL.md`).
- **Pair on a hook with the mentor.** The mentor leads; the junior writes the bash script, the test cases, the commit. The hook ships.

#### Months 12-15: Solo contribution

- **The junior owns a small harness component.** Their own skill, their own hook, their own CLAUDE.md section that they wrote and maintain.
- **The component is used by other engineers.** Not a personal-use script. Something the team adopts. This is the threshold for "real" harness contribution.
- **The junior maintains it.** They respond to bugs in their component, iterate on it based on feedback, document it.

### What the manager and mentor do

- **Senior identifies the right first contribution.** Too small (a CLAUDE.md typo fix) and the junior doesn't learn anything. Too big (build a new MCP server) and the junior fails. The manager and mentor pick the contribution carefully.
- **Manager protects 4-8 hours a week for harness work.** Without protected time, harness work falls off; tickets always feel more urgent. The manager actively defends the time.
- **Mentor reviews the first solo contribution carefully.** This is the bridge from "can fix bugs in existing harness" to "can ship harness." The review is the teaching moment.

### Exit criterion (end of phase 3)

- The junior has shipped at least one harness component used by other engineers.
- The junior maintains the component (responds to bugs, iterates).
- The junior can articulate the design choices they made and the alternatives they rejected.
- The component meets the team's quality bar (documentation, tests where appropriate, fits the team's patterns).

---

## Phase 4 — First solo design (months 12-18)

The capstone. The junior leads a small design end-to-end. Not the implementation alone — the design conversation, the ADR, the implementation, the deployment, the followup.

### What the junior actually does

#### Months 12-15: Design participation

- **The junior contributes to design conversations led by seniors.** Active contribution, not passive listening. They're asked specific questions: "What's the failure mode here?" "What would the constraint surface look like?"
- **The junior writes ADRs for their own work.** Even if they're implementing someone else's design, they write the ADR explaining the implementation choices.
- **The junior reviews ADRs from peers.** Reviewing design documents is itself a skill; the junior practices it.

#### Months 15-18: Solo design

- **The junior leads a small T2 design.** A clear-scope, low-blast-radius piece of work where they own the design conversation.
- **The senior is in the room as a sounding board, not the lead.** This is the inversion point — the junior is now driving the conversation.
- **The junior writes the ADR; the team reviews; the junior revises; the design is approved.**
- **The junior implements with the team's normal review discipline.**
- **The junior owns the rollout, including any incidents.**

### Exit criterion (end of phase 4)

- The junior has led one small T2 design end-to-end.
- The design is in production and operating.
- The junior can articulate what they would do differently next time.
- The senior team trusts the junior to run the next small design with less oversight.

This is the L3 → L4 promotion threshold per `people/career-ladder/`.

---

## Throughout all phases

### Mentor relationship

- 2 seniors per junior, per Ch 42 §42.3. One primary mentor (who the junior pair-drives with), one secondary (for backup, perspective, and to prevent over-dependence on a single senior).
- Mentor cycle changes every 6 months. The junior gets exposure to multiple senior styles.
- Mentor responsibility is explicit in the senior's perf review (per `people/perf-reviews/`).

### Pair-driving on agent sessions

The most important hour of the junior's week. See [`pair-driving-guide.md`](pair-driving-guide.md). The junior watches a senior run an agent session — the senior narrates what they're doing and why. After 4-6 weeks, the junior drives while the senior observes.

This is the mechanism by which engineering judgment transfers. Code reviews show what's wrong; pair-driving shows how a senior thinks.

### Direction / Architecture / Evaluation rotation

Per Ch 5 §5.2, the three bottleneck disciplines. The junior rotates through:

- **Direction (writing specs)** — heavy in phase 2
- **Architecture (designing systems)** — heavy in phase 4
- **Evaluation (designing how we measure)** — light touch through all phases; deep dive in months 15-18 if the junior is on the platform team

The rotation is not strict; the junior should touch all three, but depth comes in their L4 trajectory choice (see `people/jds/senior-engineer-direction.md` etc.).

### Postmortems

Per Ch 42 §42.3, postmortem ownership is mandatory for the junior. They own at least one postmortem in phase 2 and one substantial postmortem in phase 3 or 4. Postmortem ownership develops the investigative discipline that distinguishes senior engineers.

---

## What the curriculum will NOT do

- **Will not produce a senior engineer in 18 months.** That's not the goal. The goal is to produce a credible L3-going-on-L4 engineer who has the foundation for the next 3-5 years of growth.
- **Will not work with a junior who lacks foundational coding skills.** The program assumes the junior can write code; it teaches engineering judgment.
- **Will not save a hire who shouldn't have been hired.** The 6-month calibration is honest about this. Some juniors won't make it; the rubric tells you which ones, when.
- **Will not scale beyond 1:2 mentor:junior ratio.** Try to scale and it dilutes; everyone burns out.

## When to deviate from the curriculum

Some juniors come in with substantial prior experience (3+ months of bootcamp + side projects + open source contributions). Compress the curriculum: phase 1 in 3 months, phase 2 starting at month 2, etc. The junior who has already been writing code in real codebases doesn't need the same on-ramp.

Some juniors plateau in phase 1. They can't reliably review code; they're missing slop signatures even at 6 months; the calibration rubric flags this. The honest answer: extend phase 1 by 3-6 months OR have the conversation about whether this is the right role. See [`calibration-rubric.md`](calibration-rubric.md).

## Companion artifacts

- [`anti-patterns.md`](anti-patterns.md) — what kills the curriculum
- [`manager-1on1-playbook.md`](manager-1on1-playbook.md) — the weekly cadence that makes the curriculum work
- [`calibration-rubric.md`](calibration-rubric.md) — the 6/12/18-month assessments
- [`pair-driving-guide.md`](pair-driving-guide.md) — the most important hour of the week
- `skills/code-review/SKILL.md` — the canonical review discipline
- Ch 22 — the seven slop signatures
- Ch 42 §42.3 — the source of the curriculum
