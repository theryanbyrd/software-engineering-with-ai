# Postmortem — User-facing error message exposed internal vendor

> Worked example for [`postmortem-template.md`](../postmortem-template.md). Fictional but representative.

| Field | Value |
|---|---|
| Incident date | 2026-04-29 |
| Incident commander | @blee |
| Severity | SEV-2 |
| Customer impact | ~340 customers saw the message; 1 noted it on social media |
| Duration | 09:15 → 10:42 UTC (1h 27m) |

## Summary

A feature shipped on 2026-04-28 to display user-friendly error messages on payment failures included internal vendor names and infrastructure details in the user-facing strings ("Stripe webhook returned 503"). Discovered when a customer tweeted a screenshot. Hotfix replaced strings with neutral language; ~340 customers had seen the message before the fix.

## Root cause

The feature's spec said "show user-friendly error messages on payment failures." The agent built a comprehensive error-display system: caught exceptions from the payment service, mapped exception types to user-facing strings, displayed them. The user-facing strings were generated from the exception type, which included the vendor name. The agent's plan didn't include a step "review user-facing strings for sensitive information" because the issue didn't mention it.

## AI involvement
- AI's role: AI-authored
- Tool: Claude Code
- Originating issue: [INT-2945] — "Show user-friendly errors on payment failures"
- Date merged: 2026-04-28

## DeepSet failure category
- [x] **Planning failure**

**Reasoning:** The agent's plan was substantively correct for the feature scope but didn't account for the principle "never expose internal vendors or infrastructure to users." The issue didn't mention this; a senior would have asked. This is upstream of any code-level signature.

## Slop signature check
- [ ] No slop signature applied

The code was structurally fine. The bug was in *what was being communicated*, not in code patterns.

## Harness deficiency
- [x] **CLAUDE.md / AGENTS.md content** [PRIMARY] — explicit rule about user-facing strings
- [x] **A subagent** [SECONDARY] — user-facing-content reviewer
- [x] **An autonomy level downgrade** [SECONDARY] — feature work touching user-facing strings requires human approval

## Action items

### Harness changes
| Action | Owner | Deadline | Done |
|---|---|---|---|
| Add to CLAUDE.md: "User-facing strings must NEVER reference internal services, vendors, or infrastructure" with examples | @rbyrd | 2026-05-06 | [x] |
| Build subagent that reviews any PR diff touching user-facing strings against the rule | @platform-team | 2026-05-20 | [x] |
| Issue template addition: "User-facing content review" checkbox required for PRs touching `**/strings/**`, `**/i18n/**`, etc. | @rbyrd | 2026-05-06 | [x] |
| CODEOWNERS: user-facing string files require designer review | @rbyrd | 2026-05-06 | [x] |

### Process changes
| Action | Owner | Deadline | Done |
|---|---|---|---|
| Plan-approval gate for any work touching user-facing strings | @rbyrd | 2026-05-13 | [x] |

## Lessons for the team
1. "User-friendly" is not a complete spec for user-facing content. Always specify what counts as a sensitive reference.
2. Issues should explicitly mention principles like "no internal references" rather than assuming they're known.
3. Some work classes (user-facing content, data exposure, security) warrant plan-approval gates even when the spec seems clear.
