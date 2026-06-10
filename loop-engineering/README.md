# Loop Engineering

Companion material to *Software Engineering with AI: A Practical Handbook for the Claude Code Era* by Ryan Byrd. Cross-references Ch 6 (skills & the harness), Ch 43.6 (the IC perspective — running five agents at once), and the cost-discipline runbook.

> "You shouldn't be prompting coding agents anymore. You should be designing loops that prompt your agents." — Peter Steinberger *(reported)*
>
> "I don't prompt Claude anymore. I have loops running that prompt Claude and figuring out what to do. My job is to write loops." — Boris Cherny, Claude Code at Anthropic *(reported)*

Loop engineering is the move past running five agents by hand: not prompting the agents at all, but building the small system that prompts them for you — on a timer, without you. It sits one floor above the harness. The harness is the environment a single agent runs inside; the loop runs the harness on a schedule, spawns helpers, and feeds itself.

This is early, genuinely risky on token cost, and easy to do badly. This kit lays out both the shape of it and the ways it bites.

## What's in here

| File | Purpose |
|---|---|
| [`five-building-blocks.md`](five-building-blocks.md) | The five pieces every loop needs (automations, worktrees, skills, connectors, sub-agents) plus the sixth thing — memory. Same capabilities in Claude Code and Codex. |
| [`five-day-plan.md`](five-day-plan.md) | A day-by-day ramp to your first working loop, ending in the one rule that holds the whole thing together. |

## The honest caveat

The loop changes the work; it does not remove you from it. Verification stays on you, your understanding rots if you let it, and the comfortable posture (merge whatever comes back) is the dangerous one. Two people can build the identical loop and get opposite outcomes — one moves faster on work they understand deeply, the other avoids understanding the work at all. The loop can't tell the difference. You can.

> Build the loop. But build it like someone who intends to stay the engineer, not just the person who presses go.
