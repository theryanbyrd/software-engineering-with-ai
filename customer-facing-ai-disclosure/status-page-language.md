# Status Page Language for AI-Authored Code Incidents

Customer-facing language for status page updates when an incident involves code authored or significantly assisted by AI tooling. Direct implementation of Ch 31 §31.6 (the attribution toolkit) and Ch 41 (governance and disclosure).

## The principle

The customer cares about three things on a status page during an incident:

1. **What's broken right now.**
2. **When it will be fixed.**
3. **Whether it's going to happen again.**

The customer does *not* primarily care whether the code was AI-authored, human-authored, or pair-authored. The AI-authorship detail enters the conversation in two specific places:

- **The post-incident review or postmortem** (where the root cause is named honestly)
- **The disclosure to specific customers who explicitly ask** (when their security or compliance team raises it)

It rarely belongs on the live status page itself, except in the specific cases below.

## When AI authorship goes on the status page

### ✅ It belongs on the status page when:

1. **The incident's root cause is specifically a known AI failure mode** (e.g., agent-induced hallucinated API call hitting a third-party service, agent-introduced N+1 query that took the database down). The honest disclosure helps customers calibrate their own AI usage.
2. **A regulatory disclosure requires it.** Some industries (finance, healthcare) require disclosure of automated tooling involvement in incidents.
3. **Public discourse is already ahead of you.** If a customer or third party has already speculated publicly that AI tooling was involved, denial creates more damage than honest disclosure.
4. **The pattern affects multiple customers in identifiable ways** (e.g., agent-authored code generated incorrect responses for a specific customer-data shape). Disclosure helps customers verify they weren't affected.

### ❌ It does NOT belong on the status page when:

1. The incident's root cause is a normal bug that happens to be in code an agent wrote. Code review, tests, and verify discipline failed; the AI authorship is upstream of those failures, not the cause itself.
2. You're doing it to manage public perception of AI usage. Customers can tell.
3. You haven't yet completed a real root-cause analysis. Speculating that "AI tooling may have been involved" before knowing is worse than waiting.
4. The disclosure would identify a specific customer or PII.

## The status page templates

The templates below are calibrated to the typical phases of an incident. Use them in sequence; don't jump to "resolved" before the actual resolution.

### Initial detection (within 5-15 minutes of detection)

> **[Incident name] — Investigating**
>
> _[Time stamp]_
>
> We are currently investigating reports of [observable customer impact — slow responses, errors, missing functionality]. We've activated our incident response process and will provide updates as we learn more.
>
> Initial impact estimate: [scope — all customers / customers using feature X / customers in region Y].

**No mention of cause yet, AI or otherwise.** Cause is unknown.

### Identified cause (when root cause is known but fix is pending)

#### Standard version (most incidents):

> **[Incident name] — Identified**
>
> _[Time stamp]_
>
> We've identified the root cause: [brief, honest description in customer-affecting terms]. Our engineering team is implementing the fix.
>
> Expected resolution: [time estimate]. We'll update this page when the fix is deployed.

#### AI-authored cause version (when the disclosure criteria above apply):

> **[Incident name] — Identified**
>
> _[Time stamp]_
>
> We've identified the root cause: [brief description]. The affected code was authored with AI assistance and contained [specific failure mode — e.g., a malformed query pattern, an incorrect API response shape] that our review and CI pipeline did not catch before deployment.
>
> Our engineering team is implementing the fix. We'll address the gap in our review process in our follow-up post-incident review and share findings.
>
> Expected resolution: [time estimate].

### Resolution (after the fix is deployed and verified)

> **[Incident name] — Resolved**
>
> _[Time stamp]_
>
> The fix has been deployed and we've verified [normal behavior is restored / metric X is back to baseline].
>
> Affected customers: [scope and approximate count if known]. We are reaching out individually to customers with material impact.
>
> A post-incident review will be published within [N business days].

### Post-incident review reference (when the public PIR is published)

