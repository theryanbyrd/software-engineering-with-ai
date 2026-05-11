# The First Conversation with Leadership

The conversation that resets expectations from "AI will modernize this codebase by Q4" to "we'll bring 1-2 services to MVH Level 2-3 in 90 days." This is the most important conversation in the brownfield onboarding program.

The book's framing:

> The teams that try to compress this end up with the worst of both worlds: slop in legacy code with no safety net.
>
> — Ch 11 §11.6

If leadership has expectations calibrated by vendor demos rather than by Ch 11's reality, every other piece of the program will be sacrificed. The honest conversation up front prevents the rolling sacrifice.

## When to have this conversation

- **Day 1-7 of inheriting the codebase.** Before commitments accumulate.
- **Before any planning conversation about modernization timeline.** Reset the framing first.
- **When a new VP or CTO comes in with modernization expectations.** Repeat the conversation.
- **When the timeline is being pressured.** Don't wait until you're missing milestones; recalibrate when the pressure starts.

## When NOT to have this conversation

- When leadership is already calibrated. Don't over-explain.
- When you don't have data yet. The conversation is more credible after Phase A (Days 0-30) when you've actually scoped the codebase.
- In a hostile political situation where the conversation will be used against you. Get more credibility first.

---

## The conversation structure

### Opening (90 seconds)

> "Before we plan this out, I want to make sure we're aligned on what's realistic. I'd rather have an uncomfortable conversation up front than slip a quarter and surprise you.
>
> The honest read on brownfield work in 2026: the AI tooling is genuinely useful here, but not the way the vendor demos suggest. Modern AI works beautifully on clean, well-typed, well-tested codebases. It's a hazard on old enterprise systems unless we've prepared the codebase for it. The preparation work isn't optional and it isn't fast.
>
> What I want to walk you through: what realistic looks like, what the path looks like, and what the risk is if we try to compress."

### What realistic looks like

> "The realistic timeline for this codebase is roughly:
>
> - **First 90 days:** one or two specific services brought to a state where AI tooling can be used safely on them. Specifically: characterization tests, working verify command, named owner, documentation that didn't exist before.
> - **First six months:** harness in production use on three to five services. Team comfortable with brownfield-specific patterns. First strangler-fig new module shipped.
> - **First year:** harness covers the highest-risk services. Team has stable practices. Modernization of specific high-pain modules underway.
> - **18-24 months:** the codebase is meaningfully different. Most services are AI-tooling-ready. Modernization is in progress for the modules that warrant it.
>
> What 'modernized' looks like in 24 months is not 'rewritten in a modern stack.' It's 'safe to touch under AI assistance, with characterization tests, with named owners, with the highest-risk modules either bridged or being strangled by new functionality.'
>
> Some modules will still be legacy in 24 months. That's fine. The point is they're under harness, not that they've been rewritten."

### What the path looks like

> "The discipline is from Chapter 11 of [Ryan Byrd's book on AI in software engineering] — happy to share, but the short version is:
>
> 1. **Characterize first, refactor second.** Before changing any module's behavior, we capture the current behavior in tests. The AI agent writes the characterization tests. This is the canonical use case for AI in legacy code.
> 2. **Strangler-fig over rewrite.** New functionality goes in new modules with modern discipline; old modules stay as-is until they can be deprecated. Big rewrites are almost always wrong.
> 3. **Strict autonomy ceiling on legacy.** Agents at L1 (suggest) or L2 (single-file edit with mandatory review) only on legacy modules. Higher autonomy is greenfield work; legacy needs the safety rails.
>
> What I'm asking for from you:
>
> - Air cover on the 9-12 month timeline. Not 'modernization in a quarter' messaging.
> - Tolerance for unglamorous early work. The first 30 days produce no shipped features; they produce understanding and a tracker.
> - Willingness to let me say no to the next 'AI will fix this' pitch. Some of those pitches are right; most aren't.
> - In return, I commit to honest progress reports — not vendor-demo-shaped progress, real progress on the metrics that matter."

### What the risk is

> "If we try to compress, here's what happens — I've seen this at multiple companies:
>
> - The team uses AI tooling on legacy code without the harness. AI generates code confidently. Tests pass because the test suite is sparse. Bugs ship to production. Some are caught fast; some show up six weeks later in customer escalations.
> - The team starts treating AI tooling as untrustworthy. The benefit goes negative. Senior engineers stop using AI on legacy because they've seen it break things.
> - The 'modernization' narrative becomes embarrassing. Leadership starts asking 'why aren't we faster?' The team responds with bigger AI investments that don't fix the underlying issue.
> - Eventually someone proposes a rewrite. The rewrite takes 18 months and produces a system with the old bugs and new bugs.
>
> The compress-the-timeline path doesn't get to modernization faster; it gets to a worse place slower. The honest path is the faster path."

### Asking for the commitment

