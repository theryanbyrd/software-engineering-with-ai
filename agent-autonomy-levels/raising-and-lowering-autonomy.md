# Raising and Lowering Autonomy

The conversation and discipline for moving levels up or down. Per Ch 32 §32.4:

> A team's autonomy level is not the highest level of any individual; it is the level that the team's harness, review discipline, and incident history have earned. Move levels deliberately.

This file is the operational discipline for those moves.

## The promotion criteria (Ch 32 §32.4 verbatim)

| Move | Required |
|---|---|
| **L0 → L1** | Harness in place (CLAUDE.md, AGENTS.md, verify, hooks) |
| **L1 → L2** | PR review discipline proven on 30+ AI-assisted PRs without a slop incident |
| **L2 → L3** | Subagent roster in production, review checkpoints automated, observed for 90 days |
| **L3 → L4** | Strictly within tier-restricted whitelist (docs/tests/types only), CODEOWNERS enforced, automated rollback exercised within last 30 days, zero auto-merge incidents in 90 days |
| **L4 → L5** | Never |

Each promotion is a discrete decision, not a gradual drift. The discipline is to make the decision explicitly, document it, and review it regularly.

## When to raise autonomy

The conversation about raising autonomy starts when at least three things are true:

1. The team has met the explicit criteria for the next level
2. There is a specific category of work that would benefit from the higher level
3. The current level is producing visible friction (slow PR throughput, engineers bypassing the discipline informally, etc.)

If only one or two are true, raising is premature. The friction may be the discipline doing its job.

### The conversation script — raising autonomy

The team lead or platform lead initiates:

> "I want to talk about raising our autonomy level for [specific category, e.g., test additions] from L2 to L3. Three things make me think it's time:
>
> First — we've met the criteria. Specifically: [concrete examples — subagent roster running, 90 days at L2 with no slop incidents, our review checkpoints are automated for this category].
>
> Second — there's a specific use case. [Specific example — the test-generation work we've been doing manually represents X PRs/quarter; running at L3 with a defined task whitelist would let us actually do the test backfill we keep deferring.]
>
> Third — we're seeing friction at L2 specifically. [Specific examples — engineers are batching test PRs because the L2 review overhead is heavy; this is producing review fatigue and slow merges.]
>
> What I'm proposing: a 60-day trial at L3 for test additions specifically, with a narrow task whitelist, with explicit checkpoints. After 60 days we review."

### What the conversation should produce

A clear yes / no / not-yet:

- **Yes:** specific task whitelist, specific success criteria, specific review date
- **No:** specific reason (criteria not met, harness gap, recent incident)
- **Not yet:** specific work to close the gap before reconsidering

If the conversation produces "let me think about it," that's a soft no. Push for a specific answer.

### What raising autonomy looks like in practice

Once the team agrees:

1. **Update the published autonomy ladder** (per [`autonomy-ladder.md`](autonomy-ladder.md))
2. **Update the relevant CLAUDE.md / AGENTS.md** to reflect the new level
3. **Update permission configurations** (MCP boundaries, hooks, CI gates)
4. **Communicate to the team** — what changed, when, why
5. **Set the review date** — when will we revisit this decision?
6. **Track the metrics that drove the change** — incidents, throughput, review cycle time

If any of these steps is skipped, the autonomy change is informal — and informal changes drift.

---

## When to lower autonomy

The conversation about lowering autonomy is harder than raising it. Engineers feel demoted; the team feels distrusted. The discipline is to do it anyway when the criteria say to.

### Triggers for lowering autonomy

- **An incident.** A slop signature shipped to production at the current level. The harness didn't catch it.
- **Pattern of near-misses.** Multiple incidents barely caught at PR review; the harness is operating at the edge.
- **Harness regression.** A subagent is producing more false negatives; the slop-detector heuristics are stale; the verify command is flaky.
- **Team change.** Engineers turning over; new engineers operating at the team's level without training.
- **Quarterly review.** Even without specific incidents, the data may show drift or pattern decay.

### The conversation script — lowering autonomy

The team lead initiates after an incident or near-miss pattern:

> "I want to talk about lowering our autonomy level for [specific category] from L3 back to L2. The reason: [specific incident or pattern]. Specifically: [details].
>
> What I'm proposing:
>
> - We move [specific category] from L3 to L2 effective [date]
> - The pre-defined task whitelist for L3 is suspended for [category]
> - Engineer review at L2 applies until we've reviewed and addressed the gap
>
> This is not a permanent move. After we've addressed [specific gap], we can re-evaluate raising back to L3.
>
> I want to be clear: this is not about anyone's competence. The harness didn't catch [specific issue]; the right response is to tighten until we close the gap, not to add more discipline on top of weak infrastructure."

### What the conversation should produce

- Specific date the lower level takes effect
- Specific gaps that need addressing before re-raising
- Specific success criteria for re-raising
- Specific review date

### What lowering autonomy looks like in practice

