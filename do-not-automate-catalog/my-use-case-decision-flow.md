# My Use Case Decision Flow

The decision flow for an engineer who thinks "but my use case is in the catalog and it shouldn't be — there's something specific about my situation."

This file exists because engineers will, predictably, try to argue out of the catalog when it's inconvenient. Some of those arguments are right (the catalog has gaps; new domains need classification). Some are wrong (the catalog is right; the engineer wants speed). The decision flow distinguishes.

## When to use this flow

- An engineer says "this work seems like Tier 1 but I think we should be able to automate it"
- A team says "the catalog forces too much overhead for our context"
- A new domain comes up that doesn't clearly map to existing tiers
- A specific implementation pattern looks like it should be exempted

## The decision flow

```
                 Is the work in the published catalog?
                         |
            +------------+------------+
           Yes                       No
            |                         |
   What tier is it in?       What tier should it be in?
            |                         |
   +--------+--------+        Use Step 6: classify-new-work
   |        |        |
  Tier 1   Tier 2   Tier 3
   |        |        |
   See     See      See
   Step 1  Step 2   Step 3
```

### Step 1 — Tier 1 work that you think shouldn't be Tier 1

Most common pushback: "this is auth code but the change is trivial; surely we can ship it without all the discipline."

Run through these questions:

#### Q1.1: What's the failure mode if this change has a subtle bug?

If the answer is "potential security incident, customer harm, regulatory exposure, financial loss" — Tier 1 stays.

If the answer is "minor inconvenience, easily reversible" — wait, that's not Tier 1. Are you sure the work is in Tier 1? Re-check.

#### Q1.2: How verifiable is the change?

