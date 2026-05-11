# Quarterly Model Lineup Review

The recurring review per Ch 44 §44.4 item 8: "Re-evaluate the model lineup quarterly, the routing policy with it."

This is the cadence that catches drift in the model landscape. Models improve; pricing shifts; tokenizers change; new model families emerge. Without quarterly review, the team's routing policy ossifies; six months later, the team is paying for capability they don't need or missing capability they could have.

## When to run

Quarterly. Specific calendar week (e.g., second week of quarter end month) so it's predictable. 2-4 days of platform team time.

## Inputs

Before the review:

1. **Current model lineup** — what models the team uses and for what
2. **Internal benchmark results** for current model (per [`internal-benchmark-construction.md`](internal-benchmark-construction.md))
3. **Internal benchmark results** for candidate alternatives
4. **Cost data** from `cost-discipline-runbook/` — model mix, cost-per-PR, anomalies
5. **Public benchmark observations** — what's been said about candidate models in the last 90 days
6. **Vendor announcements** — new releases, deprecation notices, pricing changes
7. **Failed one-shot triage data** (per `failed-one-shot-triage/`) — Question failures specifically (model capability gaps)

## Attendees

Core:
- Platform team lead
- Tech leads (representing each major work area: backend, frontend, infra, etc.)
- Engineering manager / director

Optional:
- Senior IC who runs the benchmark
- Vendor relations / procurement (if vendor changes are on the table)
- Finance representative (for cost decisions of significant magnitude)

## Agenda

A typical 4-hour review (split across 2 sessions or one block):

### Section 1 — Current state (30 minutes)

Platform team presents:

- **Current routing**: what model for what work
- **Current spend**: total monthly, by model, by team
- **Current model mix**: % Haiku / Sonnet / Opus
- **Internal benchmark score** for current primary model

What the data should show:
- Routing matches the published rubric (per `cost-discipline-runbook/model-routing-rubric.md`)
- Model mix is healthy (per the rubric: ~70-80% Sonnet, ~10-15% Haiku, ~5-10% Opus)
- Cost is within budget (per `cost-discipline-runbook/token-budgets-by-team.md`)
- Benchmark score is stable or improving

### Section 2 — Candidate models (45-60 minutes)

For each candidate model that wasn't in the lineup last quarter:

- **What it is**: vendor, version, release date, claimed capabilities
- **Internal benchmark score**: per-category and aggregate
- **Cost**: per-million-token cost; effective cost given tokenizer differences
- **Capability gaps closed**: did this model close any capability gaps the team had?
- **Capability gaps remaining**: what does it still not do well?

Common candidates in 2026:
- New release of current vendor's primary model
- New release of current vendor's smaller / cheaper model
- Strong release from a different vendor
- Specialized models for specific work types (e.g., code-only models)

### Section 3 — Comparison (45-60 minutes)

For each comparison:

- **Per-category scores**: where does the new model win, where does it lose?
- **Aggregate score difference**: per Ch 26 §26.5, 5+ points is signal; 1-2 is noise
- **Cost difference**: per task, per month at expected volume
- **Capability profile difference**: any specific work types where one is markedly better?
- **Migration cost**: what would switching require? (tooling updates, harness adjustments, eng training)

### Section 4 — Decisions (60 minutes)

Per [`when-to-switch-primary-model.md`](when-to-switch-primary-model.md), the decisions:

