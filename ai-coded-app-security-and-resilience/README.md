# AI-Coded App: Security & Resilience Gaps

Companion material to *Software Engineering with AI: A Practical Handbook for the Claude Code Era* by Ryan Byrd. Cross-references Ch 2 (the seven slop signatures), Ch 35 (Sandbox Reference Architecture), Ch 36 (Security Controls), and the Ch 47.6 worked example.

The book's security chapters are mostly about securing **the agent** — its runtime, the secrets it can read, the injected text it might obey. This kit is about the opposite surface: the security and resilience defects an agent quietly bakes into **the application it builds for you**. The agent is good at producing an app that demos perfectly and is structurally unsafe in ways the demo never reveals.

The pattern underneath all of these is the one named in Ch 2 §2.1a: the agent optimizes for the task you stated ("make the feature work"), not the task you meant ("make it safe when a bot finds it at 3 a.m."). Security and resilience live in that gap, and the agent fills the gap with a confident guess every time. None of these defects are exotic — they're the boring, repeated ones, and they share a tell: the code works on the happy path, so nothing in the normal development loop ever surfaces them.

## What's in here

| File | Purpose |
|---|---|
| [`security-and-resilience-checklist.md`](security-and-resilience-checklist.md) | Paste-ready review checklist for any AI-built app — frontend secrets, RLS, rate limits, silent failures, offline/throttled networks. |
| [`verification-gates.md`](verification-gates.md) | The tests and hooks that turn each defect class into a gate the agent cannot pass. Encode these as constraints, not hopes. |

## The one idea

Asking the agent to "be more careful" catches none of these. Structure the team owns catches all of them. A hope is a sentence in a prompt the next session forgets; a constraint is a hook, a test, or a checklist item that runs every time regardless of who or what wrote the code. Wire the gates in [`verification-gates.md`](verification-gates.md) into CI and the agent's blind spots stop being your incidents.

> The agent will build it to work. Your job is to confirm it is safe when it doesn't.
