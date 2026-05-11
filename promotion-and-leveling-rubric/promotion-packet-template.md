# Promotion Packet Template

The structured artifact a manager produces to make the case for an engineer's promotion. Used as input to the calibration committee.

## How to use this template

1. Manager prepares the packet 2-3 weeks before the calibration committee meeting
2. Engineer contributes the self-assessment section
3. Manager solicits peer feedback (typically 3-5 peers)
4. Packet is finalized and sent to the committee 5-7 business days before the meeting
5. Committee reviews in advance; meeting is for discussion, not first-reading

## Packet length

Aim for 4-8 pages. Longer packets aren't read carefully; shorter packets don't make the case. The committee will read the entire packet; respect their time.

---

# Promotion Packet — [Engineer Name]

| Field | Value |
|---|---|
| **Engineer** | [Name] |
| **Current level** | [Current — e.g., L3 Engineer] |
| **Proposed level** | [Proposed — e.g., L4 Senior Engineer] |
| **Manager** | [Name] |
| **Time at current level** | [N years/months] |
| **Cycle** | [e.g., Q3 2026] |
| **Manager recommendation** | Strong promote / Promote / Promote with reservations |

---

## Section 1 — Engineer self-assessment

> Engineer writes this section. Manager doesn't edit (but reviews to ensure it's complete and accurate). Recommended length: 1-2 pages.

### What I've worked on at the current level

- [Specific projects, with brief description and outcomes]
- [Brief — bullet points are fine]

### What I'm proudest of

> 2-3 specific accomplishments. Why each was meaningful. What you learned.

### Where I've grown

> 2-3 specific dimensions where the engineer can name their own growth. Self-awareness about growth is itself a signal.

### Where I'm still growing

> Honest acknowledgment of areas the engineer is still developing. Not "I'm great at everything" — specific gaps the engineer is working on.

### Why I think I'm ready for [proposed level]

> The engineer's case in their own words. 1-2 paragraphs.

---

## Section 2 — Manager's case

> Manager writes this section. Recommended length: 2-3 pages.

### Summary

> 2-3 sentences. The manager's overall recommendation and the strongest 1-2 reasons.

### Scope

How does the engineer's scope match the proposed level?

- **Current scope:** [specific work owned end-to-end]
- **Proposed level scope:** [specific work the level requires]
- **Match:** [explanation; specific examples]

### Direction / Architecture / Evaluation depth

Per Ch 5 §5.2, depth in one with competence in others. Which is the engineer's depth, and is it credible?

- **Depth dimension:** [Direction / Architecture / Evaluation]
- **Evidence:** [specific work — a spec they wrote, a constraint system they built, a feedback loop they own]
- **Competence in others:** [specific examples]

### Five high-value engineer properties (Ch 42 §42.1)

For each, name the evidence:

1. **Code review intuition:** [evidence — specific PR reviews, slop signatures caught]
2. **Specification clarity:** [evidence — specific specs they wrote that didn't need revision]
3. **System reasoning:** [evidence — specific architectural decisions or design docs]
4. **Tooling fluency:** [evidence — harness contributions, AI tooling depth, per the level rubric for AI tooling]
5. **Calibrated skepticism:** [evidence — specific cases of useful pushback]

### Specific examples mapped to the rubric

For each criterion in [`level-rubric.md`](level-rubric.md) at the proposed level, provide 1-2 specific examples.

### Mentorship and influence

- Engineers the candidate has mentored (named, with what they grew into)
- Cross-team influence (specific examples)
- Reviews / feedback the candidate has given that improved others' work

### Areas of growth (acknowledged, not hidden)

> Be honest. Even strong promotion cases have areas where the engineer is still growing. Acknowledging them strengthens the case (the manager has clear-eyed view) rather than weakens it.

### Why now

> Why is the promotion timely? Why this cycle and not next? What evidence does the manager have that the engineer is operating at the new level NOW (not "soon" or "going to")?

---

## Section 3 — Specific examples (artifact section)

> 2-4 specific artifacts, each with brief manager commentary.

### Artifact 1: [Specific deliverable]

- **What it was:** [brief description]
- **Why it matters:** [why this is at the proposed level]
- **What it shows:** [which dimensions of the rubric]
- **Link / location:** [where to find it]

### Artifact 2: [Specific deliverable]

[Same structure]

### Artifact 3 (optional): [Specific deliverable]

[Same structure]

---

## Section 4 — Peer feedback

> Manager solicits feedback from 3-5 peers. Anonymized in the packet (peer names not exposed; just "peer 1," "peer 2," etc.).

> Each peer is asked the same questions:
> - What's [engineer's] strongest dimension at the current level?
> - Where are they still growing?
> - Have they operated at the [proposed level] consistently?
> - Any specific examples (positive or negative) you'd want a calibration committee to know?

### Peer 1 [role / level]

> Brief synthesis of feedback (2-3 sentences). Direct quotes only when especially illustrative.

### Peer 2 [role / level]

[Same structure]

### Peer 3 [role / level]

[Same structure]

### Synthesis

> Manager's synthesis: what does the peer feedback collectively suggest? Are the patterns consistent? Any divergent views worth discussing?

---

## Section 5 — Committee notes

> Filled in by the committee chair after the meeting. The packet is updated post-meeting with the decision and reasoning.

| Field | Value |
|---|---|
| **Decision** | Promoted / Deferred / Declined |
| **Date of decision** | YYYY-MM-DD |
| **Committee chair** | [Name] |
| **Effective date (if promoted)** | YYYY-MM-DD |

### Decision reasoning

> 2-3 sentences from the chair: why the committee decided as they did. Specific reference to the rubric criteria.

### If deferred or declined: gaps to close

> Specific named gaps. Path forward. Re-evaluation date.

---

## Section 6 — Engineer feedback (post-decision)

> The engineer is invited to add their reflection after the decision is communicated. Optional but recommended; the engineer's experience of the process is institutional memory.

> Filled in 2-4 weeks post-decision.

---

## What this packet will NOT do

- Will not produce a unanimous decision in every case. Some cases are close calls.
- Will not work without honest content. A packet that overstates the case will be caught by the committee.
- Will not work without time. Rushing the packet (writing it the night before the meeting) produces low-quality input.

## Common packet failure modes

- **Vague evidence.** "Engineer is great at code review" without specific PR examples. Specifics or it doesn't count.
- **Hidden gaps.** Not naming areas of growth. The committee will find them anyway; manager loses credibility.
- **Padding.** 12 pages of similar examples. The committee will skim. Quality > volume.
- **Missing peer feedback.** A packet without peers reads as "the manager's opinion alone." Peers add credibility.
- **Self-assessment that doesn't match manager's case.** Inconsistency between engineer and manager surfaces a deeper issue worth discussing pre-committee.

## Companion artifacts

- [`level-rubric.md`](level-rubric.md) — what the packet maps to
- [`ai-tooling-fluency-by-level.md`](ai-tooling-fluency-by-level.md) — the dimension that's often missed
- [`promotion-conversation-script.md`](promotion-conversation-script.md) — pre- and post-packet conversations
- [`calibration-committee-structure.md`](calibration-committee-structure.md) — what the committee does with the packet
