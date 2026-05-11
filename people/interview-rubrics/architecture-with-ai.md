# Architecture-with-AI Conversation — Rubric

A 60-minute whiteboard discussion where AI tooling is in the room as a thinking partner. Per Ch 60 §60.5 of _Software Engineering with AI_.

## Purpose

To assess how the candidate designs systems WITH AI tooling, not just before. The signals we want:

- Can the candidate use AI tooling productively during the conversation, or does it slow them down?
- When they disagree with the agent's suggestion, can they explain why with specifics?
- Do they treat AI output as a starting point for thinking, or as a finished answer to defer to?
- Can they articulate where AI is weak in the design problem and what constraint surface they'd build to protect it?

## Format

- **60 minutes**, live, with whiteboard or shared doc.
- **Two interviewers**, one leading the conversation and one taking notes.
- Candidate may use **any AI tool they're comfortable with**: Claude Code, Cursor, ChatGPT, etc. They are not required to use one — declining is a valid choice we don't penalize.
- The problem is **not a system design textbook problem.** It's a problem from the actual work: "design the rate-limiting subsystem for our public API given these constraints" or "design the schema migration tooling we'd want to support 10x growth."

## What the candidate produces

A working sketch — boxes, arrows, schemas, contracts, ADR-style decisions — with explicit reasoning about:

- The Direction, Architecture, and Evaluation considerations (Ch 5 §5.2)
- The constraint surfaces (lints, hooks, schemas) that protect the design from foreseeable failure modes
- Where AI tooling helped, where it was wrong, where it was useful as a sounding board

## Grading rubric

### AI tooling fluency — 3 points
- **Excellent**: Uses the tool naturally. Asks targeted questions, evaluates the response critically, integrates what's useful, discards what's not. The tool accelerates their thinking.
- **Good**: Uses the tool well in some moments, less well in others. Net positive on the conversation.
- **Weak**: Uses the tool but it slows them down. Defers to AI output without evaluation.
- **Poor**: Either refuses to engage with the tool at all, OR pastes the AI's response wholesale without thinking.

Note: a candidate who chooses NOT to use AI tooling is not penalized in this dimension if they can articulate why ("I'd want to think this through first, then check my reasoning against an agent").

### Direction / Architecture / Evaluation framing — 4 points
- **Excellent**: Explicitly considers all three. Can articulate which is the harder problem in this design and why.
- **Good**: Considers two of the three solidly; gestures at the third.
- **Weak**: Strong on one (usually Architecture); weak on the others.
- **Poor**: Treats the problem as a pure architecture diagram with no thought for what success looks like or how we'd know.

### Constraint-surface design — 3 points
- **Excellent**: Identifies where AI tooling would be weak in the proposed system and designs explicit constraint surfaces (lints, hooks, schemas, CODEOWNERS routes) to protect those areas.
- **Good**: Identifies one or two areas where constraints would help.
- **Weak**: Constraints are an afterthought; the candidate would build the system and add safety later.
- **Poor**: No constraint-surface thinking at all.

### Trade-off articulation — 3 points
- **Excellent**: Names trade-offs explicitly with quantified estimates where possible. "Adding the cache adds 20ms p50 in the cold path but reduces p99 from 800ms to 200ms."
- **Good**: Names trade-offs qualitatively. "There's a complexity cost here."
- **Weak**: Picks one approach without articulating why; doesn't explore alternatives.
- **Poor**: Argues for an approach as if it's the only option.

### Pushback on AI suggestions — 3 points
- **Excellent**: Disagrees with the agent's suggestion at least once during the session, with a specific reason. The disagreement is well-founded.
- **Good**: Disagrees with the agent occasionally; reasoning is OK.
- **Weak**: Defers to the agent's suggestions consistently.
- **Poor**: Either accepts everything the agent says, OR dismisses everything without evaluation.

**Total possible:** 16

## Calibration thresholds

- **Strong hire (14-16):** the candidate's architectural reasoning meets the bar AND they integrate AI tooling at the senior level we want.
- **Hire (11-13):** strong on either architecture OR AI integration but not both. The PR review exercise and harness conversation are the tiebreakers.
- **Weak (8-10):** would need significant ramp on either the architecture or the AI integration dimension.
- **No (≤7):** not at the senior level for either dimension.

## What this rubric will NOT do

- Will not surface candidates who interview poorly under whiteboard pressure even though they design well in real life. Consider offering them the take-home format if you suspect this.
- Will not work for a candidate who uses an AI tool you've never seen. The interviewers should be AI-tooling-fluent themselves; if they aren't, they can't grade this round.

## Common failure modes for the interviewer

- **Grading on the diagram quality.** A messy whiteboard with sharp reasoning beats a clean diagram with shallow reasoning.
- **Letting the candidate's AI-tool brand bias the grade.** Cursor user, Claude Code user — same signal, different surface.
- **Forgetting to take notes on the candidate's pushback against the AI.** This is one of the most predictive signals; it's easy to miss in real time.

## Tips for the interviewing team

- **Choose problems where AI tooling is genuinely useful.** Pure algorithmic problems make poor architecture-with-AI conversations.
- **Pre-agree on the "right" answer space.** Multiple solutions should be valid. If only one solution is acceptable, the conversation is a quiz, not a conversation.
- **Watch for "AI did all the work."** A candidate who pastes the agent's response with no engagement is not demonstrating senior judgment.
