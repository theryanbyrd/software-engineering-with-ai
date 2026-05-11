# Promotion Conversation Script

The verbatim conversation when a manager talks to an engineer about promotion. Four scenarios:

1. **The promotion conversation when the engineer IS ready** — clean case
2. **The promotion conversation when the engineer is NOT ready** — gap-naming with path forward
3. **The "you've been at this level long enough but not promoting" hard conversation**
4. **The cross-track conversation** — engineer interested in EM, platform, or different track

These are starting scripts. Adapt to the specific person and situation; don't read them like a script.

---

## Scenario 1 — Engineer is ready for promotion

The case for promotion is clear; the calibration committee will support; the conversation is relatively easy.

### Opening (the case for)

> "I want to talk about your level. I'm going to recommend you for promotion to L4 [or whatever level] in the next cycle. Before we go into the details, I want to walk you through the case.
>
> You've been operating at the L4 bar for the last two quarters. Specifically:
>
> - **Scope:** you've owned [specific T2 features end-to-end / specific substantial module]. You've shipped [specific examples] without senior intervention beyond standard review.
>
> - **Direction / Architecture / Evaluation:** your strength is [Direction / Architecture / Evaluation]. You've shown it specifically through [specific work — a spec you wrote, a constraint you encoded, a feedback loop you built]. You have credible competence in the other two — for example, [specific case where the other disciplines showed up].
>
> - **Code review judgment:** you're catching slop signatures other engineers miss. Specifically, [specific PR review where the engineer caught something].
>
> - **Harness contribution:** you've shipped [specific harness component] that's used by [other engineers / teams]. The component is in active use.
>
> - **Mentorship:** you've been the senior partner in pair-driving with [L3 engineers]. They've grown under your guidance.
>
> Calibrating against the L4 rubric, you're there. The promotion would recognize work you've already done."

### Calibration

> "Calibration is real — I won't pretend the committee is a rubber stamp. The committee will look at the case, compare to other engineers being considered, and make the call. From what I've seen, your case is solid. I'll write the packet that captures the work; the calibration committee will see what I see.
>
> Most likely outcome: promotion approved. Possible outcome: deferred a cycle for calibration reasons (e.g., timing relative to other promotions). Unlikely outcome: declined — I don't see a case for that, but I want to be honest that I can't promise."

### What changes (or doesn't)

> "If the promotion goes through:
>
> - Your title changes to [new title]
> - Your compensation moves to the L4 band (your specific number is finalized after the cycle; expect [rough range])
> - The work doesn't change immediately. The promotion recognizes work you're already doing.
> - Over the next 6-12 months, you'll naturally take on more L4-level scope: [specific examples — owning a domain, leading a small initiative, etc.]
>
> What I'd ask of you between now and the promotion taking effect: keep doing what you're doing. The promotion is for sustained operation at the new level; we don't want a sprint to look promotable and then a regression."

### Questions

> "What questions do you have? Comp, timing, scope after promotion — anything is fair."

---

## Scenario 2 — Engineer is NOT ready

The harder conversation. The engineer may believe they're ready; the manager doesn't think so. The discipline is honest, specific, with a path forward.

### Opening (don't bury the answer)

> "I want to talk about your level. You've asked about promotion, and I want to be direct rather than vague.
>
> I'm not going to recommend you for promotion in the next cycle. I'll explain the specific gaps and what would close them.
>
> Before I get into specifics: this is not a 'no, never.' This is 'no, not now, here's the specific work.' Some of what I'm going to say might be uncomfortable; I'd rather say it clearly than have you guess what's going on."

### The named gaps

> "The L4 bar has [N] dimensions. You're meeting [some of them] solidly. The gaps:
>
> **Gap 1: [Specific dimension].** Specifically, [specific evidence — a PR that wasn't ready for the L4 standard, a spec that needed substantial revision, a harness contribution that's not yet there].
>
> **Gap 2: [Specific dimension].** Specifically, [specific evidence].
>
> [If 3+ gaps, the engineer is significantly below the bar; consider whether the conversation should be about pace of growth, not promotion.]
>
> What I'm not saying: 'you have personality issues.' What I am saying: there are specific work outcomes the L4 bar requires that I can name, and we're not seeing them yet."

