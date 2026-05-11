# The "Do Not Automate" Catalog

The explicit catalog of work that should NEVER be automated. Direct implementation of Chapter 33 of [_Software Engineering with AI: A Practical Handbook for the Claude Code Era_](https://www.linkedin.com/in/ryanbyrd) by Ryan Byrd, with cross-references to Ch 32 (autonomy levels) and Ch 34 (data classification).

The book's framing:

> The catalog is the organization's negative space — the things that AI does not touch without a human in the loop. Tier it by reversibility and blast radius.
>
> — Ch 33 opening

This folder is the operational catalog. It pairs with `agent-autonomy-levels/forbidden-categories.md` but is broader: forbidden-categories is the L5 list (capabilities the agent should never have); this catalog is the work patterns that should never be fully automated, even when the capability exists.

## What's in here

| File | Purpose |
|---|---|
| [`tier-1-never-autonomous.md`](tier-1-never-autonomous.md) | The Tier 1 catalog — never autonomous, always human-led |
| [`tier-2-mandatory-human-gate.md`](tier-2-mandatory-human-gate.md) | The Tier 2 catalog — AI-assisted with mandatory human gate |
| [`tier-3-light-human-gate.md`](tier-3-light-human-gate.md) | The Tier 3 catalog — AI-led with light human gate |
| [`domain-specific-extensions.md`](domain-specific-extensions.md) | Healthcare, financial services, defense / public sector additions |
| [`my-use-case-decision-flow.md`](my-use-case-decision-flow.md) | The decision flow when an engineer thinks "but my case is in the catalog and shouldn't be" |
| [`catalog-governance.md`](catalog-governance.md) | How to maintain the catalog: ownership, review cadence, when to add/remove items |

## The book's three tiers

Per Ch 33:

### Tier 1 — Never autonomous, always human-led

The work where automation is forbidden regardless of harness maturity, engineer experience, or vendor capability. Examples: authentication code, billing, cryptographic key management, schema migrations affecting production data.

### Tier 2 — AI-assisted with mandatory human gate

The work where AI can contribute substantially but a human gate is required at every stage. Examples: public API contract changes, feature flag rollouts with revenue impact, regulated codebase changes.

### Tier 3 — AI-led with light human gate

The work where AI can lead and the human review is light (catch obvious issues, ensure scope discipline). Examples: documentation, internal-only scripts, type fixes, dependency security patches with no API change.

## How this catalog differs from `agent-autonomy-levels/forbidden-categories.md`

| | `agent-autonomy-levels/forbidden-categories.md` | This catalog |
|---|---|---|
| **Scope** | The L5 capabilities the agent should never have | The work categories that should never be fully automated |
| **Enforcement** | Mechanical (MCP boundaries, hooks, IAM scopes) | Mostly procedural (CODEOWNERS, mandatory review, certification gates) |
| **Examples** | Direct production database write access; tokens with org-wide scope | Authentication code review; billing logic changes; schema migrations |
| **Failure mode** | Catastrophic blast radius from agent action | Subtle errors, regulatory exposure, customer harm from automation that should have had human judgment |

The two are complementary. A team that has the L5 forbidden categories enforced still needs the do-not-automate catalog because:
- An engineer can be operating at L1/L2 (allowed by the autonomy ladder) but on Tier 1 work (which still requires human-led approach)
- Some work patterns warrant human leadership regardless of agent capability

## Who this is for

- **Engineering managers** establishing the catalog for their teams
- **VP of Engineering / CTO** publishing the org-wide catalog
- **Tech leads** answering "can we automate this?" questions from engineers
- **Compliance / regulatory leads** for industry-specific extensions
- **Engineers** wondering whether a specific task is in scope for their AI tooling

## Read first

- Ch 33 — the source chapter
- Ch 32 — the autonomy ladder (closely related)
- Ch 34 — data classification (informs Tier 2 regulated codebase work)
- `agent-autonomy-levels/forbidden-categories.md` — adjacent but narrower
- `agent-autonomy-levels/task-taxonomy-rubric.md` — adjacent (work-to-autonomy-level mapping)

## What this catalog WILL do

- Make the negative space explicit. Engineers can look up "is this in the catalog?"
- Surface the reasoning. Engineers understand WHY each item is in its tier.
- Provide the decision flow when a task seems to be in the catalog but the engineer believes it shouldn't be.
- Encode the team's discipline so it survives turnover.
- Support customer audits and compliance reviews ("here's our explicit do-not-automate catalog").

## What this catalog will NOT do

- Will not eliminate every gray case. Some work sits between tiers; the catalog establishes anchors, not absolute decisions.
- Will not protect against engineers who route around the catalog. Cultural alignment is upstream.
- Will not work without ownership. An unowned catalog drifts; per [`catalog-governance.md`](catalog-governance.md), assigned ownership and quarterly review are required.
- Will not work in cultures that treat the catalog as obstacle. The catalog reflects the team's chosen discipline; without alignment, it's decorative.

## How this folder fits with adjacent material

| Need | Where to look |
|---|---|
| Mechanical enforcement of L5 capabilities | `agent-autonomy-levels/forbidden-categories.md` |
| Decision rubric for autonomy level per task | `agent-autonomy-levels/task-taxonomy-rubric.md` |
| Customer-facing disclosure of the catalog | `customer-facing-ai-disclosure/security-questionnaire-answers.md` |
| Onboarding engineers to the catalog | `ai-tooling-onboarding-curriculum/` (this round) |
| Postmortem template referencing the catalog | `incident-postmortem-templates/postmortem-template.md` |

## The core principle

Per Ch 33:

> The catalog should live as a versioned document with named owners, reviewed quarterly. Anything not on the catalog is not automatically permitted — new domains must be classified before automation is enabled.

The default is "we haven't decided yet" → human-led until classified. New work that doesn't fit existing tiers gets classified before automation. The catalog grows as the org's scope grows.

## Companion artifacts

- `agent-autonomy-levels/` — adjacent governance
- `incident-postmortem-templates/` — postmortems reference the catalog
- `customer-facing-ai-disclosure/` — customer-facing version
- `ai-tooling-onboarding-curriculum/` — engineers learn the catalog as part of L1 cert
- Ch 33 — source
