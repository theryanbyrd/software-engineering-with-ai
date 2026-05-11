# Pair-Driving on Agent Sessions

The most important hour of the junior's week. The mechanism by which engineering judgment transfers from senior to junior in the AI-native era.

Code review shows what's wrong. Pair-driving shows how a senior thinks.

## Why pair-driving matters

The senior engineer who runs a productive agent session is making 30-50 micro-decisions per session: what to prompt, when to stop the agent, what to push back on, when to accept, when to delete and start over, when to commit and step back.

These decisions are largely tacit. The senior doesn't write them down because they don't need to — they happen in seconds, by feel. A junior cannot learn these decisions by watching the output (the merged PR) or even by reading reviews. They learn by watching the senior decide *in real time* and asking why.

The format: the senior runs an agent session for 30-60 minutes; the junior watches and asks questions; the senior narrates their thinking. After 4-6 weeks, the junior drives while the senior observes.

## Cadence

- **Frequency:** weekly during phases 1-2 (months 0-12). Biweekly thereafter.
- **Duration:** 30-60 minutes. Long enough for a real session; short enough that the senior doesn't burn out.
- **Format:** in-person or screen-share. Async (recorded) is a poor substitute; the live questioning is the value.
- **Defended on the calendar.** Like the 1:1 cadence, this is the easy thing to skip; skipping kills the program.

## Phases of pair-driving

### Phase A — Senior drives, junior observes (months 0-2)

The senior runs an agent session on real work — not a contrived demo. The junior watches. The senior narrates:

- "I'm going to start by reading the existing handler before I prompt the agent. The agent will do better with the file in context."
- "Notice that I'm phrasing the request as 'add the field, mirror the existing pattern in line N.' I'm not saying 'add the field'; I'm telling the agent what pattern to mirror."
- "The agent's first response has X, Y, Z. Y is wrong because of [specific reason]. I'm going to push back on Y but accept X and Z."
- "I'm stopping the agent here because the next move would be to commit. But I want to read the diff first. The agent suggested Q changes; I'm going to look at each one."

The junior asks questions. The senior answers. The senior is patient with questions that feel obvious; obvious to a senior is not obvious to a junior.

### Phase B — Senior drives, junior reacts (months 2-4)

The senior runs an agent session, but now the junior is asked to predict:

- "Before I respond to the agent's suggestion, what would you do?"
- "What's wrong with this output? Take a moment."
- "If you were the senior reviewer of this PR, what would you flag?"

The senior then narrates whether they agreed with the junior's prediction and why. This is where calibration happens. The junior learns where their intuition is right (positive reinforcement) and where it's miscalibrated (specific correction).

### Phase C — Junior drives, senior observes (months 4-12)

The junior runs an agent session on real work. The senior watches and lets the junior make decisions, including bad ones (within bounds). After the session, the senior debriefs:

- "You accepted the agent's suggestion at minute 12. I would have pushed back. Here's why."
- "When you re-prompted at minute 22, the prompt was vague. The agent did its best with the ambiguity, but you got more revisions than necessary. Try this phrasing next time."
- "You stopped at the right moment for the right reason. The diff was getting too big. That's the right call."

The senior does NOT take over during the session. The junior must complete the session themselves. Taking over reverts to phase A and the junior never learns to drive.

### Phase D — Junior drives independently, occasional pair-drive (months 12-18)

The junior runs sessions on their own. They reach out to a senior for pair-drive only when:
- They're stuck and want a senior to review the live state
- They're starting a piece of work where they want senior judgment up front
- The session involves a category of work the junior hasn't done before (their first cross-service refactor, their first migration, their first incident-driven hotfix)

This is the steady-state pattern for L3 engineers. They're competent solo; they ask for partnership on the hard stuff.

## What to pair-drive on

Choose work that matters and is real. Not a contrived exercise.

Good targets:
- A real T1 or T2 feature from the backlog
- A real bug investigation
- A real refactor of an existing module
- A real incident response (live, with appropriate caution)
- A real harness contribution (during phase 3)

Bad targets:
- Toy problems
- Advent of Code or LeetCode
- Greenfield "build a new microservice from scratch" exercises
- Anything where the senior has already memorized the answer

The reason: the senior's tacit decisions are most visible on real work where the right answer is genuinely uncertain. Toy problems have known answers; the senior's judgment doesn't surface.

## What the senior actually does

### Narrate the why

The senior should be saying "because X" or "because Y" several times per session. Not "I'm reading this file" but "I'm reading this file because the agent's first prompt would benefit from having this context loaded; otherwise it'll make assumptions about line N that turn out wrong."

