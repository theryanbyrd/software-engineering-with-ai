# Anomaly Detection Workflow

Detection thresholds, alerting, and triage when costs spike. Per Ch 29 §29.5 (budget guardrails):

> Per-developer soft cap: $30/day. Pages developer at 80%, requires manager ack at 100%.
> Per-team monthly hard cap: team budget × 1.2. Hits page the EM and platform on-call.
> Org-wide anomaly: any 10x spike vs 7-day rolling average pages on-call within 5 minutes.
> Per-task ceiling: any single agent invocation over $10 requires explicit confirmation.
> Idle-loop detector: if the same prompt fires three times in 60 seconds with similar token counts, kill the session.

This file is the operational implementation of those guardrails.

## The five detection layers

### Layer 1 — Real-time idle-loop detection

**What it detects:** an agent stuck in a retry loop firing the same or near-same prompt repeatedly.

**Threshold:** 3 firings in 60 seconds with similar token counts and similar response patterns.

**Action:** kill the session. Notify the engineer. Log for review.

**Implementation:** the LLM gateway tracks recent prompts per session; on detection, the next prompt is rejected with an error.

**Why this is layer 1:** retry loops can spend $100+ in minutes. Real-time detection is the only protection.

### Layer 2 — Per-task ceiling

**What it detects:** a single agent invocation that would exceed the per-task ceiling ($10 by default).

**Threshold:** projected cost of the next response exceeds $10 cumulative for the invocation.

**Action:** require explicit confirmation. The agent's next call is blocked until the engineer confirms.

**Implementation:** gateway tracks cumulative cost per invocation; surfaces a confirm prompt before exceeding ceiling.

**Why $10:** large enough that routine work doesn't trigger; small enough that runaway invocations are caught early.

### Layer 3 — Per-developer daily threshold

**What it detects:** a developer approaching or exceeding their daily soft cap.

**Threshold:**
- 80% of soft cap: notify the developer (their dashboard or a Slack DM)
- 100% of soft cap: require manager ack to continue spending today

**Action:**
- 80%: visibility, no action required
- 100%: developer must request continuation; manager reviews and approves (or denies)

**Implementation:** gateway / dashboard tracks per-developer spend per day; thresholds trigger appropriate notifications.

**Why this is layer 3:** catches sustained high-spend patterns before they become persistent; doesn't block legitimate heavy-spend days but surfaces them.

### Layer 4 — Per-team monthly threshold

**What it detects:** a team approaching or exceeding their monthly budget.

**Threshold:**
- 80% of monthly budget: notify the EM
- 100% of monthly budget: notify EM + Engineering Director
- 120% (hard cap): page EM + platform on-call

**Action:**
- 80%: visibility
- 100%: conversation about the trajectory
- 120%: investigate; pause non-critical AI usage if patterns suggest it; recalibrate budget if pattern is sustained

**Implementation:** dashboard with monthly rollup; threshold-triggered alerts.

### Layer 5 — Org-wide anomaly

**What it detects:** organization-wide spend spike vs. 7-day rolling average.

**Threshold:** 10× spike vs. 7-day rolling average for any 1-hour window.

**Action:** page on-call within 5 minutes. Investigate within 30 minutes.

**Implementation:** time-series anomaly detection on org-wide spend telemetry.

**Why this is layer 5:** catches the failure mode that bypasses other layers — a single agent or a small group spending so much in such a short window that the catastrophic spend is over before the per-developer or per-team alerts fire.

## Triage when alerts fire

### Idle-loop alert (Layer 1)

The session was killed. Investigation:

1. **Look at the session transcript.** What was the agent stuck on?
2. **Common causes:** missing context, tool failure, agent hallucination loop, prompt incompatibility with model
3. **Fix:** address the root cause. Sometimes a CLAUDE.md fix; sometimes a tool fix; sometimes a model fit issue
4. **Track:** add to the "common loops" log so the team learns

### Per-task ceiling alert (Layer 2)

The engineer must confirm to continue. Triage:

1. **Is the work legitimately expensive?** (Large refactor; large file analysis; complex debugging.) If yes, confirm and continue.
2. **Is the work badly scoped?** (Agent loaded too much context; agent is exploring rather than executing.) Cancel; rescope.
3. **Should this be a different model?** (Maybe Sonnet is overkill; maybe Opus would actually finish faster.) Reconsider routing.

### Per-developer daily alert (Layer 3)

#### At 80%: visibility prompt

The developer sees their spend approaching cap. They review:
- Is today an unusually heavy day? (legitimate; continue)
- Is there a model-routing issue? (correctable)
- Is there an agent loop or context bloat? (fixable)

#### At 100%: manager ack required

The conversation:

> "I'm at my daily cap. I'm working on [task]; I expect to need [more spend] to complete it. Reasons: [specific]. Can you ack continuation?"

Manager response:
- **Ack:** the work is legitimate; pattern is one-day, not chronic
- **Conversation:** the pattern suggests model misuse or scope creep; the conversation is about the pattern, not just today
- **Decline:** the work isn't priority enough to spend through the cap; defer

### Per-team monthly alert (Layer 4)

