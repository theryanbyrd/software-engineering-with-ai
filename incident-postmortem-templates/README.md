# Incident Postmortem Templates — AI-Authored Bugs

Postmortem templates calibrated to AI-authored bugs. Direct implementation of Ch 39 of [_Software Engineering with AI: A Practical Handbook for the Claude Code Era_](https://www.linkedin.com/in/ryanbyrd) by Ryan Byrd, with the slop-signature taxonomy from Ch 22 §22.2 and the AI-authorship attribution from Ch 31 §31.6.

## What's in here

| File | Purpose |
|---|---|
| [`postmortem-template.md`](postmortem-template.md) | The full postmortem template — standard fields plus AI-specific sections |
| [`SLOP_SIGNATURE_REFERENCE.md`](SLOP_SIGNATURE_REFERENCE.md) | The seven slop signatures from Ch 22 §22.2 with examples and detection guidance |
| [`failure-categorization-guide.md`](failure-categorization-guide.md) | DeepSet's four-category taxonomy from Ch 39 §39.2: context / constraint / verification / planning failure |
| [`harness-deficiency-checklist.md`](harness-deficiency-checklist.md) | "What in the harness, if it had existed, would have prevented this?" — the structured action-items work |
| [`example-postmortems/`](example-postmortems/) | Three worked examples covering the most common failure modes |
| [`integration-with-slop-detector.md`](integration-with-slop-detector.md) | How the postmortem feeds back into `scripts/slop-detector.py` heuristics |

## The book's framing

> When the bug came from an AI-authored or AI-assisted change, the postmortem needs structure that the standard incident template does not capture.
>
> — Ch 39 opening

Standard postmortem templates ask "what happened, what's the root cause, what's the fix." That's necessary but insufficient for AI-related bugs. The new questions:

- Which of the seven slop signatures was present that should have been caught?
- Which of the four DeepSet failure categories does this match?
- What in the harness, if it had existed, would have prevented this?
- Did the human reviewer attest to having read every line — and if yes, what was missed?
- Was the change in scope?

## Editorial stance

> Always pair an incident with a specific harness or process change. "Be more careful" is not an action item.
>
> — Ch 39 §39.3

The point of these templates is not to assign blame to AI tools or to engineers. The point is to extract durable harness improvements from each incident. An incident that produces a generic "everyone be more careful" action item is an incident that's going to recur. An incident that produces a specific hook, skill, CLAUDE.md addition, or autonomy-level change is an incident the team learned from.

## Who this is for

- Incident commanders running a postmortem
- Engineering managers reviewing incident response quality
- Platform team members who own harness improvements
- VP of Engineering tracking the failure-mode patterns across incidents

## Read first

- Ch 22 — code review in the AI era; the seven slop signatures
- Ch 31 §31.6 — the attribution toolkit (PR tagging, six quality decay signals)
- Ch 39 — the chapter this implements
- `scripts/slop-detector.py` — the automated detection paired with the postmortem categorization
- `prompt-injection-test-suite/` — adjacent failure-mode discipline

## What these templates WILL do

- Produce postmortems that name the harness gap explicitly
- Generate action items that ship harness improvements within 1-2 weeks of the incident
- Build a categorized incident corpus over time that surfaces patterns
- Calibrate the team's review practices against actual failure modes
- Feed back into the slop-detector heuristics so the next instance is caught automatically

## What these templates will NOT do

- Will not work in a culture that scapegoats AI tools or individual engineers. Postmortems require psychological safety; the templates assume it.
- Will not eliminate incidents. They make incidents productive.
- Will not work if the action items don't ship. A postmortem with great categorization and unstaffed action items produces no learning.
- Will not apply to incidents that have nothing to do with AI tooling. Standard postmortem template applies for those; don't shoehorn.

## When to use which template

| Situation | Template |
|---|---|
| AI-authored or AI-assisted change introduced a bug | [`postmortem-template.md`](postmortem-template.md) |
| Outage caused by infrastructure or dependency, no AI authorship involved | Your standard postmortem template |
| Mixed: AI was involved but the root cause was upstream | Use this template's AI sections; add infrastructure root-cause sections from your standard template |
| Near-miss (caught in review, never shipped) | Lightweight version: just the slop-signature section + harness-deficiency section |

## How the templates fit together

The postmortem template references the other files. The flow during a postmortem:

1. Open the postmortem with [`postmortem-template.md`](postmortem-template.md)
2. When filling out the slop-signature section, reference [`SLOP_SIGNATURE_REFERENCE.md`](SLOP_SIGNATURE_REFERENCE.md)
3. When filling out the failure-category section, reference [`failure-categorization-guide.md`](failure-categorization-guide.md)
4. When filling out the harness-deficiency section, reference [`harness-deficiency-checklist.md`](harness-deficiency-checklist.md)
5. When deciding on action items, the categorization tells you what kind of harness change is most likely to help

## Companion artifacts

- `scripts/slop-detector.py` — automated detection of the seven signatures
- `skills/code-review/SKILL.md` — the canonical review discipline
- `prompt-injection-test-suite/` — adjacent failure-mode discipline
- `benchmarks/` — quarterly regression testing that paths could trigger the postmortem template
- Ch 22, 31 §31.6, 39 — the source chapters
