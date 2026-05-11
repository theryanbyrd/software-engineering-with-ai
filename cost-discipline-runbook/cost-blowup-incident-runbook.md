# Cost Blowup Incident Runbook

What to do when a cost incident is happening right now. Per Ch 29 §29.6 (common cost blowup patterns).

This runbook is for the moment between alert firing and the costs being contained. The discipline: stop the bleeding, then investigate.

## When this runbook applies

Triggers:
- Org-wide anomaly alert fires (10× spike vs 7-day rolling average)
- Per-task ceiling alert fires repeatedly in a short window
- A vendor-side notification (e.g., the LLM provider notifies of unusual usage)
- A finance / FP&A signal (the monthly bill is dramatically higher than expected before the month is even half over)
- An engineer self-reports a runaway session

## Phase 1 — Stop the bleeding (first 15 minutes)

The single most important objective: contain the spend NOW.

### Step 1 — Identify the source

Where is the spend coming from?

- The on-call engineer pulls the gateway dashboard
- Sort by spend in the last hour; identify the top engineer / session / workflow
- Common sources:
  - One engineer with a runaway session
  - A scheduled batch job that's looped
  - A subagent in a retry loop
  - A new automation that wasn't tested at scale

### Step 2 — Kill the source

Once identified, kill it:

- **Runaway agent session:** terminate via the gateway or via the engineer's IDE
- **Scheduled job:** disable the schedule; cancel running instances
- **Subagent loop:** disable the subagent; investigate why
- **Automation:** disable the automation; review its config

If the source is unclear, the on-call may need to take a more aggressive measure: rate-limit the entire org's gateway temporarily. This is appropriate when:
- The spend rate is so high that 5 more minutes of investigation costs $5K+
- The source can't be identified within 5-10 minutes
- The blast radius of a temporary rate-limit is acceptable

### Step 3 — Communicate

Notify:
- The engineer whose work was killed (if applicable)
- The team's EM
- Engineering leadership (if spend in the spike was >$5K)
- Finance (if spend was >$25K)

The communication is short and factual:

> "Cost incident: [source]. Stopped at [time]. Spend in the spike: ~$[amount]. Investigating root cause; will follow up with postmortem."

Don't speculate on cause yet. The investigation comes in Phase 2.

## Phase 2 — Investigate (next 24 hours)

Now that the bleeding is stopped, the question: what happened?

### Common root causes

#### Cause 1 — Idle-loop / retry-loop

Per Ch 29 §29.6:

> Agents in tight retry loops. Cap retries at 3; fail loudly.

The agent encountered an error and retried; each retry costs more; no upper bound on retries.

**Investigation:**
- Look at the session transcript
- Identify the failure that triggered the loop
- Verify retry budgets are configured

**Fix:**
- Add or tighten retry budget at the gateway / agent level
- Update agent's prompt/skill to handle the failure mode gracefully
- Add monitoring that catches the pattern earlier

#### Cause 2 — Long-running agent task

Per Ch 29 §29.6:

> Runaway long-running tasks. Time-box every agent invocation. Default 15 minutes.

The agent ran for hours, generating tokens continuously without completing.

**Investigation:**
- Check whether time-box was configured
- Identify whether the task was scoped appropriately
- Review whether the agent was making progress (long but useful) or stuck (long and not useful)

**Fix:**
- Implement gateway-level time budgets if not present
- Tighten task scope at agent invocation
- Add progress monitoring

#### Cause 3 — Opus on routine tasks

Per Ch 29 §29.6:

> Opus on routine tasks. Route to Sonnet by default; promote to Opus only on demonstrated need.

Engineer (or system) configured the agent for Opus by default. Routine workflows ran at Opus cost.

**Investigation:**
- Look at the model mix in the spike
- Identify why Opus was selected
- Check whether routing rules apply

**Fix:**
- Per [`model-routing-rubric.md`](model-routing-rubric.md), reset defaults to Sonnet
- Review skills / subagents for explicit Opus calls; demote to Sonnet where appropriate

#### Cause 4 — Context bloat

Per Ch 29 §29.6:

> Trim context aggressively; use skills (loaded only when invoked) instead of bloated CLAUDE.md.

The CLAUDE.md / AGENTS.md / system prompts were so large that every call paid significant input cost.

**Investigation:**
- Measure the input token count for the affected sessions
- Identify what's in the context that shouldn't be

**Fix:**
- Trim CLAUDE.md to team-wide invariants
- Move per-task content to skills
- Audit `llms.txt` and other auto-loaded content

#### Cause 5 — Cache misses

Per Ch 29 §29.6:

> A workload that should hit cache but isn't is a bug.

Stable system prompts that should be cached weren't being cached, costing input tokens unnecessarily.