The why is the value. Without it, the junior watches mechanical actions and learns mechanical actions.

### Show the dead ends

A real agent session has dead ends — paths the senior took that didn't work, prompts that produced bad output, ideas that the senior abandoned. Don't edit these out. The dead ends are some of the most valuable learning.

A common failure: the senior runs an agent session knowing what they want and produces only the path that works. The junior sees a clean session that doesn't reflect real work. The junior then expects their own sessions to look clean, gets discouraged when they don't, and concludes "I'm not as good as the senior."

The honest senior shows the messy path.

### Push back on the agent visibly

The senior pushes back on the agent during the session. Saying "no, that's wrong because X" out loud, then re-prompting. The junior learns that pushing back is normal, frequent, and grounded in specific reasoning.

A common failure: the senior accepts agent suggestions silently when they're correct and silently discards them when they're wrong. The junior sees only the merge of correct suggestions; doesn't learn the discard pattern.

### Stop and look at the diff

Multiple times per session, the senior should stop and look at what the agent has produced cumulatively. "Let me look at the diff before we proceed." This is one of the most underrated disciplines; juniors who never see a senior do this learn to ship long uninspected agent sessions.

### Show the cost discipline

The senior occasionally checks token cost. "We're at $1.40 on this session; I'd want to wrap this up under $3. Let me think about whether the next move is necessary." Cost is part of the craft; juniors who never see seniors think about cost don't develop the discipline.

## What the junior actually does

### Ask "why?" frequently

Not as a challenge; as a learner. "Why did you push back on that?" "Why did you stop there?" "Why did you accept that one?" The junior who only watches without asking gets the surface; the junior who asks gets the depth.

### Predict before being told

The senior should ask "what would you do?" routinely. The junior should also volunteer predictions: "I think the next move is to..." The act of predicting calibrates intuition faster than passive observation.

### Take notes on patterns

Not on the specifics of the session (those age out fast) but on the patterns: "Senior pushes back when the agent uses APIs the senior didn't load into context. Senior stops to read diff every ~5 agent turns. Senior abandons a path within 2 prompts if it's not working."

The patterns become the junior's playbook.

### Drive the session in phase B onward

The junior should not be a permanent observer. By phase B (month 2-4), the junior is making real decisions in the session, with the senior watching. The transition is uncomfortable; the senior must resist taking over.

## What goes wrong in pair-driving

### The senior takes over mid-session

The junior makes a wrong call; the senior says "let me drive for a minute." This is the cardinal sin. The session reverts to phase A; the junior learns "I'll be saved when it gets hard." The next session, they make less effort because they expect rescue.

The fix: the senior commits to letting the session play out. If the junior makes a wrong call, the senior asks a question ("what's the failure mode of that?") rather than taking the keyboard. After the session, the senior debriefs.

### The senior runs a clean session

The senior pre-thinks the entire session and runs through it without dead ends. The junior sees a smooth path that doesn't match real work. Fix: pick a piece of work the senior hasn't pre-thought.

### The junior asks no questions

The junior watches passively. The session ends; they thank the senior; nothing has transferred. Fix: the senior asks frequent "what would you do" questions; the junior is responsible for at least 5 substantive questions per session.

### The session is canceled or rushed

The senior is busy; the session is shortened from 60 minutes to 15. The 15-minute session is worse than no session because it teaches the junior that pair-driving is decorative. Fix: the senior commits to the 60 minutes or moves the session.

### The senior does the demo session

The senior shows a polished session they've rehearsed, suitable for a conference talk. The junior is impressed and learns nothing. Fix: pair-drive on real, current, uncertain work.

## What this guide will NOT do

- Will not work without senior buy-in. The senior who treats this as a chore produces a chore; the senior who treats it as a craft produces craft.
- Will not work for juniors who don't drive in phase B onward. The transition is critical; passive juniors plateau.
- Will not transfer skills the senior doesn't have. If the senior runs unproductive agent sessions, pair-driving teaches unproductive habits.

## Companion artifacts

- [`18-month-curriculum.md`](18-month-curriculum.md) — pair-driving's role in each phase
- [`manager-1on1-playbook.md`](manager-1on1-playbook.md) — the manager's role in defending pair-driving time
- [`anti-patterns.md`](anti-patterns.md) — anti-patterns 4 (the senior who won't let go) and 5 (mentor by appearance) most directly affect pair-driving
- `skills/code-review/SKILL.md` — adjacent discipline
