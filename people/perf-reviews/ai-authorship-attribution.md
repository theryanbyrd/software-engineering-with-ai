# Performance Review Section — AI Authorship Attribution

Add this section to your performance review template, per Ch 60 §60.3 of _Software Engineering with AI_.

---

## Section: AI Authorship Attribution

### What this measures

How the engineer thinks about, discloses, and takes responsibility for AI-authored code in their work. This is a reflection-and-judgment section, not a quantitative one.

### Manager prompt

> "Describe how this engineer thinks about and discloses AI authorship in their work. Do they accurately represent the level of AI involvement in their PRs? Do they take responsibility for AI-authored code as if it were their own? Have they had to explain AI authorship to a customer, an incident review, or a security audit?"

### Self-assessment prompt for the engineer

> "Reflect on a recent piece of work where AI tooling was substantially involved. How did you decide what to disclose, and to whom? Where did you push back on the AI's output? Where did you accept its work? In an incident or audit, would you stand by the disclosure?"

The reflection prompt is the deliverable. We're looking for substance and self-awareness, not a specific "right answer."

### What we're looking for

The engineer should be able to articulate:

- **The disclosure spectrum.** Different AI authorship levels warrant different disclosure: `ai:none`, `ai:assisted`, `ai:authored`, `ai:agent` (per Ch 31 §31.6). The engineer uses these (or your team's equivalent) accurately.
- **The responsibility default.** AI-authored code that the engineer merged is THEIR code. They reviewed it, they own it, they will not blame the agent if it breaks.
- **Asymmetric disclosure.** Some channels need more disclosure than others. PR descriptions, postmortems, security audits, customer communications — each has its own bar.
- **The "would I stand by this" test.** If the engineer would not be comfortable defending a piece of AI-authored code in an incident review, they should have either disclosed more, reviewed more carefully, or not merged.

### Common patterns

**Strong:** The engineer disclosed accurately throughout the period, took responsibility for AI-authored code in at least one moment of stress (an incident, a code review, a customer escalation), and can articulate a thoughtful position on disclosure that goes beyond "I label everything ai:assisted."

**Meeting expectations:** The engineer disclosed appropriately on most PRs. May have had a moment where disclosure was lighter than ideal but no harm came of it; they reflected and adjusted.

**Below expectations:** The engineer either over-discloses (everything is `ai:authored` to deflect blame) or under-discloses (passes off agent work as their own thinking). The engineer cannot articulate a position when asked.

### Why this matters

Per Ch 31 §31.6 and Ch 41 §41.x, AI authorship attribution is becoming a regulatory, contractual, and ethical requirement in many settings:

- Enterprise customers are asking about it in security questionnaires.
- Some regulators (financial services, healthcare) require it for code that touches their domains.
- Postmortem investigations need it to assess root cause.
- Contracts with creative-output protections need it.

Engineers who don't develop the disclosure muscle become a liability when one of these requirements lands on a project they've been working on without disclosure discipline.

### What this section will NOT do

- Will not detect a thoughtful-sounding answer covering up bad practice. Cross-reference with actual PR labels, postmortem language, and the engineer's review history.
- Will not work in a culture that punishes disclosure. If your org treats `ai:authored` as a negative signal in promotion conversations, engineers will under-disclose. Fix the culture before relying on the section.

### Calibration notes

- Junior engineers (L3): the floor is "uses the disclosure tags accurately" — they may not yet have developed a thoughtful position.
- Mid-level (L4): the floor is "can articulate the disclosure spectrum and applies it consistently."
- Senior (L5+): the floor is "has navigated at least one stress moment (incident, audit, customer escalation) where disclosure mattered, and can describe their reasoning."

### Discussion prompts for 1:1s

If the section's annual cadence is too infrequent, these prompts are useful for periodic check-ins:

- "Describe the most heavily AI-assisted piece of work you shipped this quarter. What was your disclosure?"
- "Have you reviewed someone else's AI-authored code recently and pushed back? What did you find?"
- "What would you change about how the team currently labels AI authorship?"