### The path forward

> "Here's what would close these gaps. I'm offering this as a 6-month plan.
>
> For Gap 1: [specific work — own a particular project end-to-end, lead a specific initiative, ship a particular harness component]. Concrete success criterion: [specific outcome].
>
> For Gap 2: [specific work]. Concrete success criterion: [specific outcome].
>
> If you do this work over the next 6 months and the gaps close, I'll bring you to the next cycle with a strong case. If you do this work and the gaps don't close, we'll have a different conversation about pace and direction."

### Anticipating pushback

The engineer often pushes back. Common patterns and responses:

**"I think I'm doing this work."**

> "Let's get specific. The L4 bar is about sustained operation; I'm not seeing that yet, even if you've done specific instances. Can you walk me through [specific case] from your perspective?"

**"Other engineers got promoted with less work."**

> "I won't compare you to specific people. I'll say: the L4 bar is what it is, and the calibration committee is consistent. If you have specific concerns about fairness, we can talk to HR or to my manager about the calibration process."

**"This feels like moving the goalposts."**

> "It might feel that way. The bar hasn't changed. What's changed is that you're closer to it now than you were 6 months ago, so we're talking about it more specifically. The criteria I named just now are the criteria I would have named 6 months ago."

**"I'm going to look elsewhere."**

> "I understand. If you want to leave, I won't try to stop you. I want you to make the decision with good information. The L4 bar at most companies our size is similar; you might find a place that levels you faster, but you might not. What I can promise is honest conversation here. I won't promise quick promotion to keep you, because that wouldn't be honest."

### Closing

> "I know this isn't the conversation you were hoping for. I respect you enough to be direct rather than vague. Let's talk in 30 days about how the work is going. If anything I said doesn't match your read of the situation, push back — I'd rather have the disagreement than leave it unspoken."

---

## Scenario 3 — Stuck at level for a long time

The engineer has been at the current level for 3+ years. There's no clear path to promotion. The conversation is harder than Scenario 2 because the path forward might not be the next level on this team.

### Opening

> "I want to have an honest conversation about your career here. You've been at L4 for [3-5 years]. We've talked about L5 in the past; the bar hasn't been met. I want to step back from the specific cycle and talk about the broader question of what's next for you.
>
> This isn't a performance conversation. You're delivering well at the L4 bar; that's a meaningful contribution. The conversation is about whether L5 is the right next step and what would move you toward it."

### Possible paths

> "Three honest possibilities:
>
> **Path A: There's specific work that would move you toward L5.** I'd name it specifically; we'd discuss whether it's work you want to take on. If you do, we'd reset the conversation.
>
> **Path B: You're a strong L4 and you might cap there on this team.** That's not a value judgment; it's a calibration about scope and the kinds of work the team has available. Some engineers operate brilliantly at L4 for entire careers; that's a fine outcome.
>
> **Path C: There's a different shape of work that'd move you toward L5 that isn't on this team.** Maybe a role change — moving to platform team, or to a different domain. Maybe a different company where the work and scope let you operate at L5 more naturally.
>
> I want to talk through which of these you think fits, and what you want."

### When the engineer wants Path A

> "Okay. The specific work that would move you toward L5: [specific examples]. I'm going to be honest about whether the team has the work available; sometimes we can scope into it, sometimes we can't.
>
> What I'd commit to: I'll look for opportunities to give you that scope over the next 2 quarters. If by then we haven't found them, we'd revisit this conversation honestly."

### When the engineer wants Path B

> "That's a meaningful choice. Let me make sure we're aligned on what it means: you'd continue at L4 indefinitely, with full recognition that you're delivering value, with the understanding that you're not trying to grow toward L5. Comp continues at L4; equity refreshes at L4 levels.
>
> What you'd get from me: continued real work, real review, real engagement. What I'd ask in return: keep operating at the L4 bar; don't drift down."

