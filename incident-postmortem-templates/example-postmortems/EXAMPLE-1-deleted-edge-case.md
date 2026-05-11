# Postmortem — Stripe webhook handler 503 retry exhaustion

> Worked example for [`postmortem-template.md`](../postmortem-template.md). Fictional but representative incident.

| Field | Value |
|---|---|
| Incident date | 2026-04-12 |
| Incident commander | @rbyrd |
| Severity | SEV-2 |
| Customer impact | 6 customers; $14,200 in delayed transactions |
| Duration | 13:42 → 15:07 UTC (1h 25m) |
| Reviewers | @ssmith, @kchen |
| Postmortem owner | @rbyrd |
| Final review meeting | 2026-04-19 |

## Summary

A Stripe webhook handler refactored on 2026-04-08 dropped a retry-with-jitter branch that the original code had. When Stripe returned 503 during a Saturday traffic spike, the new handler retried infinitely without backoff, exhausting the database connection pool. Customer-facing impact: 6 enterprise customers' payment confirmations delayed 60-90 minutes.

## Standard postmortem fields

### Timeline

| Time (UTC) | Event |
|---|---|
| 13:42 | DB connection pool alert fires (95% utilization) |
| 13:44 | On-call (@rbyrd) acknowledges; investigates |
| 13:51 | Identified the new webhook handler retrying continuously |
| 13:54 | Rate-limited the handler at the load balancer |
| 14:01 | Connection pool drains to 60% |
| 14:23 | Root cause hypothesis: missing exponential backoff |
| 14:38 | Hotfix prepared (re-add the backoff) |
| 14:51 | Hotfix deployed to canary |
| 14:55 | Canary metrics green |
| 15:02 | Hotfix to production |
| 15:07 | Resolved |

### Impact
- Users affected: 6 enterprise customers
- Dollars affected: $14,200 in delayed transactions; $0 lost (all eventually settled)
- Data affected: None
- External notifications: Status page entry posted at 14:01; cleared 15:15

### Root cause

