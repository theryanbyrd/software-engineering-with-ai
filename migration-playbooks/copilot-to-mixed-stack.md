# Copilot → Mixed Stack Playbook

The second-most-common scenario in 2026: a team has GitHub Copilot (often Enterprise) and is adding Claude Code (or another agentic tool) alongside it. Unlike the Cursor migration, this is rarely a "consolidation" — Copilot's strengths and Claude Code's strengths don't overlap heavily.

**The book's editorial position:** Most teams keep Copilot for inline completions and add an agentic tool for outer-loop work. Choosing between them is rarely the right call; running both is.

> Most teams keep Copilot for inline completions and add Claude Code for agentic work, rather than choose between them.
>
> The exception is cost. Copilot Enterprise plus Claude Code Max for everyone gets expensive fast at scale. Many mid-size teams settle on Copilot Business for everyone and Claude Code Max for the senior tier and the platform team.
>
> — Ch 53 §53.3

This playbook covers the addition (not migration) of an agentic tool to a Copilot-using team.

## Who this playbook is for

- VP of Engineering deciding whether and how to add agentic tooling
- Platform team lead executing the rollout
- The CFO managing dual-tool spend
- Hiring manager whose team is affected

## Read first

- [`pre-migration-checklist.md`](pre-migration-checklist.md) — the additions case is lower-risk than full migration but still needs preconditions
- Ch 53 §53.3 of the handbook
- Ch 38 — vendor risk and procurement (review before adding any new tool)

## When you should NOT add a second tool

- Your team is fewer than 15 engineers. You don't yet have the volume to amortize a second tool's harness cost.
- You're already significantly over budget on AI tooling. Story 005 in war-stories.
- Your team has not gotten consistent value from Copilot yet. Adding a second tool when the first isn't producing ROI doesn't fix the underlying issue.
- You're in the middle of a layoff or reorg. Sequence.

If any of these apply, your work is to make Copilot work better, not to add a second tool.

## Phase 0 — Preconditions (Week -4 to 0)

1. **Run the pre-migration checklist** (treating "addition" as "migration" — the team-conversation considerations apply equally).
2. **Document the budget split.** Decide upfront: Copilot for everyone + Claude Code for senior tier (most common), or both for everyone (more expensive). The decision is harder to revise once announced.
3. **Identify the senior tier.** If you're going with the split model, who gets the senior license? Document the criteria; write them down so the decision isn't political.
4. **Brief the CFO.** This is dual licensing forever, not a temporary parallel period. Make sure the CFO understands.
5. **Run procurement on the new tool.** Security review, data classification, contract terms. See Ch 38.

## Phase 1 — Initial introduction (Months 1-2)

### Week 1 — Announcement

The framing is fundamentally different from the Cursor playbook. There is no implied threat to anyone's existing tool. The conversation is purely additive.

**The all-hands message.** See [`team-conversation-scripts.md`](team-conversation-scripts.md) §4 for verbatim. Key elements:

- *"We're adding [Claude Code / Codex / agentic tool X] alongside Copilot. Copilot is staying. The new tool fills a gap Copilot doesn't address."*
- Specific gap: agentic workflows, multi-step changes, GitHub Action integrations, the planner / implementer / reviewer pattern.
- Who gets it: senior tier and platform team initially. Broader rollout after proof of value.
- Cost: shared transparently. *"Adding $X/year for [N] seats; we'll review at [Q+2]."*

### Week 2 — Senior tier onboarding

The 5-15 engineers in the senior tier get access. They are NOT migration champions in the Cursor-playbook sense — Copilot isn't being replaced — they are early adopters validating that the new tool earns its keep.

Each early adopter is asked to:
- Use the new tool on real work for 4-6 weeks
- Document one or two scenarios where the new tool did something Copilot couldn't (or did it significantly better)
- Document one or two scenarios where the new tool failed and Copilot would have been the better tool

The output is the data for the broader-rollout decision.

### Weeks 3-8 — Harness investment

The platform team builds the harness for the new tool. Different work from the Cursor migration: there's no `.cursorrules` to translate, but Copilot's harness is much thinner, so you're often building from scratch.

Work items:
- CLAUDE.md / AGENTS.md for the codebase
- Initial skills (use the `skills/` library from this repo as starter)
- Hooks for protected paths and bash firewall
- CI integration (`scripts/ai-readiness-audit.py`, etc.)
- Verify command if not already present

The senior tier is using the new tool while this is being built. Their feedback shapes the harness.

## Phase 2 — Decision point (Month 3)