- **Stay with current primary?** Default unless signal is strong.
- **Switch primary?** Requires 5+ point benchmark improvement and clear pattern across task types.
- **Add a model to the lineup?** (e.g., add a specialized model for one work type while keeping the primary)
- **Drop a model from the lineup?** (e.g., the cheaper model isn't being routed to enough)
- **Change routing thresholds?** (e.g., what triggers escalation from Sonnet to Opus)

For each decision: specific rationale, specific date for change, specific success criteria for re-evaluation next quarter.

### Section 5 — Routing policy update (30 minutes)

If decisions affect the routing policy, update `cost-discipline-runbook/model-routing-rubric.md`:

- Default model for routine work
- Escalation paths for hard work
- Demotion paths for cheap work
- Subagent model assignments
- Skill model assignments

Per [`routing-policy-update-process.md`](routing-policy-update-process.md), the update has a process beyond just changing the doc.

### Section 6 — Communicate (15 minutes)

What needs to be communicated to the team:

- Specific changes (model X is now default; model Y is deprecated)
- Specific dates (when changes take effect)
- Specific actions engineers need to take (update local config, retrain on new patterns)
- Specific resources (link to updated routing rubric, examples of when to use new model)

Communication channels:
- Major changes (primary model switch): all-hands or org-wide email
- Minor changes (routing thresholds): team-channel announcement
- Vendor changes (deprecations): platform team broadcasts via their normal channels

## Outputs

After the review:

1. **Decisions log**: what was decided, why, by whom
2. **Updated routing rubric** (if decisions affect it)
3. **Updated CLAUDE.md / AGENTS.md** (if model defaults change)
4. **Updated tooling configuration** (if defaults are configured at the tool level)
5. **Communication plan** with specific dates
6. **Next quarter's review date** on the calendar

## What good quarterly review looks like

Healthy:
- Most quarters produce minor adjustments, not major switches
- Decisions are based on internal benchmark, not vendor marketing
- Cost considerations are factored in but not dominant
- Communication reaches the team within a week of the review
- Engineers experience the changes as deliberate, not surprising

Concerning:
- Switches happen every quarter (chasing benchmarks)
- Switches are based on vendor announcements without internal benchmark
- Cost considerations dominate (or are entirely absent)
- Communication is delayed or absent
- Engineers learn about changes through second-hand channels

## What can go wrong

### Internal benchmark is stale

If the benchmark hasn't been refreshed in 6+ months, results may not reflect current work patterns. Mitigation: per [`internal-benchmark-construction.md`](internal-benchmark-construction.md), refresh quarterly.

### Decisions made without full data

The platform team didn't run the candidate model against the benchmark before the review. The decision is on vibes.

Mitigation: the benchmark run is a prerequisite. If it hasn't been done, defer the decision to next month, not next quarter.

### Decisions made by committee with no owner

Multiple stakeholders weigh in; no one has decision authority. Decisions don't actually get made.

Mitigation: clear decision rights — typically the platform team lead or engineering director has the call, with input from the others.

### Switching too often

The team switches primary model every quarter. Each switch has migration cost; cumulative migration cost exceeds capability gains.

Mitigation: the 5-point rule. Don't switch on noise; do switch on signal.

### Switching too rarely

The team is loyal to the current primary regardless of benchmark data. After 18 months, the primary is two model generations behind.

Mitigation: the benchmark forces the conversation. Even if the decision is "stay," the conversation has happened.

### Vendor pressure for switches

A vendor's BD team is pitching their newer model heavily. The team feels pressure to switch.

Mitigation: vendor pitches are input; the internal benchmark is the decision. Per `vendor-procurement-runbook/`, vendor relationships are managed separately from technical decisions.

## Mid-cycle review triggers

Don't wait until the next quarterly review if:

- A major model release (new flagship model) drops with claimed substantial improvements
- A pricing change makes the current routing economically irrational
- A model deprecation forces action
- A capability gap surfaces that the current lineup can't address (e.g., new work type the team needs to support)

For these, schedule a mid-cycle review within 2-4 weeks of the trigger.

## Anti-patterns

### Quarterly review without action

The review happens; no decisions are made; the routing rubric isn't updated. The cadence becomes performative.

Mitigation: every review produces specific outputs. Even "no change" is a decision with documented reasoning.

### Quarterly review that reviews everything every time

The review tries to evaluate every model from every vendor every quarter. Becomes a 3-day exercise; gets skipped.

Mitigation: focus on materially relevant changes. Most quarters, the review is current model + 1-2 candidates.

### Quarterly review without engineer input

The platform team makes routing decisions without engineer feedback. Engineers route around the decisions.

Mitigation: tech leads attend the review; engineer feedback flows in via normal channels (Slack, retros, 1:1s).

### Quarterly review tied to vendor renewals

The review timing is set by the vendor's contract cycle, not the team's needs. Decisions are coupled to procurement.

Mitigation: the technical review and the procurement review are separate. Per `vendor-procurement-runbook/renewal-discipline.md`, vendor renewals have their own discipline.

## Companion artifacts

- [`internal-benchmark-construction.md`](internal-benchmark-construction.md) — the foundation
- [`when-to-switch-primary-model.md`](when-to-switch-primary-model.md) — the decision framework
- [`routing-policy-update-process.md`](routing-policy-update-process.md) — what happens after a decision
- `cost-discipline-runbook/model-routing-rubric.md` — what gets updated
- `cost-discipline-runbook/monthly-cost-review-structure.md` — adjacent monthly cadence
- `vendor-procurement-runbook/renewal-discipline.md` — adjacent vendor cadence
- Ch 26 §26.5, Ch 44 §44.4 item 8 — sources
