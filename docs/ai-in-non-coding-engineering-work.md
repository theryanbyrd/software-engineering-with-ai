# AI in Non-Coding Engineering Work (Ch 47.5)

> Companion to *Software Engineering with AI*, Chapter 47.5. The book mostly delivers AI
> *in coding* — the most concrete, demonstrable part of the job. But senior engineers
> spend less than half their week in editors, and the non-coding workflows are
> **higher leverage**. Same harness, applied with discipline.

Across all of these the line is identical: **use the agent to draft and structure; do not
use it to publish or decide.** The failure modes here are mostly recoverable (a bad draft
wastes an afternoon), which is the opposite of the coding cases (a bad merge wastes a
week) — so adoption can be *more* aggressive here, not less.

| Workflow | The win | Hard caveat |
|----------|---------|-------------|
| **Incident-response triage (§47.5.1)** | A T1 slash command takes a Slack channel + time window, pulls thread + logs/dashboards via MCP, and emits a timeline, a draft status-page update in the company voice, and rank-ordered probable causes with supporting log lines. Real case: time-to-status-update cut from ~15 min to <3. | The agent **drafts**; humans approve and post. One bad autonomous status-page post isn't worth the time saved. Compose, don't publish. |
| **On-call summarization / weekly digests (§47.5.2)** | A weekly job turns the noisy alert stream + incident docs + resolution notes into a one-page summary: patterns, proposed runbook fixes, follow-ups worth a review. ~90 min/week saved for a manager over one rotation. | Read it, route it; it's a digest, not a decision. |
| **Vendor risk reviews (§47.5.3)** | Document-comparison task: SOC2 + DPA + questionnaire vs. company risk policy (in CLAUDE.md). First-pass findings hit ~80% of what a human would write, with clauses quoted + page refs. ~4 hours → ~40-min review (≈6x on the slow part). | Human reviewer still reviews; legal still signs off. Nobody who can't be fired ships it. |
| **RFP responses (§47.5.4)** | With past responses + compliance docs + architecture docs in CLAUDE.md, the agent drafts ~70% in an afternoon; the senior spends time on the ~30% that's genuinely new. | Legal review is non-negotiable — RFPs contain binding commitments. |
| **Technical recruiting screens (§47.5.5)** | Tailored screen problems calibrated to role/level; grading take-homes against a published rubric; structured debriefs from raw interviewer notes. | **Most cautious section.** Never let the agent score candidates, rank a slate, or make hire/no-hire calls — it's a bias amplifier. Draft and structure only; the interviewer's name is on the debrief. |
| **Architecture review prep (§47.5.6)** | Feed the design doc + repos + last 3 ADRs; get the 15–20 questions the panel will likely ask. 30 min of prep means the author walks in ready instead of being surprised. | It generates a checklist of obvious questions, not insight — which is exactly what the too-close author has stopped seeing. |
| **Performance review writing (§47.5.7)** | Manager dictates observations throughout the cycle; at review time the agent produces a structured first draft cross-referenced to the leveling rubric and flags vague language ("collaborates well" → concrete example). | **Data never leaves the manager's machine.** No cloud sync, no shared repo, no vendor MCP. If you can't guarantee that operationally, don't use the agent here — this is where the local-LLM story actually matters. |

## Why these are higher leverage (§47.5.8)

A 30% speedup on coding work is real but localized; a 6x speedup on vendor reviews changes
*whether vendor reviews happen at all*. The hours saved on RFP toil, weekly digests,
vendor reviews, and architecture prep compound across the org far faster than per-task
coding gains — and the failure modes are recoverable. The asymmetry favors **aggressive
adoption in non-coding work, conservative adoption in coding work** — roughly the opposite
of how most teams have allocated their attention.

**Related repo artifacts:** [`../incident-postmortem-templates/`](../incident-postmortem-templates/) ·
[`../vendor-procurement-runbook/`](../vendor-procurement-runbook/) ·
[`../people/`](../people/) · [`../promotion-and-leveling-rubric/`](../promotion-and-leveling-rubric/) ·
[`../customer-facing-ai-disclosure/`](../customer-facing-ai-disclosure/).
