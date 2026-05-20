# Board Deck — AI Engineering Update

Companion to *Software Engineering with AI* by Ryan Byrd · Ch 52 §52.1

Four-slide narrative source for the quarterly board update on AI engineering. Replaces `board-deck-template.pptx` so the content is version-controlled and agent-readable. Render to slides only when you actually have a board meeting; the markdown is the source of truth.

The four-slide structure: **Posture · Investment · Metrics · Risks**. Keep to four slides. The board does not need five.

---

## Slide 1 — Posture (01 / 04)

**Title:** AI Engineering — Board Update, Q[N] [YEAR]

**Headline statement:**

> We are pursuing an **investment** posture on AI in engineering. We add AI capacity on top of current headcount. We expect throughput up and quality flat-to-rising, with a six-month review against named metrics.

**Speaker note:** Pick exactly one posture in writing — Investment, Substitution, or Wait-and-See. Ch 29 §29.2 describes the three. Most mid-size companies should pick Investment in year one. If you cannot get to "yes" on one of the three, the board conversation will go badly regardless of what's on the next three slides.

---

## Slide 2 — Investment (02 / 04)

**Headline:** $[X.XM] committed for fiscal year [YYYY]

| Category | Allocation | Notes |
|---|---|---|
| Per-seat licenses (Cursor / Copilot / Claude Code) | $[X]K | Scales with adoption. |
| API token spend | $[X]K | Routing discipline matters most here. |
| Platform engineering time on harness | $[X]K | FTE equivalent. |
| Governance, security review, training | $[X]K | Includes vendor reviews and customer Q&A. |

**Named outcomes:** 8–15% throughput gain on Tier-2 work · quality at or above baseline · zero AI-attributed customer incidents.

**Owner:** [Your name], VP Engineering · **With:** [Platform Lead], harness · **CISO countersign on tooling matrix.**

**Cadence:** Quarterly review · monthly dashboard to CFO · weekly cost telemetry to engineering.

---

## Slide 3 — Metrics (03 / 04)

The five numbers you commit to in writing, with comparison to last quarter's baseline.

| Metric | This quarter | vs. Q[N-1] | Notes |
|---|---|---|---|
| Lead time (Tier-2) | _[value]_ | _[-12%]_ | Lower is better. |
| Deployment frequency | _[value]_ | _[+4%]_ | Higher is better. |
| Change failure rate | _[value]_ | _[flat]_ | Flat is good. Watch for AI-attributed changes. |
| MTTR | _[value]_ | _[-8%]_ | Lower is better. |
| Failed-one-shot ratio | _[value]_ | _[down from 41% in M1]_ | Operational quality signal. |
| Per-dev token spend | _[$92/wk median]_ | _[under budget]_ | Cost discipline signal. |

**Speaker note:** Do not add metrics. If a board member asks for a new metric, ask why and what decision it would change. Most ad-hoc board metrics produce no decision.

---

## Slide 4 — Risks (04 / 04)

Five named risks, with mitigation, owner, and trigger condition.

| Risk | Mitigation |
|---|---|
| **Vendor terms change unexpectedly.** AI vendor changes pricing, training opt-in defaults, or deprecates features with insufficient notice. | Quarterly contract reviews · multi-vendor approach · vendor-changes log · contractual notice obligations on renewal. |
| **AI-authored code defect in production.** An AI-assisted change passes review and CI but causes a customer-impacting incident. | Multi-stage review (AI reviewer subagent + human) · CODEOWNER gating on sensitive paths · canary deploys · AI-aware postmortem. |
| **Reviewer burnout / quality decay.** Senior engineers absorb increased PR volume; review quality drops; slop accumulates. | Hard PR-size limits · round-robin review · PR throughput caps per author · quality decay monitoring (mutation score, revert rate). |
| **Customer data exposure via AI tooling.** Customer-classified data sent to AI vendor without contractual protection. | Pre-commit hooks block known patterns · data classification matrix · cost gateway logs all calls · quarterly prompt-injection exercises. |
| **Budget overrun on token spend.** Token spend exceeds forecast due to model-mix shift or retry loops. | Per-developer cost dashboard · routing discipline (Sonnet default, Opus on review) · monthly forecast vs actual · CFO has dashboard access. |

---

## Rendering to slides

When you need actual slides for a meeting, paste each `##` section into a slide template of your choice (Keynote, Google Slides, etc.). The structure is intentionally minimal — bullet points are the wrong shape for board updates. Use the markdown above as the script; the visual is secondary.