> **[Incident name] — Post-Incident Review Published**
>
> Our review of the [date] incident is now available: [link]. Key findings:
>
> - Root cause: [one sentence]
> - Customer impact: [one sentence]
> - Mitigations now in place: [one sentence]
> - Process changes: [one sentence]
>
> Questions or concerns? Contact [email].

## Calibration: how much AI-authorship detail in the PIR itself

The post-incident review (PIR) is more detailed than the status page. The AI-authorship disclosure question is more nuanced here.

### What to include in the PIR when AI tooling was involved

- **The fact that the affected code was AI-assisted.** Don't hide it; the engineers who reviewed the PIR know. Customers who ask specifically deserve the truth.
- **What the engineer's review caught and didn't catch.** Be specific. Code review is not a sole defense; CI, harness, and the verify command are part of the system.
- **The specific failure mode.** "The agent generated a query that worked at the test data scale but caused a full table scan at production scale" is more useful than "the AI made a mistake."
- **The harness or process gap.** "The verify command did not include a query plan check; we are adding one" is the part customers respect.
- **What you're changing about the AI tooling discipline.** "We are adding a constraint surface that catches this pattern before merge" or "We have added a hook that requires explicit reviewer sign-off on queries against table X."

### What NOT to include in the PIR

- **Specific tool brand-name blame.** "Claude Code generated the bug" is not the right framing; "the agent we use generated a query pattern that we did not catch in review" is. The brand-name framing invites speculation about whether you should switch tools, which is rarely the actual lesson.
- **Productivity metrics or token costs.** Out of scope for a PIR.
- **Speculation about what other vendors might have done differently.** Invites comparative claims you can't substantiate.
- **Personal blame on the engineer who reviewed the PR.** Code review is a system; the system failed, not just the reviewer.

### Sample PIR section on AI-authorship

> ### Code authorship and review
>
> The change that introduced the regression was authored with AI tooling assistance under our standard development practices. The pull request was reviewed by two engineers, one of whom was the change's author and one of whom was a senior engineer in the affected service area. Both reviewers approved.
>
> The specific failure mode — a query plan that performed acceptably on test data and pathologically on production-scale data — is one that our review process did not have an explicit check for. The verify command in our CI pipeline does not currently include a query-plan analysis step.
>
> #### What we're changing
>
> 1. We are adding query-plan analysis to our verify command for changes touching the affected service. Targeted change; not all queries need this. Implementation by [date].
> 2. We are updating our code review checklist to include explicit query-plan review for changes that touch tables above [size threshold].
> 3. We are improving the CI test fixtures for this service to include data at production-representative scale.
>
> The use of AI tooling did not cause this incident. The lack of an automated check for the specific failure mode caused this incident. We are correcting the gap.

## What this template will NOT do

- Will not work in a culture where the company position is "we don't disclose AI usage." If that's your stance, this template is wrong; you'll need a different approach (and we recommend reconsidering the stance).
- Will not work if your incident response process is itself broken. Status page language is downstream of having a real incident response. Fix the incident response first.
- Will not work for incidents involving a security breach. Different domain; legal counsel drives the disclosure language.

## When customers ask about a specific past incident

If a customer asks about an incident that's in the past — typically because they're reading your status page or PIR archive as part of their procurement review — direct them to the public PIR. Do not embellish or add detail beyond the public document. The public document is the canonical answer.

If they ask follow-up questions beyond what's in the public doc:

> "The public post-incident review at [link] has the canonical detail. If you have specific questions beyond what's there, your account team can connect you with the relevant engineering leader for a deeper conversation under NDA."

## Companion artifacts

- [`security-questionnaire-answers.md`](security-questionnaire-answers.md) — for the questionnaire-side of disclosure
- [`disclosure-decision-framework.md`](disclosure-decision-framework.md) — when to disclose what
- [`customer-conversation-scripts.md`](customer-conversation-scripts.md) — for the live customer conversation
- `incident-postmortem-templates/` — the internal PIR structure that feeds the public version
- Ch 31 §31.6 — the attribution toolkit
- Ch 41 — governance and disclosure