### Week 9-10 — Adoption assessment

The data from Phase 1:
- Did the senior tier use the new tool for the scenarios where Copilot was inadequate? (Yes = the gap is real)
- Did productivity for the senior tier go up, down, or flat? (Up = the tool earns its keep at this scope; flat = mixed signal; down = stop)
- What % of senior tier use is on outer-loop / agentic work vs. inner-loop completion? (Should be 80%+ outer-loop; otherwise the tool is being used wrong)

### Week 11-12 — The broader rollout decision

Two paths:

**Path A — Expand to all engineers (30-50% of cases):**
If the new tool clearly earns its keep at the senior tier and engineers below the senior tier are asking for access, expand. Be transparent about cost. Plan to evaluate value at each tier independently — the senior-tier ROI does not automatically extend.

**Path B — Stay at senior tier (40-60% of cases):**
The most common outcome. The new tool's value is concentrated at the senior tier where outer-loop work is most common. Mid-level engineers do mostly inner-loop work where Copilot is sufficient. Hold the line; revisit annually.

**Path C — Reverse the addition (5-10% of cases):**
The new tool didn't earn its keep even at the senior tier. Cancel before the renewal cycle. Document what didn't work for next time.

## Phase 3 — Steady state (Month 4+)

If Path A or B:

### Quarterly cadence

- Cost review with finance: per-team spend, per-engineer cost, productivity correlation
- Senior tier retro: still earning its keep? Any patterns where one tool is clearly better and team should standardize?
- Adoption metrics: are non-tier engineers using their access? If a non-tier engineer has been given access and isn't using it, reclaim and redistribute

### Vendor management

Don't sign multi-year contracts for either tool. The market shifts every 6-12 months.

When Copilot or the new tool releases a major capability change:
- Run the benchmark suite (`benchmarks/`) to verify quality
- Check if the capability changes the value calculation
- Be prepared to reverse course if the calculus changes significantly

## Variants

### Sovereign / regulated environment

If you have data classification requirements (CMMC, ITAR, PHI), the additional tool's data handling matters more than its productivity. Verify before procurement; do not start the rollout until the legal/compliance review is complete.

### Heavy frontend team

Frontend teams often get less from Copilot Enterprise's stronger surfaces (PR summaries, code analysis on full repos) and more from the inline-completion side. The new tool's agentic workflows are less differentiated for pure frontend work. Consider this when sizing the senior tier.

### Heavy infrastructure / DevOps team

Ops-heavy teams often get the most from agentic tools (multi-step infra changes, alert triage, runbook automation) and less from Copilot's code-focus. For these teams, the senior-tier might be inverted: most ops engineers get the new tool, only the application code reviewers get Copilot.

## What to do if it goes wrong

### The senior tier doesn't use the new tool

- Investigate the harness. Often the gap is missing skills, hooks, or CLAUDE.md investment, not the tool itself.
- Talk to senior engineers individually. Are they not using it because it's bad, or because they didn't get around to it?
- If after 8 weeks of investment the senior tier still isn't using the tool, it's not the right tool. Cancel before the renewal cycle.

### Cost overruns hit at month 6

- Pull the cost dashboard. Per-team breakdown.
- Identify any engineers in the senior tier who aren't using the new tool. Reclaim seats.
- Renegotiate the budget process, not the budget itself. Story 005 again.

### A new model release changes Copilot's capability significantly

- Run the benchmarks against both tools.
- If Copilot's new capability covers what the new tool was added for, consider sunsetting the new tool's seats at renewal.
- Don't reverse mid-quarter on a single news item. Wait for benchmark data.

## Common failure modes

- **Adding the new tool without harness investment.** Engineers get access, find the experience underwhelming, never form the habit. The harness investment is what makes the new tool earn its keep.
- **Treating the new tool as a Copilot replacement.** It isn't. Different tools, different surfaces. Engineers who try to replace inner-loop tab completion with agentic workflows have a bad time.
- **Making access a status symbol.** "The senior tier gets access" can become political. Document the criteria; apply them objectively.
- **Underbudgeting the platform team.** Building the harness for the second tool is real work. If the platform team is at capacity, sequence — finish current work before adding tool.

## Companion artifacts

- `skills/` — starter skills for the new tool
- [`team-conversation-scripts.md`](team-conversation-scripts.md) §4
- `exec-kit/approved-tooling-matrix-template.xlsx` — for the data classification side
- `benchmarks/` — to verify quality and detect regressions
- `governance/prompt-injection-test-suite/` — verify the new tool's harness security
