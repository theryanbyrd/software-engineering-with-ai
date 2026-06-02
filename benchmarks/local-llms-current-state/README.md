# Local LLMs — Current State (Ch 28)

> Companion to *Software Engineering with AI*, Chapter 28. The book deliberately moved
> the perishable specifics here: "I have moved that content to the companion repo
> (`benchmarks/local-llms-current-state/`), where it can be updated quarterly. What stays
> in the book is the principles, which are durable." (Ch 28 §28.3)

**This file is a snapshot and goes stale fast. Refreshed quarterly.** Last reviewed:
2026-Q2 (book revised v15). If the date is more than a quarter old, treat every specific
number as wrong and trust the principles, not the figures.

## The durable principle (this does not go stale)

Frontier API for agents; local LLM for routing and sovereign data. Most mid-size teams
should treat local LLMs as a **year-two** question. The two exceptions that make it a
**this-quarter** question (Ch 28, Ch 50.5 §50.5.3):

- **Sovereign-data customers** who legally cannot send prompts to a hosted model
  (EU/healthcare/government). This category is growing, and EU AI Act enforcement is real.
- **High-volume routing/classification** workloads where per-token economics dominate.

If you're in either bucket, start the evaluation now — the harness work transfers; the
model swap is the easy part if you built the harness right.

## What this directory tracks (quarterly refresh)

- **Best open-weights coding model right now** — and how it scores on *your* internal
  benchmark (see [`../`](../) golden tasks), not on public leaderboards.
- **Inference engine** tradeoffs — vLLM, llama.cpp, MLX, TGI.
- **Hardware** — current Mac Studio / RTX / Pro-class configurations, the unified-memory
  threshold for a competent model at reasonable token rates, AMD vs NVIDIA vs Apple Silicon,
  and the wattage/rack math.
- **Break-even ROI** — plug in your token volume and decide whether local beats hosted for
  *your* situation.

## Why the specifics aren't in this file (yet)

Earlier book drafts quoted specific RTX 5090 / Pro 6000 / M3 Ultra prices and SKU-level
configs. Every one of those goes wrong within a quarter — the SKU moves, the price drops,
or a successor ships. This README intentionally carries the **structure** of what to
evaluate; drop the current-quarter numbers and the ROI calculator inputs in alongside it
and date them. A dated, wrong-but-honest snapshot beats an undated one that looks current.

**To contribute a refresh:** add a dated section (`## 2026-Q3`, etc.) with the four
categories above, your benchmark methodology, and a `last-verified` date. Don't edit a
prior quarter's snapshot — append a new one, so the trend stays visible.
