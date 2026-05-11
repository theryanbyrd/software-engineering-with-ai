# Senior Software Engineer (AI-Native)

**Job description template** — adapt to your company's voice, location, and benefits stack. Sections marked `[REPLACE]` need company-specific content. Sections marked `[KEEP]` should remain substantively as-written; they encode signals that have proven predictive in 2026 hiring.

---

## About the role

[REPLACE — 2-3 sentences about the team, the product, the mission]

We're hiring a Senior Software Engineer who is fluent with AI engineering tooling and can operate at the new bottleneck disciplines: Direction, Architecture, and Evaluation. You'll ship product features end-to-end, contribute to the team's harness (skills, hooks, subagents), and review the work of more junior engineers — including AI-authored work.

## What you'll do [KEEP — adapt to your stack]

- Ship features end-to-end on [REPLACE — your stack/product]. Some days you'll be writing code directly; some days you'll be orchestrating AI agents with a clear specification, careful verification, and judicious review.
- Contribute to the team's AI engineering harness: skills, subagents, hooks, CLAUDE.md, AGENTS.md, the verify command. The bar is "another team can use what you shipped without you in the room."
- Review pull requests — including AI-authored ones — with the discipline to spot the seven slop signatures (Ch 22 of [_Software Engineering with AI_](https://www.linkedin.com/in/ryanbyrd) is required reading by month two).
- Write specifications that an AI agent can execute against. Specifications that produce slop on first attempt are not the agent's fault; they are the spec author's.
- Mentor more junior engineers through the new craft: when to delegate to an agent, when to write the code yourself, how to know the difference.
- Carry your share of on-call, incident response, and operational work. Use AI tooling where it accelerates these; do not delegate judgment.

## What we're looking for [KEEP]

**Required:**

- 5+ years of professional software engineering experience
- Demonstrable experience using AI engineering tools (Claude Code, Cursor, Copilot, Codex, or equivalent) on production code, not just side projects
- Strong code review intuition. You can read a 200-line diff and identify the parts that look right but aren't.
- Specification clarity. You can write an agent-ready issue from scratch in 15 minutes — knowing what the model needs and what it doesn't.
- System-level reasoning. You think about boundaries, contracts, and failure modes, not just functions.
- Skepticism without cynicism. You trust agent output the way you trust a junior engineer's output: read it, verify, push back when wrong, accept when right.

**Preferred:**

- Experience contributing to a team's harness (a skill, a hook, a subagent, a CI integration). One worked example is more interesting to us than five years of "AI-curious."
- Depth in one of: Direction (deciding what to build and what good feels like), Architecture (encoding constraints into hooks, lints, contracts), or Evaluation (the feedback loop that lets us learn whether we're delivering). Credible competence in the other two.
- Experience reviewing AI-authored code in production — and pushing back when it was wrong.
- Background in [REPLACE — domain expertise relevant to your product].

**Things that are NOT requirements:**

- Strong LeetCode/algorithm skills. We do not interview on these for senior engineers anymore. (Ch 60 §60.5)
- "Self-described AI fluency." We're hiring for demonstrated experience, not vibe.
- A specific AI tool. We use [REPLACE — your stack], but if you're fluent with another major tool the transition is days, not months.
- AI/ML model training experience. This role is about USING AI tools to build production software, not about training models.

## Compensation and benefits [REPLACE]

[Salary range, equity, benefits — be specific. The handbook recommends 10-20% premium at senior tier for engineers with credible AI tooling experience (Ch 60 §60.2). If your bands haven't moved, this is the reason you've been losing seniors.]

## Interview process [KEEP]

We've redesigned our interview process around the signals that predict success in this role:

1. **30-minute introductory call** with the hiring manager. Mutual fit, role context, your questions.
2. **Take-home or async PR review exercise** (~90 minutes of your time, on your own schedule). We give you a real PR — sometimes from this codebase, sometimes from a public open-source project — and ask you to review it. We're looking for what you catch and what you let slide.
3. **Architecture-with-AI conversation** (60 minutes). A whiteboard discussion of a system design problem where you can use AI tooling as a thinking partner during the conversation, not just before. We want to see how you think AND how you collaborate with the agent.
4. **Harness component conversation** (45 minutes). Tell us about a hook, skill, subagent, or harness component you shipped. What problem did it solve? What were the trade-offs? What would you do differently now?
5. **Team interviews** (3 × 45 minutes). Two engineers and one cross-functional partner.
6. **Reference checks.**

We do not have a coding round in the LeetCode style. The PR review exercise is our primary signal that you can read and reason about real code.

## What we will NOT do [KEEP]

- We will not ask you to solve a 45-minute algorithm problem at a whiteboard. The signal correlation with senior engineering performance has degraded; we've replaced it.
- We will not ask you to do a full system design from scratch in 60 minutes. Real systems aren't designed that way; the architecture conversation is collaborative.
- We will not ghost you. If you reach the team-interview stage, you'll get a yes, no, or specific feedback within 5 business days.
- We will not require you to use any specific AI tool during interviews. We may ask which tool you'd reach for and why; we'll accept any answer that shows judgment.

## Application

[REPLACE — application instructions, contact, etc.]

We particularly welcome applications from engineers who have been doing this work but don't have a personal brand around it. The market is full of "AI thought leaders"; we're hiring engineers.

---

## For the recruiter / hiring manager

This template encodes the hiring updates from Chapter 60 §60.5 of _Software Engineering with AI_:

- "Stop using LeetCode-style algorithm interviews as the sole signal for senior engineers."
- "Add a real PR review exercise."
- "Add an architecture-with-AI conversation."
- "Add a 'tell me about a recent harness component you shipped' question."

The "5+ years" floor and the rejection of the LeetCode signal are the two most consequential changes from a typical 2024 senior JD. Both are deliberate.

If your candidate funnel has been heavily algorithm-screened in the past, expect the first round of applications to a JD using these signals to look "weaker" than what you're used to. That's because the old signal was selecting on the wrong thing. Calibrate by running the PR review exercise on a few candidates from BOTH funnels (algorithm-strong and harness-strong); the harness-strong cohort tends to perform better on the new exercises.
