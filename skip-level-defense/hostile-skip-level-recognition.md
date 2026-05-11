# Hostile Skip-Level Recognition

The four signals from Ch 61 §61.4 and the conversation script for addressing it.

Most skip-levels are normal. This template is for the small percentage that aren't.

> Most skip-levels are normal. Treat them that way. When one is hostile, recognize it for what it is and respond.
>
> — Ch 61 §61.1

## What hostile skip-levels look like (the four signals)

From Ch 61 §61.4:

1. **The CEO is asking the same question they have already asked you, of multiple of your reports, in multiple forums.**
2. **The CEO is making commitments to your reports that they have not made to you.**
3. **Your reports are reluctant to debrief you on the conversation.**
4. **The CEO is asking for direct access to engineering data that you would normally provide.**

When you see two of those, raise it.

## Distinguishing hostile from normal

Normal skip-levels are how CEOs stay close to the work. They are not the problem. The signals matter when they cluster:

| Signal in isolation | What it usually means | When it's hostile |
|---|---|---|
| CEO talked to your senior engineer | They're curious; learning the work | They're checking on YOU through the engineer |
| CEO asked you the same question twice | They forgot the first answer; or the answer wasn't satisfying | They're asking everyone the same question, looking for inconsistency |
| EM was reluctant to debrief | The conversation was politically awkward | A pattern across multiple EMs |
| CEO asked for direct dashboard access | They want to be self-service | They're going around your interpretation of the data |

A single signal is almost always normal. Two clustered signals is the threshold for the conversation.

## The pre-conversation work

Before the conversation, do three things:

### 1. Verify the pattern

You may be misreading. Run through the four signals carefully. Get a second opinion from your CTO or peer if you have one. Hostile skip-level recognition errors run in both directions — paranoia is also a failure mode.

### 2. Identify what specifically you want to change

The conversation works only if you can name what you want differently. Vague ("I feel undermined") doesn't carry; specific ("commitments to delivery dates should come from me, not from skip-levels") does.

The most common ask: *"AI delivery commitments come from me, not from skip-level conversations."*

Other valid asks:
- "When you have a question for engineering, please come to me first or copy me."
- "When you make a commitment in a conversation with my team, please tell me before I hear it from them."
- "When you want data, I'm happy to provide it; please don't ask my team for it directly."

### 3. Decide what you'll do if the conversation doesn't resolve it

The conversation may not work. The CEO may agree in the moment and continue the pattern. The CEO may push back on your characterization. The CEO may escalate to you ("you're being insecure"). Decide before the conversation:

- What's your line? (Where does this stop being absorbable?)
- What's your escalation path? (CTO if you have one; if the CTO is the source, the CEO themselves; if the CEO is the source, it's the board or your departure.)
- What's your timeline? (How long do you give this before the next move?)

You won't say any of this in the conversation. But you should know it before you walk in.

## The conversation — the script (verbatim)

Per Ch 61 §61.4, the conversation is in person, in a one-on-one, NOT in writing. Don't email this. Don't Slack this.

### The opener

> "[CEO name], I want to raise something I've been seeing. I'm going to be direct, and I want to be clear up front that this isn't an accusation. I'm raising it because I think the current state isn't going to work for either of us if it continues.
>
> I noticed you're talking with [EM name / staff engineer name] about [topic]. I'm happy to support those conversations, brief the team in advance, and help you get what you need. The thing I want to avoid is divergent commitments — you committing to a timeline or a deliverable in those conversations that I haven't agreed to, and then me having to renegotiate later.
>
> Can we agree that AI delivery commitments come from me, not from skip-level conversations?"

The structure:
1. Name what you're seeing without accusation
2. Affirm the legitimacy of the underlying activity (skip-levels are fine)
3. Name the specific thing that's not working (divergent commitments)
4. Ask for a specific change

### What works in this script

- **"This isn't an accusation."** Diffuses the defensive reaction.
- **"I'm happy to support those conversations."** Offers cooperation; signals you're not trying to wall off the team.
- **The specific name of the person.** Not "I've heard you've been talking to my team." A specific name. That's harder to deflect.
- **The specific topic.** Not "various topics." A topic.
- **The ask is small.** "AI delivery commitments come from me." That's a low bar.

### What to NOT do

- **Don't name multiple incidents.** Pick the most recent or most serious. Lists feel like prosecution.
- **Don't name the report's name as the source.** That gets the report in trouble. Frame it as your observation.
- **Don't bring data, screenshots, or written timelines.** This is a conversation, not a case.
- **Don't make it about your authority.** "I run engineering" is technically true and politically expensive. The frame is "we'll have divergent commitments that hurt us both," not "you're stepping on me."

## How CEOs respond — and what to say back

