# Brief Your Reports — Pre-Skip-Level Discipline

When you know a skip-level is coming, you brief your reports. This template covers the structure of the briefing, what to say, what NOT to say, and the debrief discipline.

The book's framing:

> Most engineering managers and senior engineers are loyal but unprepared. Preparation is your job.
>
> — Ch 61 §61.2

The ICs and EMs going into a skip-level want to do well. They are not going to lie for you. They are going to answer questions honestly. Your job is to make sure that "honest" and "consistent" are the same thing.

## When to use this template

- A skip-level is scheduled
- You suspect a skip-level may happen even if not announced (CEO has been talking to your team informally)
- A board member is doing engineering deep-dives
- A new CTO is doing org listening tours

## When NOT to use this template

- Routine 1:1s between your reports and their managers (different conversation)
- Performance management conversations (different domain)
- Customer-facing technical conversations (your reports are usually fine to handle these unbriefed)

## The pre-skip-level briefing — structure

Per Ch 52 §52.6, the briefing has two parts: what to say and what NOT to say. This template adds a third: what to OBSERVE.

### Schedule

- **Briefing time:** 15-20 minutes, 1-2 days before the skip-level
- **Format:** in-person or video, not email or Slack (you want to read their reaction)
- **Follow-up:** debrief within 24 hours of the skip-level

### Part 1 — What to say (verbatim from Ch 52 §52.6)

> "Here's what I'd ask you to lead with if [CEO/board member] asks about the AI program:
>
> 1. **The posture.** One sentence. 'We're at [stage] of the AI program; we've made [progress]; we're [tracking / behind / ahead] of the plan.'
> 2. **The investment number.** One sentence. 'We're spending $[N] on tooling and $[M] on platform headcount; the breakdown is in [your name]'s dashboard.'
> 3. **The pilot status.** One sentence. 'The [pilot/rollout/migration] is [in progress / completing / wrapping up]; the next milestone is [date].'
> 4. **The handoff.** Full stop. '[Your name] has the dashboard if you want to see it.'"

This four-sentence answer is the safe foundation. It's truthful, it's complete enough for most contexts, and it routes detailed questions back to you without being evasive.

### Part 2 — What NOT to say

The four categories from Ch 52 §52.6:

- **Internal pilot frustrations.** "The platform team has been struggling to ship the harness on time" is a true statement that hurts you in a CEO conversation. The right framing for the same fact: "the platform team is actively building the harness; the next deliverable is X by Y."
- **Comp or headcount conversations.** Engineers don't have full visibility into comp negotiations or headcount planning. They should not speculate.
- **Tooling preferences.** "I personally prefer Cursor to Claude Code" is a fine thing to say in a 1:1 with you. It is a bad thing to say to a CEO, who will hear "the team isn't bought in to the tool we standardized on."
- **Estimates of how much faster the team is moving.** This is the worst one. Engineers will give a number; the CEO will remember it; you'll be held to it. Steer engineers away from quantifying productivity in skip-levels. The dashboard is the place for productivity numbers.

The phrasing for the briefing:

> "Three things to specifically not get drawn into. One — internal frustrations about the rollout. They're real and we're working on them, but in the room they sound like 'this isn't working.' Steer to 'we're actively addressing X.'
>
> Two — comp and headcount. You don't have the full picture; speculation here is dangerous. If asked, say 'I'd defer to [your name] on that.'
>
> Three — productivity numbers. Don't quantify how much faster the team is moving. The CEO will hold us to whatever number lands. If asked, say 'the dashboard has the trend data.'
>
> If you find yourself asked something you're not sure how to answer, say: 'That's a good question; I'd want to think about it carefully. Let me come back to you with a thoughtful answer.' That's a perfectly fine answer; CEOs don't expect ICs to have every answer instantly."

### Part 3 — What to observe

Ask the report to notice:

> "Three things I'd love you to pay attention to during the conversation. They'll help us debrief well.
>
> 1. **Did they ask a question that surprised you?** Tells me what they're thinking about that I might not know.
> 2. **Did they make any commitments?** Like 'we'll do X by Y' or 'we'll figure out Z.' I want to know about every one.
> 3. **What was the energy?** Frustrated, curious, supportive, neutral. Vibe matters more than words sometimes.
>
> Doesn't have to be perfect notes. Just what you remember."