> "Three specific things I'd ask you to commit to today:
>
> 1. **The 90-day plan I'll write at Day 30 will define realistic outcomes.** When I bring it to you, the conversation will be 'is this realistic?' not 'can you do more?'
> 2. **No public modernization timelines I haven't agreed to.** If the board, an investor, or a customer is going to be told something about timeline, I want to be in that conversation first.
> 3. **Leadership backs the discipline when it's hard.** When we're in month 4 and someone is pushing for visible feature delivery, leadership says 'we're characterizing first; that's what we agreed to.'
>
> What I'll commit to in return:
>
> 1. **Honest weekly status.** Real progress against the plan, in plain language.
> 2. **No surprises at quarter-end.** If we're going to slip, you'll know at week 4, not week 12.
> 3. **Visible wins where possible.** Some of the characterization work surfaces fixes that ship; I'll communicate those clearly when they happen.
>
> Does this work?"

---

## When the conversation goes well

The leader engages on substance. They might push back on specific points (timeline, scope, metrics) but they're working with you on calibration, not against you on framing.

Indicators:
- "Walk me through what 'characterize' means in practice"
- "How do I know we're on track at week 6?"
- "What if [specific business pressure] requires us to move faster on [specific module]?"

These are good questions. Engage with them substantively.

## When the conversation goes poorly

The leader doesn't engage on substance. They might:
- Dismiss the timeline as overly conservative ("We have AI now; this should be faster")
- Refuse the commitments ("I can't tell the board it's a year")
- Reframe your honesty as lack of ambition ("Other teams modernize faster")

How to respond:

### "We have AI now; this should be faster"

> "AI is the reason the timeline is 9-12 months instead of 24-36 months. Pre-AI, brownfield modernization at this scale was a 2-3 year program. AI compresses it. It does not compress it to a quarter. The vendor demos that suggest a quarter aren't operating on real legacy codebases; they're operating on cleaned-up examples.
>
> What I'd ask: walk me through the specific result you're targeting. If I understand the goal, I can show you what part is realistic and what part isn't."

### "I can't tell the board it's a year"

> "Then we have a different problem than scoping this work. The board has to be told something true; if 'a year' is unsayable, what's actually being committed to elsewhere? Let's work backward from what's been committed to and decide what's possible.
>
> Sometimes the answer is: the board has been over-promised. Better to recalibrate now than to miss in Q3 and recalibrate then with worse credibility."

### "Other teams modernize faster"

> "Some teams report faster timelines. Most of those reports don't survive scrutiny — they're either earlier-stage codebases, smaller scope, or selective reporting. The honest empirical work I've seen on AI-assisted brownfield modernization shows median timelines in the 9-12 month range for one or two services to come fully under harness.
>
> If you have a specific reference point, I'd love to look at it. Sometimes the comparison is informative; sometimes it's not."

### Outright refusal to engage

If the leader refuses to engage with the realistic timeline, you have a problem that's bigger than this conversation. The choices:

1. Try again in 2-3 weeks, with more data from Phase A
2. Find an ally (peer leader, the leader's leader) who can carry the framing
3. Document the disagreement in writing for your own record
4. Consider whether the role is sustainable in this culture

This isn't an outcome the conversation script can fix. Don't pretend you've reached agreement when you haven't.

---

## The follow-up cadence

After the initial conversation, the discipline:

### Weekly (the 5-minute check-in)

> "Quick status: this week we [specific accomplishment]. Next week we'll [specific plan]. Risks: [if any]. No timeline change."

If the timeline IS at risk, the message is different:

> "Quick status: I want to flag a risk to the 90-day timeline. Specifically [thing]. Here's what I want to do about it: [proposal]. Want to discuss?"

### Monthly (the longer review)

- Module status tracker walkthrough
- Specific wins (and what they cost)
- Specific gaps (and what they would cost to close)
- Forward look at next 30 days

### Quarterly (the calibration)

- 90-day retrospective
- Realistic next-90-day plan
- Adjustments to the 12-month and 24-month outlook
- Leadership ask: any changes in priority or constraint

---

## What this conversation will NOT do

- Will not work without leadership willing to engage with substance. Some leaders won't, and that's a different problem.
- Will not work as a one-time conversation. The recalibration is a discipline, not an event.
- Will not work without your own credibility. New engineers without track record have a harder time having this conversation; pair with a more senior peer if needed.
- Will not work if the team has already spent 6 months pretending the timeline was 3. Reset honestly; the credibility recovery takes time.

## Companion artifacts

- [`30-60-90-day-plan.md`](30-60-90-day-plan.md) — what you're committing to deliver
- [`characterize-rewrite-leave-alone-rubric.md`](characterize-rewrite-leave-alone-rubric.md) — what the work consists of
- `skip-level-defense/productivity-plateau-message.md` — adjacent template for ongoing leadership conversations
- `skip-level-defense/no-the-model-release-didnt-change-our-strategy.md` — when leadership wants to pivot mid-program
- Ch 11 — source