### Response 1: Agreement

> "You're right, I've been doing that. I won't make commitments without you."

This is the easy response. Take it at face value. Confirm:

> "Thanks. To make sure we're aligned: when you talk to [EM] or [staff engineer] going forward, please loop me in before any commitment lands. I'll be responsive. If you want a different cadence — like if I should be doing more proactive briefings — tell me what would be useful."

Then watch the next 4-6 weeks. If the pattern continues despite the agreement, the next conversation is harder.

### Response 2: Disagreement on the facts

> "I haven't been making commitments. We're just talking through the work."

Believe it. The CEO may genuinely not realize they've been making commitments. EMs are loyal and report what they hear; CEOs are casual and don't always realize their casual statements land as commitments.

> "Okay, fair. From where I'm sitting, [EM] came back from your conversation with the impression that we'd committed to [X by Y]. That might be a misread on their end. To prevent that going forward, can we agree that delivery commitments — even casual ones — come from me?"

This re-frames as a process improvement rather than an accusation. Most CEOs accept process improvements that aren't framed as accusations.

### Response 3: Disagreement on the principle

> "I want to talk to your team directly. That's part of how I run the company."

> "Absolutely, you should. Skip-levels are normal and they're useful. The thing I'm asking for is specifically about commitments to delivery — timelines, scope, specific features. The conversation can happen freely; the commitment should come from me. I'm not asking for fewer skip-levels, just for the commitments to be aligned."

If the CEO continues to push back — "I'll commit to whatever I think is right" — the conversation has hit the line. You're now in escalation territory.

### Response 4: Counter-attack

> "You're being insecure. You're trying to control your team's access to me."

This is the worst response, and it's not rare. It's also where you find out who you're working for.

> "I'm not trying to control access. I'm trying to prevent us from making divergent commitments. If you'd prefer to characterize this as insecurity, that's your call. The thing I'd ask you to consider: we're going to keep ending up with mismatched timelines if commitments come from two channels. That's bad for the team and bad for what we're trying to ship.
>
> What I'd like is for delivery commitments to come from me. That's all I'm asking for. Tell me how you'd like to handle this."

If the CEO continues to characterize it as insecurity, you've hit the wall. The conversation is over for now; the next move is escalation or departure.

### Response 5: The shift

> "I've been doing this because I don't trust your timelines. I think you're sandbagging."

This is the most useful negative response. It surfaces the actual issue. The conversation now becomes:

> "That's a real concern; I'd rather you tell me that than route around it. Walk me through the timelines you don't trust. Are you seeing slippage on specific commitments? Is the issue with my projections, or with delivery against them?"

The conversation has moved from "you're going around me" to "let's address the underlying trust issue." That's a much more productive place. It's still hard. But it's solvable.

## Escalation — when the conversation doesn't resolve it

If the conversation produces verbal agreement but the pattern continues for 4-6 weeks: have the conversation again, more directly:

> "We talked about this [N] weeks ago. I'm seeing the same pattern. Specifically, [most recent incident]. I'm raising it again because I told you I would. What's going on?"

If after the second conversation the pattern continues, escalate per Ch 61 §61.5:

> "I cannot effectively run engineering if commitments are being made outside the engineering chain. Either I run engineering, or the commitments come from elsewhere. The current state is not stable."

This is a hard conversation. Have it once, clearly, and follow through. Following through means: if the pattern continues, you escalate to the CTO (if any), or you start preparing your departure with dignity. The book is direct about this:

> The escalation framing: "I cannot effectively run engineering if commitments are being made outside the engineering chain. Either I run engineering, or the commitments come from elsewhere. The current state is not stable."
>
> This is a hard conversation. Have it once, clearly, and follow through.
>
> — Ch 61 §61.5

## What this template will NOT do

- Will not save you in a culture where the CEO has decided to undermine you. The template surfaces and pushes back; if the CEO is determined, the template buys you time but not safety.
- Will not work if you misdiagnose. Treating a normal skip-level as hostile damages the relationship and signals insecurity. Verify the pattern before raising.
- Will not work without the underlying credibility. A leader whose engineering is broadly seen as failing will be told "yes, I have to skip-level you because you're failing." Make the engineering work first; the political defense second.

## What success looks like

The pattern stops within 4-6 weeks. The CEO loops you in on commitments. Skip-levels continue, but they're informational, not parallel-track. Your team's debrief discipline returns to normal.

If you don't see this within 4-6 weeks: you have your answer about the situation, and you should act on it.

## Companion artifacts

- [`brief-your-reports.md`](brief-your-reports.md) — the discipline that minimizes hostile-skip-level damage
- [`README.md`](README.md) — overview of when to use which skip-level template
- Ch 61 — the full chapter
