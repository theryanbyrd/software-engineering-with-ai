# The CFO who capped token spend mid-quarter

## Setting

A 90-engineer B2B company, US-based. The AI tooling rollout had been running for two quarters. Token spend was growing month-over-month as adoption climbed, but well within the budget the CFO had originally approved.

## Situation

In a routine budget review, the CFO saw the AI-tooling line item. The number was higher than the previous month, and higher than the CFO's mental model of what the line item should be. Without consulting Engineering, the CFO sent a memo: token spend capped at the prior month's number, effective immediately, mid-quarter.

The memo went out on a Wednesday. By Friday, the engineering organization was in a quiet panic.

## What happened

30% of engineers had been on track to exceed the cap by month-end based on their current usage patterns. The cap forced rationing.

Engineers self-rationed in the way you'd expect: they switched to free-tier ChatGPT for work that didn't strictly require Claude Enterprise. Some switched to personal accounts to avoid hitting the cap on their team's allocation. A few stopped using AI tooling for some categories of work entirely.

The data classification policy — carefully constructed over several months, with clear rules about what code could and couldn't be sent to vendors without a BAA — was now being honored intermittently. Not because anyone wanted to violate it, but because the cap created a pressure to get work done that the policy hadn't planned for.

Within ten days, the policy was unenforceable in practice. The VP of Engineering didn't notice for three weeks because nobody wanted to surface the problem — every engineer doing it knew it was technically a policy violation, even if the spirit was understandable.

## What they did

When the VP did learn what was happening, the response was a cost-dashboard re-do. Specifically:

- A spend-by-team breakdown that the CFO didn't have when the original cap was imposed. Half the spend was concentrated in two teams with high tier-3 architectural work; the other 88 engineers were well within any reasonable per-engineer budget.
- A productivity-tradeoff model showing what each rationing level cost. Cutting spend by 30% would have reduced output on the affected teams by an estimated 12-18%; the cap had implicitly imposed exactly this.
- A revised budget with **quarterly approval and monthly review**, rather than month-by-month reactive caps. Engineering committed to the dashboard; the CFO committed to not changing the cap mid-cycle without an explicit conversation.

The VP also opened a side conversation with the CFO about the data classification policy: the cap had inadvertently created a security incident risk. The CFO had not understood that "engineers will just route the work somewhere else" was the predictable outcome of a hard cap.

## Outcome

The cap was lifted. Spend stabilized at slightly above the prior trajectory because the team re-routed work back to the approved tools. The new monthly review process held: when usage spiked in months when there was a real reason for it, Engineering pre-flagged the spike to the CFO with a one-paragraph explanation, and there was no further reactive capping.

Six months later, spend was running 8% under the approved budget because the dashboard surfaced over-rotation patterns early enough to coach. The dashboard turned out to be a better cost-control mechanism than the cap had been.

## Lesson

**Surprise budget caps don't reduce spend; they push it underground.** Engineering teams will find a way to do their work, and the way they find may be worse than the spend the cap was trying to control — for security, for compliance, for productivity, for trust.

**Renegotiate the budget process, not the budget itself.** The CFO's original concern — that AI tooling spend was running ahead of his mental model — was legitimate. The fix was not a hard cap; it was a dashboard that gave the CFO visibility, and a process that gave Engineering predictability. (See chapter 58 §58.4 of the handbook on this.)

## What would have prevented it

A monthly cost-review meeting that included Engineering before the spend became a surprise to the CFO. The dashboard the team built post-incident could have existed from month one. The cost of building it: about a week of platform-team time. The cost of not having it: a quarter of unenforceable policy and several conversations that strained the Engineering-Finance relationship.

Second prevention: an explicit pre-agreed protocol for "what if usage exceeds the budget" that named softer levers before harder ones — coaching the over-using teams, model-routing changes (Sonnet → Haiku for trivial work), explicit team-level allocations — rather than a single across-the-board cap as the only available response.

---

**Source:** Appendix L §L.8 of _Software Engineering with AI_ by Ryan Byrd
**Submitted:** May 2026
