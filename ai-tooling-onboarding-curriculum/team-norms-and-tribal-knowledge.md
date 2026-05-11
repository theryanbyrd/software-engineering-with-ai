# Team Norms and Tribal Knowledge

The unwritten content new engineers need. Per Ch 44 §44.1's spirit, week 1 covers the documented part — CLAUDE.md, AGENTS.md, the autonomy ladder, the do-not-automate catalog. This file is the operational guide to surfacing the undocumented part.

The premise: every team has tribal knowledge that isn't written down. Some of it should stay tacit (it changes too fast to document). Some of it should be written down (and the new engineer's confusion is the signal that it should be). This file gives the buddy a checklist of topics to surface, and the engineer a sense of what to ask about.

## Why this matters

A new engineer can read every documented artifact and still struggle for weeks because they don't know:
- That this team uses Slack threads heavily but DMs are rare
- That the Tuesday standup is short and Wednesday's is long
- That this senior engineer reviews everything and that one rarely does
- That this build has been flaky for months and the team has a workaround
- That this test suite has a timing dependency and rerunning fixes it 80% of the time
- That this domain has a subtle invariant that nobody documented because it was obvious to those who built it

The buddy's job in onboarding is partially to surface this tacit content explicitly.

## What new engineers need to know

### Communication norms

Things to surface in week 1:

- **Slack vs email vs sync:** when does each medium apply? In most modern teams, Slack is default; email is for external + record-keeping; sync is for high-bandwidth.
- **Response time expectations:** how fast does the team expect responses? Is "respond within the day" the norm, or "within an hour"?
- **DM etiquette:** do team members DM freely, or is it considered intrusive? When is a DM appropriate vs. a thread?
- **Thread discipline:** does the team use Slack threads for everything, or only for specific topics?
- **Channel etiquette:** what goes in #engineering vs #team-foo vs #random?
- **Handle the on-call channel separately:** there's usually a specific channel for on-call alerts; treating it like a chat channel is a faux pas.
- **Out-of-hours norms:** does the team expect responses at night/weekends? What about during PTO?

### Review style

- **Detailed vs. terse reviewers:** some engineers leave 30 comments per PR; others leave 2. Knowing who's which calibrates expectations.
- **What reviewers reliably catch:** specific patterns that this team's reviewers have learned to watch for. The new engineer should know.
- **When to use synchronous review:** for which PRs is async review insufficient? Usually: complex PRs, PRs that touch many surfaces, PRs where the diff is large.
- **Review SLOs:** how fast does the team aim to turn around reviews? "Within 24 hours" is common; "within 2 hours" is for high-velocity teams.
- **Approval norms:** does "LGTM" mean "I read every line carefully" or "I read the summary"? Teams differ.
- **The "hot reviewer" problem:** per Ch 44 §44.5, some teams over-rely on one or two reviewers. The new engineer should know who's overloaded so they don't default to them.

### Release cadence

- **Daily, weekly, on-demand?** Daily releases require different review discipline than weekly.
- **Release process:** who can deploy? What's the approval flow? Where are the runbooks?
- **Rollback discipline:** how does rollback work? Has the team rolled back recently?
- **Deployment windows:** are there freezes around holidays, big launches, end-of-quarter?
- **Who notifies whom:** when something is deployed, who needs to know?

### Incident response

- **How on-call works:** what's the rotation? What's the handoff process? What tools does on-call use?
- **Escalation:** when do you escalate? To whom?
- **Postmortem culture:** does the team do postmortems for every incident or only severe ones? What's the format? (Per `incident-postmortem-templates/`.)
- **Recent incidents:** what was the most recent incident? What did the team learn? This shows the team's actual incident discipline, not the documented one.

### Planning rhythm

- **Sprint cadence:** weekly, biweekly, quarterly, no-sprint? If sprints, how do they work?
- **OKR structure:** does the team set OKRs? Per quarter? How do they tie to roadmap?
- **Roadmap visibility:** is there a published roadmap? Where? How often is it updated?
- **Promotion calibration:** when does the team discuss promotions? Calibration meetings?
- **1:1 cadence:** how often do 1:1s happen, and what's the typical content?

### Technical gotchas

The undocumented technical content. Examples:

- "This service has a weird invariant: X must be done before Y. It's enforced by [obscure mechanism]."
- "This build is flaky. If it fails, retry once. If it fails twice, see #build-flakes."
- "This test has a timing dependency. It usually passes on rerun."
- "This service's logs go through [intermediary] which adds latency. Account for this when debugging."
- "Don't ever do X in this codebase. We tried and it broke Y. The fix is Z but we never wrote it down."

