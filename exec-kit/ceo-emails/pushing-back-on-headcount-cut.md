# Email — Pushing Back on a Headcount Cut

**Use when:** The CEO (or CFO, or board) proposes reducing engineering headcount on the basis that AI tooling will compensate for the lost capacity. This is the highest-stakes email in the kit. Get this conversation right and you preserve the team. Get it wrong and you spend the next year in damage control.

**Do not send if:** You haven't already had a verbal conversation. This email is the written follow-up that puts your position on the record. It is not the first move.

**Tone:** Direct, evidence-based, professional. Not emotional. Not defensive. Offer real alternatives.

**Risk:** This email puts you on record disagreeing with the CEO. That's the point — but it's also a real career exposure. Read it three times before sending. Have your CTO read it if you have one.

---

```
Subject: Re: Q[N] headcount target

[CEO name],

I want to push back, in writing, on the proposal to reduce engineering
headcount by [N]% in Q[N] on the basis that AI tooling will compensate for
the reduced capacity.

The data we have, ours and the industry's:

- Industry studies (DORA 2025, DX Q1 2026, ~135K developers in the DX
  dataset alone) show median PR throughput gains of 8-15% on prepared teams
  with significant harness investment. Our internal data is tracking to that
  range — [specific number from your dashboard]% over the past two quarters.

- The same studies show those gains are partially or fully consumed by
  review time, rework, and incident response on teams without harness
  investment. We've seen this on [specific team] when we went too fast.

- Anthropic's own published guidance is that AI tooling produces force
  multiplication, not substitution. The teams in the public case studies
  that doubled output (none of them mid-size) did so by adding capacity to
  the team, not by reducing it.

The substitution posture — paying for AI tools and reducing headcount — is
coherent and chosen by some companies. If we choose it, the throughput target
needs to come down, not up. The incoherent posture is paying for the tools,
reducing headcount, AND demanding throughput up. I am not willing to commit my
team to that, and I think you would not want me to.

If the budget pressure is real, my preference would be one of:

1. Hold headcount, delay the AI investment by one quarter, pick this up next
   year. Cost-neutral or close to it.

2. Reduce headcount by [smaller N]%, hold the AI investment, be honest with
   the board that throughput will hold flat for the year while we adjust.

3. [If applicable: a third option specific to your situation, e.g. trimming
   contractor spend, deferring a specific project, etc.]

Either of (1) or (2) I can defend in front of the team and the board. The
third option as currently proposed — cuts AND acceleration — I cannot.

Want to talk Friday? I have the dashboard pulled and can walk through what
we're actually seeing.

— [Your name]
```

---

## Before you send

Read this checklist line by line.

- [ ] **Are you sure you want to be on record?** This email is the political artifact. Once sent, it shapes the conversation for months.
- [ ] **Are the numbers in the email real?** If you cite "8-15% throughput gains," that needs to be defensible. Pull the source data.
- [ ] **Are the alternatives genuine?** If options 1 and 2 wouldn't actually work for your business, don't list them as if they would. The CEO will see through it.
- [ ] **Have you told your CTO?** If you have a CTO between you and the CEO, they need to see this draft before it goes. Going around them is its own political crisis.
- [ ] **Is your tone professional?** Re-read for any hint of emotional reaction, sarcasm, or finger-pointing. Strip those out. The data is doing the work; you don't need to add force.

## What success looks like

The conversation that follows this email is uncomfortable but productive. The CEO either agrees to one of your alternatives, or pushes for a fourth option, or escalates. All three are recoverable.

What success does *not* look like: a softer version of the email that doesn't take a position. The cost of taking no position is that the cuts happen anyway and you own the impossible commitment.

## What failure looks like

The CEO ignores the email and proceeds with the original plan. If this happens, you have three options:
1. Comply and document. (Defensible if you also document the predicted outcome and revisit at quarter-end.)
2. Escalate to the board (very rare; usually a CEO-replaceable event).
3. Resign. (Sometimes the right move; not a step to take without significant prior conversation.)

If you find yourself drafting this email and option 3 is on your mind, talk to a peer VP of Engineering at another company first. The "I have to push back on a headcount cut" conversation is one of the most common in mid-size engineering leadership in 2026; you're not alone.

## Related templates

- `defending-the-investment.md` — when the question is whether the investment is paying off, not whether to cut headcount.
- `podcast-clip-reply.md` — when the underlying issue is anxiety, not strategy.
