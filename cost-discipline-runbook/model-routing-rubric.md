# Model Routing Rubric — Haiku vs Sonnet vs Opus

When to use which model. Per Ch 29 §29.6 (common cost blowup patterns):

> Opus on routine tasks. Route to Sonnet by default; promote to Opus only on demonstrated need.

This file is the operational rubric. Calibrated against the Claude family as of 2026; adjust to your specific model lineup.

## The cost asymmetry

Approximate input/output token costs (verify current pricing):

- **Haiku 4.5:** ~$0.20 / $1.25 per million tokens (input/output)
- **Sonnet 4.6:** ~$3 / $15 per million tokens
- **Opus 4.7:** ~$15 / $75 per million tokens

Opus is roughly 5× Sonnet and 60-75× Haiku. Routing matters because the cost ratios are so steep.

## The default

Per Ch 0 (TL;DR) and Ch 29 §29.6:

> Use Sonnet 4.6 as the daily driver, Opus 4.7 for architecture/security/migrations, Haiku 4.5 for grunt work and routing.

The rule of thumb:

- **Sonnet** is the default. ~70-80% of work
- **Haiku** for high-volume cheap-task work. ~10-15% of work
- **Opus** for narrow high-stakes work. ~5-10% of work

If a team's mix doesn't roughly match this distribution, investigate why.

## When to use Haiku

Haiku is for high-volume cheap-task work where Sonnet would be overkill. Specifically:

- **Routing decisions.** "This issue is about X; route to team Y." Haiku is sufficient and 60× cheaper.
- **Classification.** "This PR is in category {feature, bug-fix, refactor}." Sufficient.
- **Simple summarization.** "Summarize this 500-word issue in 50 words."
- **Format conversions.** "Convert this CSV to JSON."
- **Quick lookups in structured docs.** "What does the X table contain?"
- **First-pass slop signature detection.** Heuristic-style checks (per `scripts/slop-detector.py`).

When NOT to use Haiku:
- Substantive code review (Sonnet minimum)
- Spec writing or design (Sonnet minimum)
- Multi-step reasoning (Sonnet minimum)
- High-stakes decisions (Sonnet for stakes >$1K of impact; Opus for higher)

### Calibration

If you're using Haiku for >25% of your spend, that's healthy. If <5%, you're probably leaving money on the table — there are routing/classification tasks that should be on Haiku.

## When to use Sonnet (the default)

Sonnet is the daily driver. Per Ch 29 §29.6, route to Sonnet by default; promote to Opus only on demonstrated need.

Specifically, Sonnet is appropriate for:

- **Most code generation.** Feature implementation, bug fixes, refactors.
- **Code review.** Substantive review of human or AI-authored PRs.
- **Spec writing.** Translating vague requirements into agent-ready specs.
- **Documentation generation.** From code or from issue threads.
- **Test generation.** Including characterization tests for legacy code (per Ch 11 Rule Zero).
- **Most subagent work.** Security-reviewer, performance-reviewer, migration-reviewer at default.
- **Pair-driving sessions.** Substantive partnership with a human.
- **Multi-step reasoning** where the steps are individually within typical complexity.

When NOT to use Sonnet:
- Trivial classification (Haiku is cheaper, equivalent quality)
- Architecture decisions affecting many systems (Opus is worth the cost)
- Security-critical reviews where the cost of being wrong is severe (Opus for high-stakes; Sonnet with extra human review for moderate stakes)

### Calibration

If you're using Sonnet for >85% of your spend, you may be over-using it (some tasks should be Haiku). If <60%, you may be under-using it (Opus or Haiku usage is over-pulled).

## When to use Opus

Opus is for narrow high-stakes work. The cost is justified when the stakes are high enough.

Specifically:

- **Architecture decisions** affecting multiple systems. The cost of a bad architecture decision is months of rework; Opus's marginal cost is justified.
- **Security-critical review.** Auth, authz, billing, payments, permissions code (per `agent-autonomy-levels/forbidden-categories.md`). Sonnet's mistakes here can be catastrophic.
- **Migration planning.** Cross-system migrations where understanding the system holistically matters.
- **Complex debugging.** When the bug spans multiple systems and Sonnet has hit a wall.
- **Critical incident response.** When you're 30 minutes into a SEV-1 and need the best reasoning.
- **Cross-system reasoning** that genuinely requires the model's larger context window.

When NOT to use Opus:
- Routine code generation (Sonnet is adequate; Opus is wasted)
- Simple bug fixes (Sonnet)
- Documentation (Sonnet)
- Anything that runs in a tight loop (Opus in a retry loop is the "common cost blowup pattern" Ch 29 §29.6 names)

