# Tier 2 — AI-Assisted with Mandatory Human Gate

The Tier 2 catalog. Per Ch 33 §33.2:

> Tier 2 (AI-assisted with mandatory human gate)

Work where AI can contribute substantially but a human gate is required at every stage. Different from Tier 1 (where humans lead and AI assists) — Tier 2 is genuine collaboration with explicit gates.

## The Tier 2 list (verbatim from Ch 33)

1. **Public API contract changes.**
2. **Feature flag rollouts with revenue impact.**
3. **Email/SMS/push notification copy or routing.**
4. **Webhook handler changes with downstream side effects.**
5. **Third-party integration credentials and OAuth scope changes.**
6. **Anything in a regulated codebase (HIPAA, SOC 2 controls, FedRAMP, ITAR)** — see Chapter 34.

## Why each item is here

### Public API contract changes

**Why:** API shape is a contract with customers. Mistakes are expensive — customer integrations break; downgrades require coordination.

**The failure mode:** an AI-authored "improvement" to a response shape changes a field from optional to required. Customer integrations that don't send the field break in production. Customer support handles a wave of complaints.

**How AI-assisted with human gate works:**
- AI assists with the contract design (drafting OpenAPI specs, generating documentation)
- AI assists with implementation
- Human reviewer (typically a senior engineer + product manager) gates the contract change at design phase
- Human review at PR time
- Backward-compatibility review explicitly required
- API versioning discipline applies (per Ch 23 if your team has one)

### Feature flag rollouts with revenue impact

**Why:** rollouts that affect revenue (pricing changes, paywall behavior, premium feature gates) need human judgment about timing, gradient, and rollback criteria.

**The failure mode:** an AI-authored feature flag change rolls a paywall to 100% of users without progressive rollout. Some users see paywalls they shouldn't. Revenue-impact incident; refunds; customer trust loss.

**How AI-assisted with human gate works:**
- AI assists with implementation of the feature flag's logic
- Human gate at the rollout decision (someone explicitly says "100% on")
- Rollback criteria documented before rollout
- Monitoring in place to catch revenue impact

### Email/SMS/push notification copy or routing

**Why:** customer-facing communications carry brand and trust. Bad copy embarrasses; wrong routing exposes data ("you sent my password reset email to my coworker").

**The failure mode:** an AI-authored notification routing change introduces a subtle bug — notifications go to the right user 99.9% of the time, but in 0.1% they go to a recently-merged user account. Privacy incident.

**How AI-assisted with human gate works:**
- AI drafts copy; human (often marketing or product) reviews tone and accuracy
- AI implements routing; human reviews logic
- Tests verify routing under realistic scenarios (account merging, deletion, etc.)
- Production rollout has gradient

### Webhook handler changes with downstream side effects

**Why:** webhooks are the integration surface with external systems. Mistakes cascade — wrong data sent to a billing partner, wrong event sent to an analytics provider.

**The failure mode:** an AI-authored webhook change sends events to a partner system in the wrong order. Partner's reconciliation fails; partner reports inconsistencies; engineering spends days reconciling.

**How AI-assisted with human gate works:**
- AI assists with handler logic
- Human review at the design and PR levels
- Integration tests against partner staging environments
- Monitoring for partner-side errors post-deployment

### Third-party integration credentials and OAuth scope changes

**Why:** credential changes affect security posture. OAuth scope expansions can grant more access than intended.

**The failure mode:** an AI-authored OAuth scope change requests `write:everything` instead of `write:specific_resource`. The change ships; the customer-facing OAuth consent screen now asks for excessive permissions. Customers complain; the company has to roll back and re-issue.

**How AI-assisted with human gate works:**
- AI assists with implementation
- Human reviewer (security team + senior engineer) gates scope changes
- Scope changes ship through a separate process from feature changes
- Customer-facing impact reviewed (consent screens, permissions explanations)

### Anything in a regulated codebase

**Why:** regulatory exposure. Per Ch 34, regulated codebases (HIPAA, SOC 2 controls, FedRAMP, ITAR) have specific compliance requirements that mistakes can violate.

