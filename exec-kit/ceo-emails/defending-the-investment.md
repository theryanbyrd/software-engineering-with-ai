# Email — Defending the AI Investment

**Use when:** The CEO asks (in a one-on-one, in Slack, in passing) whether the AI tooling investment is paying off. The question often comes after they've seen a competitor's announcement, an analyst report, or a podcast. The honest answer requires data; this template anchors the conversation in the data you have.

**Do not send if:** You don't actually have the dashboard. The whole point of this email is that the numbers are real. If you're guessing, write the dashboard first.

**Tone:** Direct, specific, honest about gaps. Not defensive.

**Cadence:** Quarterly minimum. If the CEO is asking, the answer is probably "I should have sent this last month."

---

```
Subject: AI tooling investment — Q[N] review

[CEO name],

Following up on our conversation [day] about whether the AI tooling investment
is paying off. Three things to share.

First: spend. Token spend tracked to $[X] this quarter against the budget of
$[Y]. Per-developer median is $[Z]/week, well below the per-seat ceiling we set.
Variance from forecast is [+/-N%], driven by [specific cause: more adoption
than expected / one team running batch summaries / model-mix shift to more
Sonnet usage].

Second: throughput metrics. Median lead time on tier-2 tickets dropped from
[N] days to [M] days — a [P]% improvement. PR review time per merged PR is
[up/down by Q%] (we expected this to rise during harness build-out as the AI
reviewer subagent matures; tracking to fall by Q3).

Third: where we are not seeing gains. Tier-3 architectural work — the kind
that shows up most visibly in your week — has not accelerated. This is
consistent with industry data; AI is amplifying the work we delegate to it,
not the work we still own ourselves. The system design conversations, the
trade-off decisions, the customer-facing technical strategy: those still take
the same time they always did.

The investment is paying off in the work we expected it to pay off in. The
pieces of your week that I think you're noticing have not changed — and on
the current evidence, will not change in the next two quarters — because that
work is on us.

Happy to walk through the dashboard if useful. Linked: [dashboard URL].

— [Your name]
```

---

## Customization checklist

Before you send, replace:

- [ ] `[N]` with the quarter number
- [ ] `[X]`, `[Y]`, `[Z]` with actual spend numbers from the cost dashboard
- [ ] `[N] days`, `[M] days`, `[P]%` with actual lead-time numbers
- [ ] `[Q]%` with PR review time delta
- [ ] `[specific cause]` with the real driver of variance
- [ ] `[dashboard URL]` with a link the CEO can actually open

## What to do if the numbers are bad

Don't soften the email. If lead time hasn't moved or has gotten worse, say so plainly and explain why (harness gaps, pilot team's domain, ramp time). The CEO can handle bad news. They cannot handle hedged news that turns out to be bad three months later.

If the gap is large, this email becomes the renegotiation conversation (Chapter 57 §57.4). Pivot to: "I committed to X. The current trajectory is Y, and the gap is real. Three things drive the gap: [specific causes]. To close the gap, I would need [specific investments]. Alternatively, I can adjust the commitment to Y' which is well-supported by the current evidence. Which direction would you prefer?"

## When NOT to send this email

- Within 60 days of starting the rollout. The data is not stable enough yet.
- After a single bad week. Use month-over-month or quarter-over-quarter trends.
- In response to an 11pm podcast clip. That gets a different reply (see `podcast-clip-reply.md`).
