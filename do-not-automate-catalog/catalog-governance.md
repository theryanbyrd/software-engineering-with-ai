# Catalog Governance

How to maintain the do-not-automate catalog: ownership, review cadence, when to add or remove items.

Per Ch 33:

> The catalog should live as a versioned document with named owners, reviewed quarterly. Anything not on the catalog is not automatically permitted — new domains must be classified before automation is enabled.

This file is the operational governance.

## Ownership

The catalog has a named owner. Typically:

- **Single-team org:** the tech lead or engineering manager
- **Multi-team org:** a cross-team committee (typically: VP of Engineering or designate, security lead, platform team lead, 1-2 senior IC representatives)
- **Large org:** dedicated governance committee (per `agent-autonomy-levels/certification-gates.md`'s pattern)

The owner is responsible for:
- Quarterly review
- Approving additions and removals
- Adjudicating gray-area classifications
- Communicating changes to the org

## Versioning

The catalog is versioned. Each version has:

- **Version number** (semantic-ish: 1.0, 1.1 for additions; 2.0 for major restructure)
- **Effective date**
- **Change log** describing what changed and why
- **Sign-off** from the owner

Engineers reference the version in PRs that touch catalog-relevant work, especially when applying classifications.

## Review cadence

### Quarterly

Standard review:
- Walk the catalog item by item
- For each item: still relevant? Tier still appropriate?
- New work patterns from the last quarter that need classification?
- Specific issues raised by engineers?
- Specific incidents that suggest classification changes?

### Annually

Comprehensive review:
- All of the above
- Domain-specific extensions reviewed (do new regulations or industry changes warrant extensions?)
- Cross-reference with `agent-autonomy-levels/forbidden-categories.md` (is mechanical enforcement aligned with catalog discipline?)
- Cross-reference with `customer-facing-ai-disclosure/` (does the customer-facing version match the internal catalog?)

### Per incident

Per `incident-postmortem-templates/`, postmortems include:
- Did the catalog correctly classify this work?
- Should the classification change as a result of the incident?

If yes: the catalog gets updated within 2 weeks; the change is communicated to the team.

## When to add items

A new item joins the catalog when:

1. **A new domain emerges** that wasn't classified before (e.g., team starts working on a healthcare integration; healthcare extensions apply)
2. **An incident reveals a gap** (Tier 3 work produced a Tier 1-level failure; reclassify)
3. **External requirements change** (new regulation; new compliance framework)
4. **Industry patterns evolve** (AI tooling capability changes shift the appropriate tier)

Process:
1. Engineer or manager identifies the gap
2. Brings to catalog owner with a written proposal: what, what tier, why
3. Owner reviews; convenes brief discussion if needed
4. Owner approves or returns with feedback
5. If approved: catalog updated; change log entry; team notification

Don't add items casually. Each addition increases overhead; gratuitous additions erode the catalog's signal.

## When to remove items

Items can come off the catalog when:

1. **The capability has matured significantly.** What was Tier 1 in 2024 might be Tier 2 in 2026 if AI tooling has reliably handled the category.
2. **The work pattern is no longer relevant.** A domain the team exited; a deprecated technology.
3. **Better mechanical protection exists.** If a hook or subagent now catches what the catalog was protecting against, the catalog might be able to relax (move to Tier 3).

Process:
1. Engineer or manager identifies the candidate for removal/relaxation
2. Brings to catalog owner with evidence: incident-free history, mechanical protection in place, capability evolution
3. Owner reviews; conducts due diligence (talk to relevant domain reviewers)
4. If approved: catalog updated; change log entry; team notification
5. **30-day soak:** during the soak, watch for incidents; reverse if any occur

Removing items is a higher bar than adding them. The cost of an incorrect removal is incidents.

## Communicating catalog changes

Engineers need to know about catalog changes. The communication discipline:

- **Major changes** (new tier additions, structural changes): all-hands or org-wide email
- **Minor changes** (single-item moves, clarifications): team-channel announcement; updated CLAUDE.md
- **Domain-specific extensions:** announcement to the affected teams; updated CLAUDE.md per team

Don't change the catalog silently. Engineers operating against the wrong version produce friction at best, incidents at worst.

## Catalog drift

Like the autonomy ladder (per `agent-autonomy-levels/autonomy-drift-monitoring.md`), the catalog can drift:

### Drift pattern 1 — Informal exceptions accumulate

An engineer needs to ship Tier 1 work quickly; the team allows an exception. The exception isn't logged. Three months later, the same work pattern is being done routinely without the catalog discipline.

Mitigation: exceptions require explicit approval and logging. Multiple exceptions in the same area indicate the classification might need formal review.

### Drift pattern 2 — Tier-shopping wins

Engineers consistently classify work as the lowest plausible tier. Over time, work that should be Tier 1 is treated as Tier 2; Tier 2 as Tier 3.

Mitigation: spot-check classifications quarterly. Engineers whose classifications are systematically too low get coached.

### Drift pattern 3 — Catalog ages out

Domains evolve; the catalog doesn't update. Items remain in tiers that no longer fit the current state of capabilities.

Mitigation: quarterly review forces the conversation. Don't skip the review.

### Drift pattern 4 — Org changes erode ownership

The original catalog owner leaves; new owner doesn't engage. The catalog stops being maintained.

Mitigation: ownership is a documented role; succession is part of the role's transition.

## Anti-patterns

### Catalog as marketing

The catalog is published for customers but not enforced internally. Customer audits surface the gap.

Mitigation: customer-facing disclosure (per `customer-facing-ai-disclosure/`) reflects the actual catalog, not an idealized version.

### Catalog without enforcement

The catalog exists but engineers ignore it. CODEOWNERS doesn't reflect it. Reviewers don't apply it.

Mitigation: the catalog is operationally enforced via CODEOWNERS, subagents, and review discipline. If the catalog isn't enforced, the catalog doesn't exist.

### Catalog as scapegoat

Incidents happen; the response is "the catalog should have prevented this; let's make the catalog stricter." Catalog inflation; engineering friction increases without commensurate value.

Mitigation: incident response is harness response (per `incident-postmortem-templates/harness-deficiency-checklist.md`), with catalog change as one of seven mechanisms — not the default response.

### Catalog without engineer engagement

The catalog is owned top-down without engineer input. Engineers see it as imposed; comply minimally; tier-shop.

Mitigation: engineers participate in catalog governance. Their feedback is taken seriously. The catalog evolves with the team's experience.

## What this governance will NOT do

- Will not work without leadership backing. A catalog without backing erodes.
- Will not eliminate disagreements. Quarterly review surfaces them; resolution is the work.
- Will not work as a one-time exercise. The cadence is the discipline.
- Will not protect against bad faith. Engineers determined to route around the catalog will find ways; cultural alignment is upstream.

## The first-time catalog rollout

For an org adopting the catalog for the first time:

### Month 1
- Owner named
- Initial catalog drafted using Ch 33 as starting point
- Domain-specific extensions added based on the org's industry
- Engineering leadership reviews and approves

### Month 2
- Catalog published; engineers trained
- CODEOWNERS updated to enforce Tier 1 reviewers
- Subagents updated to flag relevant categories
- First-time decision-flow conversations expected (engineers will push back)

### Month 3
- First quarterly review scheduled
- Patterns from the first 60 days reviewed; adjustments made
- Cadence settled

After the first quarter, the cadence becomes routine.

## Companion artifacts

- [`tier-1-never-autonomous.md`](tier-1-never-autonomous.md) — what the governance owns
- [`tier-2-mandatory-human-gate.md`](tier-2-mandatory-human-gate.md) — same
- [`tier-3-light-human-gate.md`](tier-3-light-human-gate.md) — same
- [`domain-specific-extensions.md`](domain-specific-extensions.md) — domain additions
- [`my-use-case-decision-flow.md`](my-use-case-decision-flow.md) — engineer-side
- `agent-autonomy-levels/autonomy-drift-monitoring.md` — adjacent discipline
- `incident-postmortem-templates/` — postmortems can trigger catalog changes
- Ch 33 — source