#### At 80%: EM notification

The EM looks at the team's spend pattern:
- Per-developer breakdown
- Per-task-type breakdown
- Anomalous days

If the pattern is normal (steady ramp; no anomalies), no action needed. The 80% alert is awareness.

#### At 100%: conversation

The EM and engineering director discuss:
- Is this team's scope and capability matched to budget? (Maybe budget needs increase)
- Is there a model-routing issue at the team level?
- Is there a specific person or task driving the over-spend?

#### At 120%: pause and investigate

Hard cap. The team pauses non-critical AI usage until the investigation completes:
- Root cause identified
- Recovery plan agreed
- Budget recalibration if pattern is sustained

The pause is uncomfortable. It's the discipline that makes the cap real.

### Org-wide anomaly (Layer 5)

This is a fire. Within 30 minutes:

1. **Identify the source.** Which team, which engineer, which session?
2. **Stop the bleeding.** Kill the session if it's still running. Pause the affected workflow.
3. **Assess the cost.** What's been spent in the spike?
4. **Communicate.** Notify the engineering leadership; finance if the spike is severe ($10K+ in an hour).
5. **Postmortem.** Per `incident-postmortem-templates/`.

## Anomaly detection technology

The mechanism: a process that watches the spend stream and triggers on patterns. The implementation:

1. **OpenTelemetry GenAI semantic conventions** (per Ch 29 §29.3) emit per-call telemetry
2. **An LLM gateway** centralizes the calls, applying budgets, retries, model routing
3. **A real-time stream processor** watches the gateway's output for anomalies
4. **Alerting integration** routes alerts to the right person (developer, EM, on-call)

If your team doesn't have this stack:
- Idle-loop detection: minimum viable is a script that scans the LLM gateway's logs for repeated prompts within 60s
- Per-task ceiling: instrument at the agent invocation level
- Per-developer daily: dashboard + email alert via your existing observability
- Per-team monthly: monthly dashboard review (per [`monthly-cost-review-structure.md`](monthly-cost-review-structure.md))
- Org-wide anomaly: requires real-time stream processing

The platform team (per `platform-team-charter/`) typically owns this infrastructure.

## False positives and tuning

Anomaly detection has false positives. The discipline is to tune:

### Idle-loop false positive

A legitimate workflow happens to send similar prompts in quick succession (e.g., parallelized scoring). Tune by:
- Whitelisting specific workflows
- Lengthening the time window
- Adding workflow context to the detection (different invocation IDs are not loops)

### Per-task ceiling false positive

A legitimately expensive task triggers the ceiling. Tune by:
- Raising the ceiling for specific task categories
- Pre-authorizing specific high-cost workflows
- Reviewing the ceiling number quarterly

### Per-developer daily false positive

An engineer doing migration work or large refactor legitimately exceeds the cap. Tune by:
- Pre-authorizing specific high-cost projects
- Adjusting the cap for engineers in roles that warrant higher spend (platform team, principal engineers)
- Reviewing patterns: persistent over-cap is a routing issue; periodic over-cap is normal

### Org-wide anomaly false positive

A scheduled batch job that runs once a week creates a "spike" relative to the rolling average. Tune by:
- Subtracting known scheduled work from the anomaly baseline
- Whitelisting specific workflow signatures
- Sliding-window averages that account for weekly periodicity

## Anti-patterns

### Alerts that go to nobody

The alert fires; it goes to a Slack channel nobody watches; nobody investigates.

Mitigation: alerts route to specific named people; on-call rotation has clear ownership.

### Alerts that fire too often

Too-tight thresholds produce noise; engineers learn to ignore. The next real anomaly is missed.

Mitigation: tune thresholds against actual data; quarterly review of alert volume; investigation of any alert with >5% false positive rate.

### Per-developer cap as performance review input

A manager uses the per-developer cap data as a performance signal — engineers below cap are praised, above cap are penalized.

Mitigation: per-developer caps are operational, not performance. Use them for routing conversations, not for ratings.

### Anomaly detection without follow-up

Alerts fire, get acknowledged, no postmortem. Patterns repeat.

Mitigation: anomaly investigations produce specific actions in the postmortem template (per `incident-postmortem-templates/`).

## What this workflow will NOT do

- Will not work without instrumentation. The detection mechanisms require telemetry.
- Will not catch every anomaly. New failure modes emerge; detection has to evolve.
- Will not eliminate the conversation. Detection produces signal; the conversation is the work.
- Will not replace cost discipline at the team level. Anomalies are the protection layer; the underlying discipline is the [`token-budgets-by-team.md`](token-budgets-by-team.md) and [`model-routing-rubric.md`](model-routing-rubric.md).

## Companion artifacts

- [`token-budgets-by-team.md`](token-budgets-by-team.md) — the structure that detection protects
- [`model-routing-rubric.md`](model-routing-rubric.md) — the routing that prevents many anomalies
- [`cost-blowup-incident-runbook.md`](cost-blowup-incident-runbook.md) — what to do when an anomaly is happening now
- `incident-postmortem-templates/` — postmortem after the incident
- Ch 29 §29.5-§29.6 — sources
