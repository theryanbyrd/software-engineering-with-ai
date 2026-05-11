# When to Switch Primary Model

The decision framework. Per Ch 26 §26.5:

> Switch when a new model is markedly better on your internal benchmark — not the public one. "Markedly" means at least 5 points on aggregate score and a clear pattern across multiple task types in your evaluation set. A 1-2 point bump is noise; a 5+ point bump is signal.

This file is the operational application of that rule, plus the broader decision framework that includes cost, capability profile, and migration overhead.

## The 5-point rule

The single most important rule:

**Aggregate score on the internal benchmark must improve by 5+ points to warrant a switch.**

Why 5 points:
- Below 5: within statistical noise for benchmarks of 30-100 tasks
- Below 5: within evaluator scoring variability (different reviewers grade the same task differently)
- Below 5: typical run-to-run variance for the same model on the same benchmark

5+ points means the new model is genuinely better in a way that survives noise.

## Beyond the 5-point rule

5 points is necessary but not sufficient. Also required:

### A clear pattern across task types

Per Ch 26 §26.5: "a clear pattern across multiple task types in your evaluation set."

What this rules out:
- The new model wins by 8 points but only because it crushes one specific task type (e.g., it's much better at Python typing but no different on the other 90% of the work). Specialized improvement isn't justification for primary switch — it's justification for adding the model to the lineup for that work type.
- The new model wins on the easy tasks but is the same on the hard tasks. The hard tasks are where capability matters most.

What this requires:
- Improvement visible across at least 4 of the major task categories (bug fixes, features, refactors, tests, etc.)
- Improvement on T2 and T3 work, not just T1

### Cost economically defensible

A model that's 8 points better but 3× more expensive isn't a slam-dunk switch. Run the math:

- **Current primary**: 79% benchmark score, $X/month
- **Candidate**: 87% benchmark score, $3X/month (3× more expensive)
- **Cost-adjusted improvement**: 8 points / 3× = ~2.7 points per cost unit

For high-stakes work where capability matters more than cost, the more expensive model may be correct. For routine work, often not.

The conversation: is the additional capability worth the additional cost? Sometimes yes, sometimes no.

### Migration cost manageable

Switching has overhead:

- **Tooling updates**: gateway config, IDE plugin defaults, skill model assignments, subagent model assignments
- **Harness adaptation**: CLAUDE.md / AGENTS.md may need updates (different models respond differently to the same prompts)
- **Engineer retraining**: muscle memory is real; engineers need to learn the new model's quirks
- **Testing**: the team's verify pipeline and PR workflows may need re-validation

For a major switch, expect 2-4 weeks of platform team time and 4-8 weeks of engineer adjustment.

If the gain is 5 points on benchmark but the migration is 8 weeks of platform team time that pushes other priorities — sometimes worth it, sometimes not.

## The decision framework

Combine the criteria:

| Criterion | Weight |
|---|---|
| **Benchmark score improvement** (aggregate) | Required: 5+ points |
| **Pattern across task types** | Required: 4+ categories |
| **Cost** | Factor: justifiable given capability |
| **Migration cost** | Factor: manageable given timeline |
| **Capability profile match** | Factor: closes capability gaps the team has |

If aggregate < 5 → don't switch (it's noise)
If aggregate ≥ 5 but only 1-2 categories → don't switch primary; consider adding to lineup for those categories
If aggregate ≥ 5 and pattern is clear and cost/migration are manageable → switch

## Switching scenarios

### Scenario A — Vendor releases a new flagship

Most common scenario. Anthropic releases Claude Sonnet 5; you're on Sonnet 4.6.

Decision flow:
1. Run internal benchmark on Sonnet 5 within 2-4 weeks of release
2. Compare aggregate and per-category scores
3. Compare cost (often: similar or lower for newer flagship)
4. Migration cost: usually low (same family; harness compatibility good)
5. Decision: if 5+ point improvement with pattern, switch within the next quarter

### Scenario B — Different vendor's model is markedly better

Less common but happens. OpenAI or Google or another vendor releases a model that significantly outperforms your current primary.