**Investigation:**
- Check cache hit rate for the affected workflow
- Identify why cache wasn't hit (changing system prompt, key drift, configuration)

**Fix:**
- Stabilize system prompts to be cache-eligible
- Configure cache headers correctly
- Verify the cache is actually being used

#### Cause 6 — Tokenizer change

Per Ch 29 §29.6:

> Opus 4.7's new tokenizer can add up to 35% effective cost vs Opus 4.6.

A model upgrade introduced a new tokenizer; effective cost shifted significantly.

**Investigation:**
- When did the model version change?
- Is the cost increase consistent with the documented tokenizer change?

**Fix:**
- Update budget to reflect new effective cost
- Adjust routing if Opus's effective cost has shifted enough to change the model selection logic
- Update the team's monthly cost review (per [`monthly-cost-review-structure.md`](monthly-cost-review-structure.md))

#### Cause 7 — New automation tested at scale

A scheduled job, subagent, or automation was built and deployed. At scale, it consumed much more than expected.

**Investigation:**
- What's the new automation?
- Was it tested at low volume before broad deployment?
- What's the per-invocation cost vs expected?

**Fix:**
- Disable until cost profile is understood
- Test at small scale; measure actual per-invocation cost
- Re-enable with appropriate budget and monitoring

#### Cause 8 — Engineer running unattended jobs

Per Ch 29 §29.4:

> One developer running unattended overnight jobs nobody approved.

An engineer (sometimes well-intentioned) ran a long-running automation without team awareness.

**Investigation:**
- Talk to the engineer
- Understand what they were trying to accomplish
- Determine whether the work was warranted at all

**Fix:**
- Cultural reset (this is a 1:1 conversation, not a public broadcast)
- Possibly a process change (overnight jobs require manager / platform pre-approval)
- Add specific patterns to monitoring

## Phase 3 — Postmortem (within 5 business days)

Per `incident-postmortem-templates/`, a structured postmortem.

The cost-incident-specific sections to add to the postmortem template:

### Cost impact

- Total spend in the incident
- Spend that wouldn't have occurred without the incident (vs baseline)
- Cost of recovery work (engineering hours)

### Detection latency

- When did the spike start?
- When did the alert fire?
- When was the source identified?
- When was it stopped?
- Was the detection within target SLO?

### Specific harness gap

Per the harness deficiency framework (`incident-postmortem-templates/harness-deficiency-checklist.md`):
- What in the harness, if it had existed, would have prevented this?
- Specific harness change to ship within 1-2 weeks

### Pattern with prior incidents

- Has a similar incident occurred before?
- Are there patterns suggesting structural rather than one-off issue?
- Should the team's autonomy ladder, budget, or routing change as a result?

### Lessons for the team

What should every engineer internalize from this incident?

## What good incident response looks like

Healthy:
- Bleeding stopped within 15 minutes of alert
- Source identified within 30 minutes
- Stakeholders notified within 30 minutes
- Postmortem within 5 business days
- Specific harness change shipped within 2 weeks of postmortem
- Same incident doesn't recur

Concerning:
- Bleeding takes >30 minutes to stop
- Source unclear for >1 hour
- Stakeholders surprised after the fact
- Postmortem doesn't ship
- Harness changes don't ship from postmortem action items
- Similar incidents recur

## Anti-patterns

### "It's just a cost incident; not really an incident"

Cost incidents are real incidents. Treat them as such. The postmortem discipline applies.

### Blame the engineer

The engineer whose session caused the spike was doing their job; the harness failed. Per `incident-postmortem-templates/`, the postmortem is harness-focused, not engineer-focused.

### Skip the postmortem because "it's a one-off"

Most "one-offs" recur in some form. The postmortem captures the learning so the recurrence is caught earlier.

### Hide the cost incident from leadership

The cost shows up on the bill anyway. Hiding the incident makes it harder to explain. Surface promptly; communicate honestly.

### Treat all cost incidents as equally serious

A $500 spike is not the same as a $50K spike. Calibrate the response. The runbook applies in both cases; the urgency and stakeholder communication scale.

## What this runbook will NOT do

- Will not eliminate cost incidents. New failure modes emerge; some incidents are unavoidable.
- Will not work without anomaly detection. The runbook starts when the alert fires; if there's no alert, the cost has already been incurred.
- Will not work in cultures that hide cost issues. The runbook depends on prompt surfacing; without it, incidents become "discovered" rather than "responded to."

## Companion artifacts

- [`anomaly-detection-workflow.md`](anomaly-detection-workflow.md) — what triggers this runbook
- [`token-budgets-by-team.md`](token-budgets-by-team.md) — adjacent
- [`model-routing-rubric.md`](model-routing-rubric.md) — adjacent
- `incident-postmortem-templates/` — the postmortem framework
- Ch 29 §29.6 — source
