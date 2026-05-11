# Performance Review Section — Review Discipline

Add this section to your performance review template, per Ch 60 §60.3 of _Software Engineering with AI_.

---

## Section: Review Discipline

### What this measures

Whether the engineer reviews code thoroughly, finds the seven slop signatures (Ch 22), and applies appropriate severity calibration. This is the muscle that protects the codebase from AI-authored slop AND from human errors.

This section ALSO applies when the engineer is not formally reviewing — comments on architecture proposals, push-backs in design docs, debate in postmortems. Review discipline is a posture, not just an activity.

### Manager prompt

> "How is this engineer's code review work? Do they find issues other reviewers miss? Are their reviews trusted by senior engineers? Do they push back appropriately or do they rubber-stamp? Do they review AI-authored code with the same discipline as human-authored code?"

### Self-assessment prompt for the engineer

> "Describe a recent review where you caught something important. Describe a review where you let something slide that you wish you hadn't. What's your default review process? Do you review AI-authored PRs differently than human-authored ones?"

### Grading rubric

| Dimension | What we're looking for |
|---|---|
| **Slop signature detection** | Catches the seven signatures (Ch 22): imaginary APIs, confidently wrong logic, repetitive boilerplate, vestigial code, tests-without-testing, comment drift, scope creep. |
| **Severity calibration** | Distinguishes blocking from major from minor from nit. Blocking findings are genuinely blocking. |
| **Should-this-exist judgment** | Asks structural questions when appropriate: should this PR be three smaller PRs? Should this approach exist at all? |
| **Tone and pushback** | Pushes back with specifics. Frames suggestions constructively. Doesn't hide concerns to be liked. |
| **Adoption** | Other engineers send their hard PRs to this person for review. The reviews are trusted. |
| **AI-authored discipline** | Reviews AI-authored PRs at least as carefully as human-authored ones; sometimes more. |

### Common patterns

**Strong (above expectations):**
- Other engineers explicitly request reviews from this person on hard PRs
- Catches issues that other reviewers miss; the catches are repeatable
- Has a known review style that the team has internalized
- Review judgment trusted enough that this engineer's "approve" carries weight

**Meeting expectations:**
- Reviews are competent and substantive
- Catches the major issues most of the time
- Severity calibration is mostly correct
- Engages with AI-authored PRs with appropriate discipline

**Below expectations:**
- Reviews are perfunctory or rubber-stamped
- Misses obvious slop signatures repeatedly
- Either inflates or deflates severity consistently
- Treats AI-authored PRs as "the AI did it; it's probably fine"

### Why this matters

Per Ch 22 and Ch 42 §42.1, code review judgment is one of the highest-value engineering skills in the AI-native era. Per Ch 60 §60.1, it's now an explicit leveling criterion at L4-L5 and above.

Engineers who can run a productive AI session can do so because they have strong code review intuition — they recognize what's wrong in seconds, the same way they'd recognize it in a junior's PR. Engineers without that muscle either reject all AI output (slow) or accept all AI output (slop).

### What this section will NOT do

- Will not capture every review the engineer did. If your team uses a code-review tool that doesn't surface metrics on review depth, this section is a manager judgment, not a data-driven score.
- Will not work if the team doesn't review thoroughly in general. If the team's review culture is "approve-after-glance," no individual engineer's discipline will fully compensate.

### Calibration: data sources

The manager has multiple sources to triangulate:

1. **Sample 3-5 of the engineer's recent reviews.** Read them. Do they catch things? Are the comments substantive?
2. **Ask 1-2 senior engineers** about the engineer's review work. "Whose reviews do you trust most? Whose do you wish you got more often? Whose do you double-check?"
3. **Sample 2-3 PRs the engineer authored.** Were the reviews on THOSE strong? Did the engineer respond well to feedback or push back appropriately?
4. **Check the engineer's response to AI-authored code** specifically. Look at PRs where the engineer reviewed an `ai:assisted` or `ai:authored` PR. Was the review thorough?

### Tied to leveling

Per Ch 60 §60.1, code review judgment is now a leveling criterion. This section's findings should feed directly into:

- L3 → L4 promotion: review work is trustworthy
- L4 → L5 promotion: other senior engineers send their hard PRs to this person
- L5 → L6/L7: the engineer's review style has shaped the team's overall review culture

### Discussion prompts for 1:1s

- "What's a review you did recently that you're proud of? What did you catch?"
- "Have you let something slide in a review recently that you wish you hadn't? What was it?"
- "Whose reviews do you learn the most from on this team?"
- "How do you decide when to escalate a finding to 'blocking' vs leaving it as a comment?"