Decision flow:
1. Run internal benchmark
2. Migration cost: usually high (different family; harness needs adaptation; tooling integration)
3. Account for: vendor risk (different vendor's incident history, support quality, contract terms)
4. Decision: requires substantially more than 5 points to justify cross-vendor switch — typically 8-10+ point improvement plus operational comfort with the vendor

### Scenario C — Smaller / cheaper model becomes capable

A previously inadequate cheap model has improved. Haiku 4.5 used to be too weak for some work; Haiku 4.6 might be sufficient.

Decision flow:
1. Run internal benchmark; compare to current default
2. Per-category breakdown is critical: the cheaper model probably ties on some categories and lags on others
3. Decision: don't switch primary; update routing to send specific work types to the cheaper model. This is a routing update, not a primary switch.

### Scenario D — Specialized model emerges

A model emerges that's specifically tuned for one work type your team does heavily.

Decision flow:
1. Run internal benchmark, focused on the relevant category
2. Compare per-category score (not aggregate)
3. Decision: add to lineup for that work type; primary stays the same

### Scenario E — Pricing change

Pricing on a model the team already uses changes significantly (up or down).

Decision flow:
1. No benchmark needed — capability hasn't changed
2. Cost analysis: does the new pricing change the routing math?
3. Decision: routing update, possibly significant. Per `cost-discipline-runbook/model-routing-rubric.md`.

### Scenario F — Vendor announces deprecation

The current primary's vendor announces deprecation date.

Decision flow:
1. Decision is forced by deprecation date
2. Run benchmark on the recommended successor model
3. Compare for context, not for decision (the deprecation forces action)
4. Time the migration to the deprecation timeline; don't wait until the last week

## When NOT to switch

### "The new model is 2 points better"

Within noise. Don't switch.

### "The new model is 6 points better but only on one category"

Add it to the lineup for that category; don't switch primary.

### "The vendor's marketing is compelling"

Marketing isn't data. Run the benchmark.

### "Other companies are switching"

Other companies have different work mixes. Their switches don't predict yours.

### "The new model is 8 points better but 4× more expensive"

Cost math may not justify the switch unless the capability gap is closing critical work the team can't do otherwise.

### "The new model is from a vendor we don't have a contract with"

Vendor risk is real. Per `vendor-procurement-runbook/`, cross-vendor switches have additional considerations.

### "The internal benchmark hasn't been run on the new model yet"

Don't decide without data. If the benchmark hasn't been run, run it before deciding. If urgency is real (e.g., deprecation), run a smaller version of the benchmark immediately.

## When TO switch

The pattern that justifies switching:

- Internal benchmark shows 5+ point aggregate improvement
- The improvement is visible across 4+ task categories
- The improvement is visible on T2 and T3 work, not just T1
- Cost is similar, lower, or justifiably higher given capability
- Migration cost is manageable in the quarter ahead
- The vendor (current or new) is in good standing per procurement discipline

When all these line up, switch within the next quarter.

## Communicating the decision

A switch is a real change for the team. Communication:

- **Announcement** when the decision is made (not when the change takes effect)
- **Specific timeline** (rollout dates, deprecation dates for the old model)
- **Why** (specific benchmark data; not "the new model is better")
- **What changes** for engineers (defaults, tooling, anything they need to do)
- **What doesn't change** (the routing rubric structure, the discipline)

If the team learns about the switch through tooling changes appearing without notice, the change is mismanaged.

## What if you're wrong

Sometimes a switch turns out to be a mistake. The new model is worse in production than the benchmark suggested. Or the migration cost is higher than expected. Or capability gaps emerge that weren't visible in the benchmark.

Mitigations:

- **Phased rollout**: switch one team at a time over 4-6 weeks; monitor real PR throughput and quality
- **Parallel run**: keep both models available for 30-60 days; allow engineers to fall back
- **Reversion plan**: documented before the switch — what's the trigger for reverting, what's the process
- **Don't sign long contracts**: per Ch 26 §26.5, "do not sign long-term token contracts"; flexibility matters

If the switch is genuinely worse, revert. The benchmark data is wrong; investigate why; update the benchmark; try again next quarter.

## Companion artifacts

- [`internal-benchmark-construction.md`](internal-benchmark-construction.md) — the foundation
- [`quarterly-model-lineup-review.md`](quarterly-model-lineup-review.md) — when this decision is made
- [`routing-policy-update-process.md`](routing-policy-update-process.md) — what happens after
- `cost-discipline-runbook/model-routing-rubric.md` — adjacent (the routing this updates)
- `vendor-procurement-runbook/renewal-discipline.md` — adjacent vendor considerations
- Ch 26 §26.5 — source
