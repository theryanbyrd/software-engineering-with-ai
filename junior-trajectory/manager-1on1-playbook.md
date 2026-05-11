# Manager 1:1 Playbook

The weekly 1:1 cadence between manager and junior. The single most important manager investment in junior development.

Skipping or shortening the 1:1 cadence is the most common cause of junior development failure. The 1:1 is the mechanism by which anti-patterns surface, the curriculum gets adjusted, and the manager has the data they need at calibration time.

## Cadence

- **Frequency:** weekly, no exceptions for the first 12 months. Biweekly in months 13-18 only if the junior is clearly on track.
- **Duration:** 30 minutes minimum. 45 if there's been a substantive piece of work to discuss.
- **Format:** in-person if same office; video if not; never phone-only or async-only.
- **Cancellations:** reschedule, never skip. If the junior cancels twice in a quarter, the manager probes; if the manager cancels twice, the junior does.
- **Notes:** the manager keeps notes, not the junior. Light notes — what came up, what action items, what to follow up on.

## Structure of a typical 1:1

Not a checklist; a rhythm:

1. **Open with their question first** (5 min). "What's on your mind?" Sometimes nothing; often something specific. Always lead with their agenda.
2. **Recent work** (10 min). What they shipped, what they reviewed, what they're stuck on. Not status reporting; conversation.
3. **One curriculum-relevant topic** (10 min). Selected from the question banks below based on the junior's phase. This is the part the manager prepares.
4. **Wrap-up** (5 min). Action items, anything to escalate, when next week is.

## Question banks by phase

### Phase 1 (months 0-6) — Review discipline

The questions in phase 1 surface whether the junior is actually building review judgment or going through motions.

#### Reading and pattern recognition

- "What did you read this week that surprised you?" *Surfaces whether they're reading anything beyond their own tickets.*
- "Show me a piece of code in our codebase you don't understand. Walk me through what's confusing." *Surfaces whether they have the courage to admit not knowing things.*
- "Which of the seven slop signatures do you find easiest to spot? Hardest?" *Surfaces calibration and helps target the next 4 weeks of practice.*
- "Tell me about a PR review you did this week. What did you catch? What might you have missed?" *Forces metacognition.*

#### Mentor relationship

- "What did your mentor teach you this week — specifically?" *If they can't answer, the mentor isn't mentoring.*
- "Are you having the pair-driving sessions on cadence?" *Direct check.*
- "What would make the mentor relationship work better for you?" *Sometimes the junior is too polite to ask.*

#### Energy and direction

- "What part of the work this week energized you?" *Tells you where to point them next.*
- "What part felt like a slog?" *Tells you where to investigate; chronic slog signals anti-pattern 6 (over-tickets) or wrong fit.*
- "Are you still glad you took this role?" *Periodic check; if the answer turns negative, surface early.*

### Phase 2 (months 4-12) — Small features

The questions in phase 2 surface whether the junior is engaging with their own work or shipping on autopilot.

#### Spec and direction

- "Walk me through the spec for [your last ticket]. What did you decide to include? What did you decide to leave out?" *Forces them to articulate Direction discipline.*
- "Where did the spec leak — meaning, where did you have to make decisions during implementation that the spec didn't cover?" *Surfaces whether their specs are getting more complete over time.*
- "If you were the senior reviewing your own spec, what would you push back on?" *Builds self-review.*

#### Implementation and engagement

- "Tell me about a decision you made in the code this week that you can't fully justify. What's nagging you?" *Critical question. Surfaces whether they're shipping things they don't understand.*
- "Tell me about a time the agent suggested something you pushed back on this week." *If they can't, anti-pattern 2 is in play.*
- "What's the worst code in this PR? Walk me through it." *Surfaces honesty about quality. The junior who claims everything is fine is hiding.*

#### Incidents and ownership

- "Have you been on call this week? Any pages? What happened?" *Surfaces whether they're owning incidents.*
- "What postmortem are you most proud of writing? What would you change?" *Develops investigative discipline.*

### Phase 3 (months 9-15) — Harness contribution

The questions in phase 3 surface whether the junior is moving from consumer to contributor.

#### Contribution direction

- "What's a recurring annoyance in our team's tooling that you'd want to fix?" *Identifies opportunity space.*
- "Who else on the team would benefit from the [skill / hook / improvement] you're building?" *Forces them to think about reach beyond personal use.*
- "What's the failure mode of your contribution? What happens when it's wrong?" *Forces trade-off thinking.*

#### Maintenance posture