### Calibration

If you're using Opus for >15% of your spend, you may be over-using it. If 0%, you may be under-using it (some work warrants Opus).

## How to surface routing to engineers

The rubric is operational only if engineers apply it. Several approaches:

### Approach 1 — Default model in tool config

Set the team's default model to Sonnet. Engineers must explicitly opt into Opus or Haiku per session.

Pros: easy default; engineers don't think about it for routine work.
Cons: opt-in for Haiku means engineers underuse it.

### Approach 2 — Skill-based routing

Per Ch 29 §29.4, route by task category in the LLM gateway. The gateway has rules:
- Tasks tagged `routing` → Haiku
- Tasks tagged `code-review` → Sonnet
- Tasks tagged `architecture-review` → Opus
- Default → Sonnet

Pros: routing is automatic; engineers don't need to choose model.
Cons: requires gateway infrastructure; tagging discipline matters.

### Approach 3 — Per-skill model assignment

Each skill (per `skills/`) has a recommended model in its frontmatter:

```yaml
recommended_model: sonnet  # or haiku, opus
```

The harness invokes the skill with the recommended model. Engineers override only with explicit reason.

Pros: routing is encoded in the canonical patterns; updates propagate.
Cons: requires skill curation; new tasks need explicit model assignment.

### Approach 4 — Subagent tier discipline

Subagents have explicit tier:
- L1 subagents (broad coverage, low cost): Haiku
- L2 subagents (substantive review): Sonnet
- L3 subagents (security, architecture): Opus or Sonnet+escalation

Per Ch 22 §22.3 (the two-tier review): L1 is a floor catching the obvious; L2 catches the substantive.

Most teams use a combination. The platform team builds the gateway / skill / subagent infrastructure that operationalizes the rubric.

## Common routing failure modes

Per Ch 29 §29.6:

### Opus on routine tasks

Engineer configures their session for Opus by default. Every code edit, every comment generation, every debug session goes through Opus. Per the data, this is a 5-15× cost multiplier with marginal capability gain.

Mitigation: default to Sonnet at the tool / gateway level; require explicit opt-in for Opus.

### Agents in tight retry loops

Agent encounters an error; retries; encounters error; retries. Each retry costs Opus-tier money. Per Ch 29 §29.6: "Cap retries at 3; fail loudly."

Mitigation: gateway-level retry budgets per tool; exponential backoff; loud failure on budget exhaustion.

### Runaway long-running tasks

Agent invocation runs for hours, generating tokens continuously. Per Ch 29 §29.6: "Time-box every agent invocation. Default 15 minutes."

Mitigation: gateway-level time budgets per invocation; auto-termination.

### Context bloat

Engineer's CLAUDE.md is 12,000 tokens; their AGENTS.md adds another 8,000; their `llms.txt` adds 5,000. Every session pays the input cost. Per Ch 29 §29.6: "Trim context aggressively; use skills (loaded only when invoked) instead of bloated CLAUDE.md."

Mitigation: skill-based architecture; CLAUDE.md focused on team-wide invariants; AGENTS.md per-repo focused; per-skill content loaded only when invoked.

### Cache misses

Stable system prompts and tool definitions should be cache-eligible. If they're not, the team is paying full cost for content that should be cached.

Mitigation: review cache hit rates per Ch 29 §29.6: "A workload that should hit cache but isn't is a bug."

### Tokenizer changes

Per Ch 29 §29.6: "Opus 4.7's new tokenizer can add up to 35% effective cost vs Opus 4.6. Monitor effective cost per call."

Mitigation: track tokens-per-call as a metric, not just dollars-per-call. Detect drift when the model version changes.

## What this rubric will NOT do

- Will not work without telemetry. You can't route effectively without measuring.
- Will not work in cultures where engineers ignore the routing. Cultural alignment is upstream.
- Will not eliminate Opus usage. Some work warrants it; the rubric is about appropriateness.
- Will not protect against vendor pricing changes. If Opus's price doubles, the rubric still applies but the math shifts; recalibrate.

## Companion artifacts

- [`token-budgets-by-team.md`](token-budgets-by-team.md) — the budgets the routing supports
- [`anomaly-detection-workflow.md`](anomaly-detection-workflow.md) — what catches when routing fails
- [`cost-attribution-per-pr.md`](cost-attribution-per-pr.md) — visibility into model mix per PR
- `vendor-procurement-runbook/` — adjacent (the contract side)
- Ch 29 §29.6 — source