**The failure mode:** an AI-authored change in a HIPAA-scoped service inadvertently logs PHI in a way that violates the BAA. Compliance audit finds the violation; remediation is months of work.

**How AI-assisted with human gate works:**
- AI assists with implementation
- Compliance-aware reviewer gates changes
- Specific compliance tests (PHI logging detection, audit trail completeness, etc.)
- Compliance team reviews quarterly

## What "mandatory human gate" means in practice

For each Tier 2 category:

- **Maximum autonomy level:** L2 (bounded autonomous task) for implementation; L1 for the design / contract level
- **Required reviewers:** senior engineer + domain reviewer (product, security, compliance, marketing as appropriate)
- **Required gate point:** explicit gate in the workflow — a PR cannot merge without specific reviewers' approval
- **Required tests:** beyond standard tests, integration tests with downstream systems where applicable

What this means for engineers:

- You can use AI tooling extensively to draft and implement
- You cannot ship without the named human reviewer's approval
- The reviewer's role is substantive (read the diff carefully) not procedural (rubber-stamp)

## Distinguishing Tier 1 from Tier 2

The line:

- **Tier 1:** the failure mode is so severe that human leadership is required at every step. AI assists with reading and suggestion; humans write the deployed code.
- **Tier 2:** the failure mode is severe but bounded; AI can write substantial code; humans gate at design and PR.

Some examples of where the line falls:

| Work | Tier | Why |
|---|---|---|
| Adding a new auth method | Tier 1 | Authentication code |
| Adding a new API endpoint that uses existing auth | Tier 2 | Public API contract; auth is reused not modified |
| Refactoring the password hashing implementation | Tier 1 | Auth code |
| Adding a new email template | Tier 2 | Customer-facing copy |
| Refactoring the email sending infrastructure | Tier 2 | Has downstream side effects |
| Changing the schema of an analytics table | Tier 1 | Schema migration |
| Adding a new tracking event to existing analytics | Tier 2 | Webhook side effects |

When in doubt: see [`my-use-case-decision-flow.md`](my-use-case-decision-flow.md).

## How to enforce Tier 2

### CODEOWNERS

- API contract files: senior engineer + product reviewer required
- Notification routing files: marketing / product reviewer required
- Regulated codebases: compliance-aware reviewer required

### Subagents

- `governance/subagents/api-contract-reviewer.yaml` — flags changes to public contracts
- `governance/subagents/regulatory-reviewer.yaml` — flags changes in regulated paths

### Required CI checks

- Backward-compatibility check for API changes
- Specific compliance checks for regulated codebases (e.g., PHI scanning)

### PR template additions

- "Does this change a public API contract? If yes, [link to API change process]"
- "Does this affect notification routing? If yes, who reviewed the routing change?"

## Common pushback

### "AI can do this autonomously; the human gate is friction"

Friction is the point. Tier 2 work is where AI tooling produces substantial leverage but the failure modes warrant the gate. The gate is the discipline that makes the leverage net-positive.

### "We don't have time for the gate"

If you don't have time for the gate, you don't have time for the incident. The empirical record on Tier 2 work without gates: subtle bugs ship; rollback is messy; trust erodes. The gate is faster than the incident.

### "Why is X in Tier 2 instead of Tier 3?"

Catalog governance question. See [`catalog-governance.md`](catalog-governance.md). The right answer might be:
- The classification is correct given the team's failure-mode history
- The classification is wrong; bring it up at the quarterly review
- The classification depends on context (some flag rollouts are revenue-impacting; others aren't)

## Companion artifacts

- [`tier-1-never-autonomous.md`](tier-1-never-autonomous.md) — adjacent
- [`tier-3-light-human-gate.md`](tier-3-light-human-gate.md) — adjacent
- [`domain-specific-extensions.md`](domain-specific-extensions.md) — for regulated industries
- [`my-use-case-decision-flow.md`](my-use-case-decision-flow.md) — when in doubt
- `agent-autonomy-levels/task-taxonomy-rubric.md` — adjacent (AI-cautious tasks)
- Ch 33 §33.2 — source