### Who-to-ask map

For new engineers, knowing who's the expert on what is half the battle. By end of week 2, the buddy should have introduced the engineer to:

- The team's senior engineers and what they specialize in
- Adjacent teams the new engineer will work with (and who their senior contacts are)
- The platform team contacts (per `platform-team-charter/`)
- The security team contact (per Day 5's prompt-injection discussion)
- The product manager
- The engineering manager (the new engineer's manager, of course; but also adjacent EMs they'll interact with)

The map doesn't need to be a literal document. It needs to be in the engineer's head: "X knows about auth, Y knows about billing, Z knows about deployment."

## How to surface tribal knowledge

### Pattern 1 — Spot when the engineer is confused

The new engineer's confusion is the signal. Things that confused them are things that probably aren't well-documented OR things that the team has learned but not written down.

The buddy's job: when the engineer expresses confusion, ask "is this confusion something we should fix in the docs, or is this just something I should explain?"

- If "fix the docs" — capture the gap; queue for documentation work
- If "I should explain" — explain, but consider whether the explanation should also go in the docs

### Pattern 2 — Run the "if you'd known this in week 1" exercise

At the end of week 4, ask the engineer:

> "What's something you wish you'd known on day 1 that you've learned since?"

The list is gold. Each item is either:
- A documentation gap (add to CLAUDE.md, AGENTS.md, or this file)
- A tribal knowledge item that should stay tacit (don't document, but the buddy now knows to surface it for the next new hire)
- A pattern in the team's onboarding that should change (raise to the manager)

### Pattern 3 — The "what would surprise an outsider" check

Once the engineer is past day 30, they're starting to internalize the team's norms. Before they fully naturalize, capture: "what surprised you about how this team works?"

This is the last chance to capture outside-perspective signal. After 60-90 days, the engineer's perspective becomes inside; the surprises blend in.

### Pattern 4 — Document patterns that cause repeated confusion

If the buddy hears the same confusion from 3+ new engineers, that's not tribal knowledge — that's a documentation gap. Address it in the team's CLAUDE.md, AGENTS.md, or onboarding docs.

## Anti-patterns

### "Sink or swim" onboarding

Some teams treat tribal knowledge transmission as the new engineer's responsibility. "They'll figure it out."

Result: 3 months of unnecessary friction; the new engineer's productivity is delayed; sometimes the engineer leaves.

Mitigation: explicit buddy responsibility for tribal-knowledge surfacing. It's not optional.

### The buddy is the only source

If only one person knows the tribal knowledge, the team has a bus factor of 1. The new engineer's onboarding succeeds, but the team is fragile.

Mitigation: tribal knowledge that recurs across hires gets documented. The buddy's role is to surface it AND to flag for documentation.

### "It's not worth documenting"

The team rationalizes that specific tribal knowledge isn't worth documenting because it changes too fast or affects too few people.

Sometimes true. Sometimes a way of avoiding documentation work.

Mitigation: when in doubt, document briefly. A single sentence in the right place is worth more than a perfectly-crafted doc that doesn't exist.

### Surfacing in week 4 instead of week 1

The buddy waits until the engineer naturally encounters something rather than surfacing proactively. The engineer hits the same confusion every previous new hire hit, then gets explained.

Mitigation: this file's checklist is the proactive surface. Don't wait for the engineer to stumble.

### "We don't have time"

Onboarding is committed time per [`buddy-and-manager-roles.md`](buddy-and-manager-roles.md). If the buddy doesn't have time to surface tribal knowledge, the buddy isn't actually buddying.

## What this file will NOT do

- Will not capture all the tribal knowledge for any specific team. The team's specific tribal knowledge is in the buddy's head; this file is the prompt to surface it.
- Will not make the documentation itself. If gaps are found, addressing them is real work — not just the surfacing.
- Will not eliminate friction. Some friction is inherent in joining a team; the goal is reducing avoidable friction.

## Companion artifacts

- [`week-1-curriculum.md`](week-1-curriculum.md) — the structured part of onboarding
- [`pair-driving-milestones.md`](pair-driving-milestones.md) — pair-driving structure
- [`buddy-and-manager-roles.md`](buddy-and-manager-roles.md) — who surfaces tribal knowledge
- [`days-8-to-30.md`](days-8-to-30.md) — when tribal knowledge becomes internalized
- Ch 44 §44.1 — source