- "Has anyone reported a bug in your harness contribution? What did you do about it?" *Surfaces whether they're maintaining.*
- "What would you change about your contribution if you were starting over?" *Iteration mindset; per `people/perf-reviews/harness-contribution.md`.*

#### Mentorship readiness

- "When [newer junior] asks you a question, what's your default response?" *Surfaces whether they're starting to mentor — or replicating the rubber-stamp pattern downward.*

### Phase 4 (months 12-18) — First solo design

The questions in phase 4 surface whether the junior is ready for L4-track work.

#### Design

- "Walk me through the design for [their current work]. What did you reject and why?" *Same as Phase 2 spec question, but now at architecture level.*
- "What's the constraint surface for this design? What lints, schemas, or hooks would you add?" *Direct test of Ch 5 §5.2 constraint-surface thinking.*
- "Who else's design would you have wanted in the room as you worked on this?" *Surfaces whether they're using senior collaboration effectively.*

#### Trade-offs

- "Tell me a trade-off you made you're not sure about. What's the case for the other option?" *Forces honest articulation of uncertainty.*
- "What's the unsexy part of this design — meaning, the part nobody will appreciate but matters?" *Surfaces deep thinking.*

#### Trajectory

- "Which discipline (Direction / Architecture / Evaluation) feels most natural to you? Which feels hardest?" *Inputs to L4 trajectory choice.*
- "What's the senior engineer you most want to be like? What specifically do you admire about them?" *Surfaces aspirations; useful for mentor matching.*

## When the answer surfaces a problem

### "I'm rubber-stamping reviews"

If the junior says (or implies) they're approving reviews without reading carefully:
- Do not punish. The honesty is valuable.
- Coach: "What would change if you treated every PR like the senior would — what would you check?"
- Adjust workload: too many reviews per week is the underlying cause. Reduce.
- Increase mentor pre-review pairing temporarily.

### "I can't explain my own code"

If the junior cannot explain a chunk of code in their PR:
- Pause the PR. Don't merge.
- Have the junior re-read the code, line by line, with the mentor.
- For the next 2 weeks, every PR review with the junior includes "walk me through this commit."
- Discuss why. Often the cause is anti-pattern 2 (agent-only output); sometimes it's overload.

### "My mentor isn't really mentoring"

If the junior signals the mentor relationship isn't working:
- Believe them.
- Investigate. Often the senior is overloaded or distracted, not unwilling.
- If the senior cannot recommit to mentorship, change the mentor. Don't keep the form without the substance.
- Don't make the junior the messenger. The manager has the conversation with the senior.

### "I'm thinking about leaving"

If the junior signals retention risk:
- Same conversation as the senior retention conversation in `migration-playbooks/team-conversation-scripts.md` §7. Listen first.
- Specifically check: comp gap, growth gap, mentor gap, scope gap.
- If the cause is comp: move on it. Per anti-pattern 8, junior comp at the floor is a false economy.
- If the cause is growth: the curriculum is the answer; show them where they are and where the next 6 months point.

### "I'm bored"

If the junior signals boredom:
- Check the phase. A phase 1 junior who's "bored" is often skipping the depth work. Don't accelerate them; deepen them.
- A phase 3 junior who's bored is often ready for harness contribution. Accelerate.
- Boredom is usually a signal mismatch with the curriculum. The curriculum almost never says "the junior should be bored at this phase."

## What to write down

Light notes the manager keeps in their own private system:
- Date of 1:1 (skip frequency tracking)
- One sentence on what came up that's worth tracking
- Action items (yours and theirs)
- Anti-pattern signals you noticed (for calibration)
- Topics to come back to next week

What NOT to write down:
- Verbatim quotes from the junior
- Anything that would be embarrassing if the junior saw it
- Performance management content (different system)

## What this playbook will NOT do

- Will not make a manager who doesn't care about junior development care. The cadence is hollow without the underlying investment.
- Will not work for a manager who is themselves overloaded. If the manager has 15 reports, the 30-minute weekly 1:1 with each junior is mathematically impossible. Fix the structural issue first.
- Will not work in a culture where managers are evaluated on team velocity rather than team development. Calibrate the manager's incentives upstream.

## Companion artifacts

- [`18-month-curriculum.md`](18-month-curriculum.md) — what the 1:1 supports
- [`anti-patterns.md`](anti-patterns.md) — what the 1:1 surfaces
- [`calibration-rubric.md`](calibration-rubric.md) — where the 1:1 data feeds
- [`pair-driving-guide.md`](pair-driving-guide.md) — what the senior runs in parallel