## The debrief — within 24 hours

The debrief is the second half of the discipline. If you brief but don't debrief, you'll be surprised by commitments you didn't know about.

### Schedule

- **Debrief time:** 15-30 minutes, ideally same day or next morning
- **Format:** in-person or video, never written-only
- **Frame:** "Tell me about the conversation" — open, not interrogative

### The questions to ask

> "1. What did they ask you that you weren't expecting?
> 2. Did anything they say sound like a commitment? Even a casual one.
> 3. Was there a moment where they pushed back on something we said? Or where you felt unsure?
> 4. What was the overall energy like?
> 5. Anything else I should know that doesn't fit those questions?"

The fifth question is the most important. It's where things you didn't know to ask about come up.

### What to do with the debrief

- **Note any commitments the CEO made.** These are now things you have to deliver against (or renegotiate). Don't pretend they weren't said.
- **Note any divergence between what the CEO said to your report and what they've said to you.** Pattern over multiple skip-levels = the four signals from [`hostile-skip-level-recognition.md`](hostile-skip-level-recognition.md).
- **Flag anything that surprised the report.** Often a CEO is thinking about something you didn't know they were thinking about. The report's surprise is your signal.
- **Don't create paperwork.** A note in your private log is fine. A formal write-up creates the impression you're tracking everything, which spooks reports.

## The "I don't want to know about it" trap

From Ch 61 §61.3:

> A specific failure mode: the CEO tells your engineering managers something, the EM does not relay it, and you find out from a third party two weeks later. This usually happens because the EM correctly assesses that the message was political and chose to stay out of it.

Address this in the briefing, before the skip-level happens:

> "One last thing. Sometimes in these conversations, [CEO] will say something that feels political — like a critique of me, or a comparison to other teams, or a 'between us' kind of comment. I want to specifically tell you: please tell me about those. I will not punish the messenger. The information matters, and political messages are exactly the ones I need to know about.
>
> If you don't tell me, I'll find out from someone else two weeks later, and at that point I have less ability to address whatever it was. Better that I hear it from you."

This explicitly inverts the EM's natural instinct (stay out of politics). Without it, the EM will sometimes correctly read "this was political" and will stay quiet, and you'll be blindsided.

## The hardest part: when the report says something they shouldn't have

Sometimes the debrief reveals that the report quantified productivity, or vented about the harness, or shared a tooling preference. The temptation is to be frustrated with them. Don't.

The right response:

> "Thanks for telling me. That's not the message I wanted in the room, but it's not on you — I should have prepped you better on that specific question. Going forward, if [topic] comes up, the framing is [X]. If you're not sure how to answer something, the safe answer is 'I'd defer to [your name] on that.'"

Two things this does:

1. **Owns your half of the failure.** You didn't prep them well enough. That's true even if you also wish they'd handled it differently.
2. **Gives them the language for next time.** Without it, the same thing will happen again.

The report comes out of the debrief feeling supported, not punished, and they're more likely to debrief honestly next time. That's the durable position.

## What this template will NOT do

- Will not work if your reports don't trust you. The brief-and-debrief discipline depends on the report being willing to share what they heard. If the relationship is strained, fix that first.
- Will not work if your reports are inexperienced. New EMs and recently-promoted senior ICs will sometimes panic in skip-levels regardless of the briefing. Build their confidence over time; for the first few skip-levels, accept some chaos.
- Will not work as a one-time discipline. This is a habit. The first 2-3 skip-levels with a new CEO are the calibration period. After that, the discipline is muscle memory.

## Companion artifacts

- [`hostile-skip-level-recognition.md`](hostile-skip-level-recognition.md) — when the brief-and-debrief discipline starts surfacing patterns
- [`six-metric-dashboard-explainer.md`](six-metric-dashboard-explainer.md) — what your report should hand back to you (literally) when asked for productivity numbers
- Ch 52 §52.6 — the source for the briefing structure
- Ch 61 §61.2 — the source for the discipline