If tests can prove correctness comprehensively, the failure mode is bounded by tests. Still Tier 1 in most cases (verification doesn't fully eliminate Tier 1 risk), but the gate review can be lighter.

If tests are partial or weak, Tier 1 stands firmly.

#### Q1.3: What's the cost of being wrong for 30 days?

If catastrophic (data breach, regulatory action, customer churn) — Tier 1 stands.

If recoverable but expensive (engineering hours, customer support burden) — typically Tier 1 still, but you're closer to Tier 2.

#### The verdict

Tier 1 work stays Tier 1 unless ALL of the following are true:
- Failure mode is bounded
- Verification is comprehensive
- Cost of being wrong for 30 days is low

If even one isn't true, Tier 1 stays. The engineer's job is to deal with the discipline, not to argue out of it.

### Step 2 — Tier 2 work that you think shouldn't be Tier 2

Less common but happens: "this API change is internal-only" or "this regulated codebase work is just docs."

#### Q2.1: Is the work genuinely lower-stakes than the Tier 2 framing suggests?

If the API change is genuinely internal (no external customers consume it), it might be Tier 3.

If the regulated codebase work doesn't touch the regulated portions (just docs about non-regulated parts), might be Tier 3.

If the feature flag rollout doesn't affect revenue, might be Tier 3.

#### Q2.2: Does the lower-stakes framing hold up under scrutiny?

Sanity-check:
- "Internal-only API" — is it really internal? Does any external system consume it?
- "Just docs in a regulated codebase" — does the docs change interact with any regulated logic?
- "Non-revenue-impacting flag" — could the flag's behavior be exploited to affect revenue?

If the lower-stakes framing holds: classify as Tier 3 with appropriate reasoning.

If the framing falls apart on scrutiny: Tier 2 stands.

### Step 3 — Tier 3 work that you think should be Tier 2 or Tier 1

This is the right kind of escalation: an engineer noticing that work is harder than its tier suggests.

#### Q3.1: What's surfacing the concern?

- A specific incident pattern (Tier 3 work has produced repeated bugs)
- A specific regulatory or compliance change
- A specific failure mode that the current tier doesn't account for

#### Q3.2: Is this a category-level change or a specific work-pattern change?

- **Category-level:** "Documentation should be Tier 2 because of compliance requirements" → bring to catalog governance
- **Specific work-pattern:** "This specific documentation work is regulated, so handle it as Tier 2 even though documentation is Tier 3 generally" → handle as one-off; document the reasoning

### Step 6 — Classify new work

When work doesn't clearly map to existing tiers:

#### Q6.1: What's the worst case if the work has a subtle bug that ships?

- Catastrophic / irreversible / regulated → Tier 1
- Severe but recoverable / customer-impacting → Tier 2
- Recoverable in normal flow / low-impact → Tier 3

#### Q6.2: What's the verification approach?

- Limited or expensive verification → bias to higher tier
- Comprehensive verification possible → bias to lower tier

#### Q6.3: How frequently does this work occur?

- High-frequency, well-understood patterns → bias to lower tier (the discipline of higher tier produces friction without commensurate value)
- Rare, novel patterns → bias to higher tier (newness is itself a risk factor)

#### Q6.4: Does this work touch any of the catalog's hot zones?

- Auth, billing, payments, schema migrations → Tier 1 unless very clearly orthogonal
- Public APIs, regulated codebases, customer-facing communications → Tier 2 unless clearly internal
- Default → Tier 3

#### The verdict

Default the work to a tier; document the reasoning; bring to catalog governance for formal classification at the next quarterly review.

## Common bad arguments

### "This case is special / unique"

Most cases that feel special aren't. The catalog reflects work patterns that have produced incidents at multiple companies; specific cases that look special usually fit the pattern.

Test: write down what makes the case special. If it's "we're really good engineers" or "we have great tests," that's not special — those are claims most teams make. If it's a specific structural property of the system (e.g., "this code can't reach production data because of architectural isolation"), that may be genuinely special.

### "We've never had a problem"

Absence of past incidents doesn't predict future incidents. The catalog protects against rare but severe failures; "never happened to us" is a sample size of one company, not enough to override.

### "Other companies don't have this discipline"

Some don't. Those companies appear in incident reports. The catalog reflects the empirical record; the right comparison is to companies operating at your scale and complexity, not to startups or one-off cases.

### "The discipline slows us down"

Yes. That's the trade-off. Tier 1 discipline is roughly 5-10% of engineering work; the speed-up on the remaining 90-95% from AI tooling is substantial. The Tier 1 discipline doesn't gate the throughput; it protects against catastrophic failures that would gate everything.

### "AI is better than I am at this"

Sometimes true. Doesn't change the catalog's classification. The catalog is about the cost of failure, not the probability of success.

### "We're behind competitors who don't have this catalog"

Maybe. The catalog discipline is part of why you don't have their security incidents. Whether you're "behind" depends on the scoreboard — if it's "shipped features per quarter," sometimes yes; if it's "not having a SEV-1 in 12 months," sometimes no.

## Common good arguments

### "The catalog has a gap"

Sometimes true. The catalog can't anticipate every domain or every work pattern. Engineers are the best source of identifying gaps because they encounter the patterns first.

If the engineer has a specific gap to flag: bring it to catalog governance. The catalog improves through engineer input; resisting feedback hurts the catalog.

### "This work pattern is changing"

Domains evolve. What was Tier 1 in 2024 might be Tier 2 in 2026 (e.g., AI tooling for documentation has matured significantly). What was Tier 3 in 2024 might be Tier 2 now (e.g., dependency patches now sometimes have subtle behavior changes that warrant more review).

If the engineer is observing real evolution: bring to governance review.

### "The classification is wrong for our context"

Companies have specific contexts. A generic catalog may not fit perfectly. If the engineer can articulate why the generic catalog doesn't fit their specific context: that's input for governance review and possible domain-specific extension.

## Anti-patterns

### Solo override

An engineer or manager unilaterally decides their work isn't Tier 1 and proceeds without the discipline. The bypass is informal; nobody else knows.

Mitigation: catalog overrides require documented governance review. Solo override is grounds for a discipline conversation, not a one-time exception.

### Tier-shopping

An engineer surveys the catalog looking for the lowest tier that any framing of their work fits. "This is documentation-adjacent so it's Tier 3."

Mitigation: classification is by work substance, not work framing. The reviewer checks the substance.

### Engineering around the catalog

An engineer routes around the catalog (uses personal tooling, bypasses CODEOWNERS via specific PR mechanics, etc.).

Mitigation: routing around the catalog is a discipline issue, addressed in 1:1 and possibly formally per the certification gates.

## What this decision flow will NOT do

- Will not eliminate gray cases. Some work genuinely sits between tiers.
- Will not satisfy every engineer. Some will disagree with the catalog regardless of process.
- Will not replace the discipline of the catalog. The flow is for genuine questions; the discipline is for routine application.
- Will not work without governance backing. If catalog overrides happen routinely without consequence, the catalog erodes.

## Companion artifacts

- [`tier-1-never-autonomous.md`](tier-1-never-autonomous.md) — Tier 1 details
- [`tier-2-mandatory-human-gate.md`](tier-2-mandatory-human-gate.md) — Tier 2 details
- [`tier-3-light-human-gate.md`](tier-3-light-human-gate.md) — Tier 3 details
- [`catalog-governance.md`](catalog-governance.md) — formal review process
- Ch 33 — source
