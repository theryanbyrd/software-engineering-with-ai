# Harness Component Conversation — Rubric

A 45-minute conversation about a harness component the candidate has shipped. Per Ch 60 §60.5: "Add a 'tell me about a recent harness component you shipped' question."

## Purpose

To assess whether the candidate has shipped real work that improved a team's AI-native engineering experience. The signals we want:

- Have they done it, or do they only talk about it?
- Can they articulate the problem the component solved?
- Do they understand the trade-offs they made?
- Would they do something differently now?
- Is the work durable — did other people use it without them?

## Format

- **45 minutes**, live or video.
- **One interviewer**, ideally the most platform-experienced senior on the team or the platform engineer.
- The candidate is asked to **walk through one harness component they shipped** in the last 12-18 months: a skill, a hook, a subagent, an MCP integration, a CLAUDE.md / AGENTS.md investment, a CI integration, a verify command, a custom auditor.

## The conversation

The interviewer's job is to extract the substance of the work. The conversation typically follows this arc:

1. **Setup** (5 min): "Tell me about a harness component you've shipped recently. What was it?"
2. **The problem** (10 min): "What problem did this solve? How did you know it was a problem worth solving? What did you try first that didn't work?"
3. **The design** (10 min): "Walk me through the design. Why did you make these choices? What did you reject?"
4. **The trade-offs** (10 min): "What did you sacrifice? Where is the component still rough? What's the failure mode?"
5. **The outcome** (5 min): "Did other people use it? How do you know? What would you change now?"
6. **Wrap and questions** (5 min): "What's your next harness investment?"

## Grading rubric

### Realness — 4 points (gating)
- **Excellent**: The candidate has clearly shipped this. They can answer specific implementation questions, cite line numbers from memory, describe the bugs they hit.
- **Good**: Mostly real with some hand-waving on details. May have shipped a smaller version than they're describing.
- **Weak**: Vague on specifics. The work may have been concept-level only.
- **Poor**: The story doesn't hold together. Likely fabricated or significantly inflated.

**This dimension is gating.** Anything below "Good" should not pass this round.

### Problem articulation — 3 points
- **Excellent**: Names the specific pain point, with evidence. "Three engineers on the team had separately written variations of this script in the last month, all subtly broken in different ways."
- **Good**: Articulates the problem at the team level. "We needed a way to do X consistently."
- **Weak**: Generic problem framing. "It seemed useful."
- **Poor**: No clear problem; the work was speculative.

### Design choices — 3 points
- **Excellent**: Can articulate at least three design choices and the alternatives they rejected. The rejections are well-reasoned.
- **Good**: Articulates one or two design choices clearly.
- **Weak**: Describes the implementation as if the design was the only option.
- **Poor**: Confused about why specific choices were made.

### Trade-off awareness — 3 points
- **Excellent**: Names what's bad about the component or where it falls short. Explicitly identifies the failure mode and the conditions under which it would not be the right tool.
- **Good**: Acknowledges some limitations.
- **Weak**: Defends the component as if it has no trade-offs.
- **Poor**: Cannot articulate any trade-off; treats the component as universally good.

### Adoption / outcome — 3 points
- **Excellent**: The component was adopted by other engineers, ideally on other teams. The candidate has data or specific stories on the adoption.
- **Good**: Used by their team; they can describe two or three concrete adoption moments.
- **Weak**: Used by the candidate themselves; unclear whether anyone else picked it up.
- **Poor**: Built but not used; or "I think it helped" without evidence.

### Iteration mindset — 2 points
- **Excellent**: Has specific things they'd do differently. The reasoning shows growth, not regret.
- **Good**: Some concrete iteration plans.
- **Weak**: "It's working fine; nothing I'd change."
- **Poor**: Defensive about the component as built.

**Total possible:** 4 (gate) + 3 + 3 + 3 + 3 + 2 = 18, with the realness dimension as a gate (anything below 3 is a no-hire signal).

## Calibration thresholds

- **Strong hire (15-18):** the candidate has shipped real harness work at the senior level. Move to offer.
- **Hire (12-14):** real work, somewhat smaller scope or somewhat softer signals. Combined with strong PR review and architecture rounds, this is a hire.
- **Weak (9-11):** the work is real but small. Discuss whether the role expects more harness scope.
- **No (≤8 OR realness below "Good"):** not a senior signal in this dimension.

## What this rubric will NOT do

- Will not penalize a strong IC who hasn't focused on harness work. If the candidate's strength is product feature delivery and they admit harness is a gap, that's an honest answer; weigh against the role.
- Will not work for candidates who are very recent to AI engineering. If the candidate has been doing AI-tooling work for under 12 months, the harness contribution may not yet have emerged. This is acceptable for L4 hires; L5+ should have the contribution.

## Common failure modes for the interviewer

- **Accepting "I introduced AI tooling at my company" as a harness contribution.** That's adoption, not contribution. Probe for the specific component.
- **Letting the candidate talk about a vendor product they configured.** Configuring Cursor settings is not shipping a harness component.
- **Skipping the trade-offs question.** This is the most predictive of senior judgment; if you skip it, the rubric isn't doing its job.

## What we explicitly DO accept as harness contributions

- A skill, hook, or subagent shipped to a shared `.claude/` directory
- A CI integration that runs an audit, a slop detector, or a prompt-injection test
- A CLAUDE.md or AGENTS.md investment that meaningfully changed team velocity (but probe — most "I wrote a CLAUDE.md" stories are too small)
- An MCP server they built or significantly contributed to
- A skill library, subagent roster, or hook framework at the org level
- A verify command they designed and got the team to adopt
- An evaluation framework for the team's AI-tool usage

## What we DO NOT accept

- "I taught the team to use AI tools."
- "I picked the AI tool we use."
- "I wrote a Slack channel about AI tools."
- "I added a few entries to .cursorrules."