### When the engineer wants Path C

> "I support that. Let's talk about whether it's a role change here or a company change. If a role change here would work for you, I can help connect you to the right places — platform team, a different domain. If a company change makes more sense, I'll be supportive — including writing a strong reference if you want one.
>
> I'd rather you find the right next thing than stay here under-leveraged."

---

## Scenario 4 — Cross-track conversation

The engineer is at L4 or L5 and is interested in a different track — engineering management, platform team, security, or another specialization.

### Opening

> "You mentioned you're thinking about [EM track / platform team / different specialization]. I want to talk about it seriously rather than dismiss it or oversell it.
>
> Before I share my view, I want to understand: what's drawing you to it? What's the specific thing you're hoping to get?"

### Listening

The engineer's answer matters. Common patterns:

- **"I want to manage people"** — substantive interest in EM track. Engage with EM ladder.
- **"I want to do less coding"** — usually NOT a good reason to move to EM; EMs do less coding but for the wrong reasons. Push back gently.
- **"I want more leverage"** — could go to EM, platform, or stay IC and grow toward L5/L6. Discuss the options.
- **"I want to work on AI tooling all the time"** — platform team fit. Discuss.
- **"I want to work on [specific domain]"** — internal mobility conversation. Discuss.

### Evaluating fit

> "From what I've seen of your work, [specific reasoning about fit]. The strengths you'd bring: [specific examples]. The areas you'd need to grow: [specific examples].
>
> [If fit is strong:] I think the move would suit you. I can support it.
>
> [If fit is mixed:] I think the move could work but it'd be a substantial growth period. We'd want to scope a runway carefully.
>
> [If fit is weak:] I'm honest that I don't see this as a good fit, and here's why: [specific reasoning]. I'd rather you have this view directly than discover it 6 months in."

### Path forward

> "If we agree this is the right move, here's how to make it real:
>
> - **Internal posting:** [specific timing — typically next open role on the target team]
> - **Trial period:** [some companies allow a 3-6 month trial; others require formal transfer]
> - **Calibration:** [where you'd land on the new ladder; comp implications if any]
> - **Backfill:** [your current role would need backfill; expect 2-3 month lag]
>
> If we don't agree, I want to be honest about why and stay supportive of your career here in your current role."

---

## Cross-cutting principles for these conversations

### Be specific

Vague feedback ("you need to grow") is the worst kind. Specific feedback ("you need to ship a harness component used by other teams; specifically, here are 3 candidate components") is honoring the engineer's intelligence.

### Don't bury the answer

If the engineer asked about promotion and the answer is no, say no in the first 90 seconds. Don't lead with 10 minutes of positive context that suggests yes. The engineer will feel bait-and-switched.

### Hold the line

Engineers will push back. Some will be persuasive. The rubric is the rubric; if you cave under pressure, the rubric is decorative. Calibration committees exist partly to depersonalize this — "the rubric requires X, the committee requires X."

### Honor the relationship

These conversations affect careers. The engineer may remember this conversation for years. Be honest, be specific, be kind. Don't be vague to avoid discomfort.

### Document

After every promotion conversation, the manager writes a brief note: who, when, what was said, what's the path forward. This survives manager transitions; the next manager doesn't restart the conversation from zero.

## What these scripts will NOT do

- Will not work as a literal recital. Adapt.
- Will not eliminate the difficulty of these conversations. They're hard for good reasons.
- Will not work in a culture where the rubric is overridden routinely. The conversation depends on the rubric being real.
- Will not work without manager skill. New managers will need practice; pair with their manager for the first few.

## Companion artifacts

- [`level-rubric.md`](level-rubric.md) — the criteria the conversation references
- [`ai-tooling-fluency-by-level.md`](ai-tooling-fluency-by-level.md) — the specific dimension
- [`promotion-packet-template.md`](promotion-packet-template.md) — what the manager produces for the committee
- [`calibration-committee-structure.md`](calibration-committee-structure.md) — what happens after the conversation
- `junior-trajectory/manager-1on1-playbook.md` — adjacent (1:1 cadence)
