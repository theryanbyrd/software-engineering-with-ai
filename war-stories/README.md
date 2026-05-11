# War Stories

Anonymized field reports from real engineering organizations rolling out AI tooling. The seed stories are drawn from Appendix L of [_Software Engineering with AI: A Practical Handbook for the Claude Code Era_](https://www.linkedin.com/in/ryanbyrd) by Ryan Byrd. New stories arrive as community contributions.

The point is not the specific tooling — the names of tools change quarterly. The point is the **shape** of what worked and what didn't, because the same shape repeats across organizations.

## What's in here

| File | Setting | The lesson |
|---|---|---|
| [`001-pilot-retrospective.md`](001-pilot-retrospective.md) | Mid-size company running a 3-workstream pilot | Compounding harness across workstreams |
| [`002-the-12-percent-plateau.md`](002-the-12-percent-plateau.md) | 110-engineer fintech | Throughput gains plateau; renegotiate from data |
| [`003-the-skipped-harness-incident.md`](003-the-skipped-harness-incident.md) | 45-engineer health-tech startup | The first 30 days of harness investment cannot be skipped |
| [`004-the-cursor-migration-mandate.md`](004-the-cursor-migration-mandate.md) | 70-engineer SaaS company | Run parallel, then converge |
| [`005-the-cfo-token-cap.md`](005-the-cfo-token-cap.md) | 90-engineer B2B company | Surprise budget caps push spend underground |

## How to read these

Each story follows the same structure:

1. **Setting** — anonymized: company size, industry vertical, role of the protagonist
2. **Situation** — what they were trying to do
3. **What happened** — the events
4. **What they did** — recovery actions
5. **Outcome** — where they ended up
6. **Lesson** — the generalizable takeaway
7. **What would have prevented it** — the counter-example

The lessons are listed at the end. If you're short on time, read the lessons table above and the Setting + Lesson sections of any story that resonates with your situation.

## How to contribute a story

We welcome anonymized contributions from VPs, CTOs, platform leads, and senior engineers who have run AI rollouts in mid-size organizations. The bar is high because these stories shape how the next reader thinks about their own situation.

**To submit:**

1. Copy [`_TEMPLATE.md`](_TEMPLATE.md) to a new file with the next sequential number (e.g., `006-your-story-slug.md`).
2. Fill in every section. Stories that skip sections rarely teach the lesson cleanly.
3. **Anonymize.** See the rules below. Anonymization is not optional.
4. Submit a PR. Maintainers review for anonymization compliance and editorial quality.

### Anonymization rules

These are non-negotiable. Stories that violate any of these are rejected.

**Always remove:**
- Company name, even partial. "A 110-engineer fintech," not "Acme Financial."
- Personal names, even initials. "The VP of Engineering," not "M.R."
- Specific products or features that uniquely identify a company.
- Specific dollar amounts that pinpoint a deal or contract. Use ranges: "low-to-mid six figures," not "$430K."
- Specific dates beyond month + year. "Q2 2026," not "April 14, 2026."
- Geographic specificity beyond country. "A US-based startup," not "Boston-based."
- Customer names or industries-of-customers if they could identify the company.

**Modify or fictionalize:**
- Specific stack details if they're a fingerprint. "A Python web service" is fine; "Python 3.11.4 on AWS Fargate with FastAPI 0.107 and SQLAlchemy 2.0.21" is identifying.
- Org structure quirks. "The platform team" is fine; "The Foundation Platform — Tooling Cluster — DX Pod" is identifying.

**Keep:**
- The shape of the failure or success — that's the point.
- General industry vertical (fintech, health-tech, B2B SaaS, ad-tech, etc.).
- General company-size band (10-30, 30-80, 80-200, 200-500, 500+).
- The chronology of events at a coarse grain.

### Editorial bar

- **Specific lessons over generic morals.** "Compress the harness phase and you pay 6 months later" beats "Plan carefully."
- **Honest about what didn't work.** Stories where everything went right are rarely useful.
- **Concrete recovery actions.** Tell the next reader what to actually do.
- **Counter-example.** What would have changed the outcome? This is often the most useful section.

### What we don't accept

- Vendor pitches in disguise. If your story is "we tried X, switched to Y, and Y was magical" — stop.
- Generic "AI is hard" musings. Specific events teach; generic reflections don't.
- Stories that punch down. The senior engineer who didn't take to AI tooling is not the villain of your story; the rollout that didn't account for them is.
- Identifying specifics that the anonymization rules prohibit. We will reject and ask you to revise.

## Cadence and ownership

War stories live in this repo permanently. Stories are not retracted unless an anonymization issue is discovered post-merge.

The maintainer (currently @ryanbyrd) reviews submissions for anonymization compliance and editorial quality. Editorial feedback may include suggestions to sharpen lessons or restructure for clarity. Anonymization concerns are non-negotiable.

If you spot a story whose anonymization may have slipped, open an issue tagged `anonymization-concern`. We take these seriously.

## Why this exists

The teams that succeed do the unglamorous work first. The teams that struggle compress something. The teams that fail compress the wrong thing.

These stories aren't about technology. They're about the operating layer — the conversations, the timelines, the recoveries, the political damage, the senior engineer who almost left. **Mid-size AI rollouts do not usually fail because the technology doesn't work. They fail because the operating layer was skipped.**

This collection is the operating layer in story form.

— Ryan Byrd
