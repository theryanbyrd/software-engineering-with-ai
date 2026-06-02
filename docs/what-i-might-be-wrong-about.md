# What the Book Might Be Wrong About (Ch 50.5)

> Companion to *Software Engineering with AI*, Chapter 50.5 — the author's steelman
> against his own thesis. Captured here because the book's main claims are *falsifiable*,
> and a companion repo is the right place to track whether they hold up over time.

The book's central thesis: **the harness matters more than the model.** Chapter 50.5 lays
out where that could be wrong. The honest counter-cases:

1. **The model eats the harness (§50.5.1).** If frontier models cross the thresholds the
   harness works around — long-context coherence, reliable autonomous browsing/verification,
   multi-hour tool-use — the skills/subagents/CLAUDE.md hierarchy collapses into
   capabilities the model just has. Watch for: companies with *no* platform investment
   matching ones with serious investment on non-trivial work.
2. **Vibe-coding is fine in narrow domains (§50.5.2).** For internal tools three people
   use, throwaway dashboards, one-time migration scripts, and experiment notebooks, the
   full Tier-1 playbook is overkill. The line: anything touching **money, user data,
   unattended schedules, or other people's work** stays disciplined; outside that line,
   let the agent rip.
3. **Local LLMs win faster than year-two (§50.5.3).** Sovereign-data customers, a strong
   open-weights release, or a high-unified-memory hardware refresh could each make local a
   this-quarter concern. (The author bets he's "probably late by a year" here.)
4. **PR throughput is a fine metric (§50.5.4).** Imperfect-but-observable can beat
   perfect-but-unmeasurable. If you can't instrument verify-pass rate / regression health /
   cost-per-change, PR throughput + a quality canary is a defensible interim — just don't
   believe it.
5. **AI pricing won't keep falling (§50.5.5).** The cheaper-every-quarter trend may be a
   subsidized price curve, not a structural one (the cloud subsidize-then-hike playbook).
   Keep the harness model-portable so a price shock is survivable; treat any vendor's
   current price as promotional, not a baseline.

**Where the author has already been wrong (§50.5.6):** in early 2024 he called AI
"fundamentally unsuited for refactoring." By mid-2025 that was clearly wrong — largely
because the *harness* improved (long-context tooling, retrieval, subagent fan-out,
verify-command culture). The lesson: capability claims are snapshots, not trends.

**The falsifiable bottom line (§50.5.7):** the thesis flips if, by end of 2027, all three
hold — (a) a frontier model's internal loop beats what a good platform team can assemble,
on Tier-2 production work; (b) low-platform-investment companies sustainably match
high-investment ones on shipped outcomes; (c) the better model's cost drops to within a
small multiple of the commodity model. One or two true → revision; none true → thesis
holds. Track these here as evidence accumulates.