1. **Update the published autonomy ladder**
2. **Update permissions / hooks / CI gates** to enforce the lower level
3. **Communicate the reason** — engineers should understand the harness gap, not perceive demotion
4. **Address the specific gap** — the lower level is the holding pattern while the gap is closed
5. **Track progress on closing the gap** — weekly or biweekly checkpoints
6. **Re-evaluate raising back when criteria are met**

---

## Anti-patterns

### Drift upward without explicit raise

The most common pattern. Per Ch 32 opening:

> A senior engineer tunes their permission mode looser, a junior copies it, the team norm shifts, and six months later you have agents merging to main with no human gate.

**How it manifests:**
- Auto-approve rates climbing per Anthropic's published data
- Engineers operating at higher autonomy than the team's published level
- Review fatigue producing rubber-stamp behavior
- The published ladder is dated and inaccurate

**Mitigations:**
- Quarterly review of actual operation against published ladder
- Telemetry on auto-approve rates per engineer (per [`autonomy-drift-monitoring.md`](autonomy-drift-monitoring.md))
- The certification gates discipline (per [`certification-gates.md`](certification-gates.md))

### Refusing to lower autonomy after an incident

The team has had an incident. The harness gap is real. The team's lead refuses to lower autonomy because "it would feel like punishing engineers."

**Why it's wrong:**
- The autonomy level is a property of the harness, not the engineers
- Refusing to lower means the gap remains; the next incident is more likely
- It signals that the autonomy ladder is decorative, not real

**Mitigation:**
- Explicit script that frames lowering as harness response, not engineer response
- Leadership backing for the discipline ("we lower autonomy after incidents because the harness needs to demonstrate the level")

### Raising autonomy because "the model is better now"

A new model release ships. It's better. The team lead concludes the team can operate at higher autonomy.

**Why it's wrong:**
- Per Ch 32, autonomy is harness + discipline + history + category, not just model capability
- A better model running with the same harness has the same gaps
- The Anthropic February 2026 paper shows trust drift increases with the model — the better the model, the more drift accumulates

**Mitigation:**
- The promotion criteria are about the harness and history, not the model
- Reset the certification clock on major model changes if behavior shifts

### Per-engineer autonomy variation

One senior engineer operates at L3; their team operates at L2. The engineer's reasoning: "I can handle it."

**Why it's wrong:**
- The team's level is the team's level. If senior engineers can operate at higher levels, that's an argument for raising the team's level (if the criteria are met) or a sign that the senior engineer is drifting.
- The team's onboarding gets confused: new engineers see senior engineers at L3; they assume L3 is the team's level; they operate at L3 without earning it.

**Mitigation:**
- The published ladder is the team's ladder
- Variation is allowed only when explicit (e.g., "platform engineers are certified for L3 in harness work; stream-aligned engineers are at L2")
- Even certified individuals don't operate above the team's published level for shared work

### "We'll lower autonomy after the next incident"

The team has had near-misses. The lead says "we'll address this if there's an actual incident."

**Why it's wrong:**
- "Actual incident" means customer impact, financial loss, or regulatory exposure — by then the cost is much higher
- Near-misses are the signal; ignoring them is choosing to learn from a more expensive incident later

**Mitigation:**
- Triggers for lowering autonomy include patterns of near-misses, not just incidents
- Quarterly review surfaces patterns that haven't yet produced incidents

---

## The cadence of review

### Quarterly

The team reviews the published ladder against:
- Actual operation (are engineers operating where the ladder says they should be?)
- Incidents and near-misses (any patterns?)
- Harness changes (new subagents, new hooks)
- Drift metrics (auto-approve rates per Anthropic's data, time-in-review trends)

Output: ladder unchanged, raised, or lowered for specific categories.

### Per incident

After every incident that involves AI authorship (per `incident-postmortem-templates/`), the postmortem includes the question:

> Should this incident trigger an autonomy downgrade?

If yes, follow the lowering-autonomy script above.

### Annually

Comprehensive ladder review. Re-examine the categories, the criteria, the certification gates. Adjust based on the year's data.

## What this discipline will NOT do

- Will not eliminate disagreements about whether to raise / lower
- Will not work without leadership backing for the discipline
- Will not protect against rapid model changes that shift behavior — those require mid-cycle review
- Will not catch drift if the team isn't measuring drift (per [`autonomy-drift-monitoring.md`](autonomy-drift-monitoring.md))

## Companion artifacts

- [`autonomy-ladder.md`](autonomy-ladder.md) — the published structure
- [`task-taxonomy-rubric.md`](task-taxonomy-rubric.md) — what work runs at which level
- [`autonomy-drift-monitoring.md`](autonomy-drift-monitoring.md) — detection
- [`certification-gates.md`](certification-gates.md) — the gating discipline
- `incident-postmortem-templates/harness-deficiency-checklist.md` — autonomy downgrade as one of seven mechanisms
- Ch 32 §32.4 — source