The webhook handler refactor on 2026-04-08 (PR #4127) extracted retry logic into a generic helper. The new helper handled the basic retry case but did not include the exponential-backoff-with-jitter pattern that the original handler had. Under 503 returns, the new handler retried with a fixed 100ms delay, generating ~600 retries/sec across the connection pool.

### Detection

How: DB connection pool utilization alert
Time from incident start to detection: 2 minutes (well within SLO of 5 min)
Was detection within SLO: Yes

### Resolution

How: Rate-limited at load balancer (immediate); hotfix re-added exponential backoff (durable)
Time from detection to resolution: 1h 23m
Was resolution within SLO: No (target is 60 min for SEV-2)

## AI-specific fields

### AI involvement

| Field | Value |
|---|---|
| Was AI involved? | Yes |
| AI's role? | AI-authored, human-reviewed |
| Tool | Claude Code |
| Model and version | `claude-sonnet-4-6` |
| Originating issue | [INT-2891](https://...) — "Refactor Stripe webhook handler retry logic" |
| AI authorship classification | `ai:authored` |
| PR link | [#4127](https://...) |
| Date the change merged | 2026-04-08 |
| Days from merge to incident | 4 |

### DeepSet failure category

- [x] **Verification failure** — the agent's tests passed but the behavior was wrong

**Reasoning:** The new tests verified that retry logic existed and that retries happened on 503. The tests did NOT verify that retries had exponential backoff or jitter. The original code's behavior under sustained 503 was not characterized in tests; the agent's refactor preserved the tested behavior but lost the un-tested behavior.

### Reviewer attestation

| Field | Value |
|---|---|
| Reviewer attest to reading every line? | Yes |
| Reviewer | @kchen |
| Time spent in review | ~25 min |
| Was diff size appropriate? | Yes (210 lines, scope appropriate) |

> The reviewer read the diff carefully and the new code looked clean. The bug was in what was REMOVED from the old code — the exponential-backoff line — but the reviewer didn't compare the old retry path to the new one structurally. This is the canonical S2 reviewer trap.

### Was the change in scope?
- Bounded by issue scope: Yes
- Unrelated changes: None
- Diff bloat: No

### Slop signature check

- [x] **S2 — Deleted edge cases** [PRIMARY]
- [x] **S1 — Tests mocking implementation rather than asserting behavior** [SECONDARY]

The original code had:
```go
// Original (deleted)
backoff := initialBackoff
for retry := 0; retry < maxRetries; retry++ {
    err := callStripe(req)
    if err == nil {
        return nil
    }
    if !isRetryable(err) {
        return err
    }
    time.Sleep(backoff + jitter())
    backoff *= 2
    if backoff > maxBackoff {
        backoff = maxBackoff
    }
}
```

The new code:
```go
// New (S2 — exponential backoff branch deleted)
for retry := 0; retry < maxRetries; retry++ {
    err := callStripe(req)
    if err == nil {
        return nil
    }
    if !isRetryable(err) {
        return err
    }
    time.Sleep(100 * time.Millisecond)
}
```

The S1 secondary: tests mocked `callStripe` and verified retry count was 5; they did not exercise the timing of retries.

**Was this signature detectable by slop-detector?**
- [x] Yes, and the detector should have flagged it (heuristic gap)

The detector's current S2 heuristic looks for whole-branch deletions. This case was a partial-branch simplification (the retry loop survived; the backoff calculation inside the loop was deleted). Issue [#detector-47] opened to add a "loop-body simplification check" that flags significant complexity reduction inside a preserved control structure.

### Harness deficiency

- [x] **An ADR** [SECONDARY] — ADR-019 needed: "External API retry policy standards"
- [x] **A skill** [PRIMARY] — `skills/external-api-retry/SKILL.md` codifying the team's retry pattern
- [x] **CLAUDE.md / AGENTS.md content** [SECONDARY] — note added under "External calls" section

The skill is the primary fix because it gives the agent a canonical pattern to invoke; the ADR documents why; the CLAUDE.md addition makes the skill discoverable.

## Action items

### Harness changes

| Action | Owner | Deadline | Done |
|---|---|---|---|
| Write `skills/external-api-retry/SKILL.md` with exponential backoff + jitter pattern | @rbyrd | 2026-04-22 | [x] |
| Add ADR-019 documenting retry policy standards | @rbyrd | 2026-04-26 | [x] |
| Update CLAUDE.md with reference to the skill | @rbyrd | 2026-04-22 | [x] |
| Issue [#detector-47] — add loop-body simplification check to slop-detector | @platform-team | 2026-05-03 | [x] |

### Process changes

| Action | Owner | Deadline | Done |
|---|---|---|---|
| Review checklist addition: "When refactoring retry/backoff/timeout logic, compare structurally to the original" | @kchen | 2026-04-19 | [x] |

### Org changes

| Action | Owner | Deadline | Done |
|---|---|---|---|
| None this incident | — | — | — |

### Postmortem follow-through

| Action | Owner | Deadline | Done |
|---|---|---|---|
| Update slop-detector heuristics | @platform-team | 2026-05-03 | [x] |
| Add to incident corpus index | @rbyrd | 2026-04-19 | [x] |
| Schedule 30-day check | @rbyrd | 2026-05-12 | [x] |

## What we got right

- Detection within 2 minutes; rate-limit mitigation within 12 minutes
- Hotfix was clean and minimal; canary process worked as designed
- Status page communication was timely and accurate

## What we got wrong

- The PR review didn't catch the S2 signature despite reading every line
- The skill for external API retries didn't exist; engineering hadn't codified the team's standard
- The slop-detector heuristic for S2 didn't catch loop-body simplification (heuristic gap)
- Resolution took 1h 23m vs. SLO of 60 min; need to investigate whether SLO is realistic for this class

## Lessons for the team

1. When refactoring complex control flow (retry, backoff, timeout, circuit breaker), compare structurally to the original — line-by-line review misses behavior in deleted lines
2. Tests that pass on a refactor are necessary but not sufficient; if the original behavior wasn't tested, the refactor has a gap
3. When extracting code into a helper, verify the helper preserves all the edge cases of the original

## Postmortem review

- [x] Reviewer 1 sign-off: @ssmith on 2026-04-19
- [x] Reviewer 2 sign-off: @kchen on 2026-04-19
- [x] Action items entered in tracking system: 2026-04-19
- [x] Slop-detector heuristic update issue opened: [#detector-47]
- [x] Indexed in incident corpus: 2026-04-19

## 30-day follow-up

- [x] Harness action items shipped (skill, ADR, CLAUDE.md update — all completed)
- [x] Process action items shipped (review checklist updated)
- [x] Org action items: N/A
- [x] Has a similar incident occurred since? No
- [x] Categorization update? Confirmed: verification failure was the right primary; the secondary signature S1 was correctly identified

**30-day reviewer:** @rbyrd on 2026-05-12. Heuristic shipped; tested against past 90 days of PRs (3 true positives, 1 false positive — acceptable).
