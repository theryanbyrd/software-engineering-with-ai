# Postmortem — [INCIDENT TITLE]

> Copy this file. Rename to `YYYY-MM-DD-incident-slug.md`. Fill out during and after the incident. Aim for first draft within 48h, final within 5 business days.

| Field | Value |
|---|---|
| Incident date | YYYY-MM-DD |
| Incident commander | @handle |
| Severity | SEV-1 / SEV-2 / SEV-3 |
| Customer impact | (specific count if known) |
| Duration | start → resolution |
| Reviewers | @handle, @handle |
| Postmortem owner | @handle |
| Final review meeting | YYYY-MM-DD |

---

## Summary

> 2-3 sentences. What happened, what was the impact, what's the action being taken. Written for someone who wasn't on call.

---

## Standard postmortem fields

### Timeline

> Reverse chronological. Times in UTC. Include detection, key decision points, resolution. Don't include every Slack message; include the moments that mattered.

| Time (UTC) | Event |
|---|---|
| HH:MM | Incident detected |
| HH:MM | ... |
| HH:MM | Resolved |

### Impact

- **Users affected:** (count or estimate, with method)
- **Dollars affected:** (revenue impact, refunds, SLA credits)
- **Data affected:** (any user data lost, exposed, corrupted; reference any GDPR / SOC 2 / regulatory implications)
- **External notifications required:** (status page entries, customer emails, regulator notifications)

### Root cause

> The technical root cause. NOT "human error" — what was the specific mechanism by which the bug entered the codebase and reached production? Be specific enough that another engineer could verify it independently.

### Detection

- How did we find out? (alert, customer report, internal observation)
- Time from incident start to detection: ___ minutes
- Was detection within target SLO? (Y/N)
- If detection was slow: what monitoring would have caught this earlier?

### Resolution

- How did we stop the bleeding? (rollback, hotfix, feature flag, rate limit)
- Time from detection to resolution: ___ minutes
- Was resolution within target SLO? (Y/N)

---

## AI-specific fields

These sections are required if any AI tool was involved in the change that caused the incident. If not, mark "N/A — incident not related to AI-authored work" and skip.

### AI involvement

| Field | Value |
|---|---|
| Was AI involved in the change that caused this incident? | Y / N |
| If Y, what was AI's role? | (mostly AI / AI-assisted / human-authored with AI review) |
| Tool | (e.g., Claude Code, Cursor, Copilot, Codex) |
| Model and version | (e.g., `claude-sonnet-4-6`) |
| Originating issue or prompt | [link] |
| AI authorship classification (per Ch 31 §31.6) | `ai:none` / `ai:assisted` / `ai:authored` / `ai:agent` |
| PR link | [link] |
| Date the change merged | YYYY-MM-DD |
| Days from merge to incident | ___ |

### DeepSet failure category

Which of the four does this match? See [`failure-categorization-guide.md`](failure-categorization-guide.md) for definitions and examples.

- [ ] **Context failure** — the agent did not have the context it needed
- [ ] **Constraint failure** — the agent violated a stated rule
- [ ] **Verification failure** — the agent's tests passed but the behavior was wrong
- [ ] **Planning failure** — the agent's plan was incorrect or incomplete

> Pick exactly one. If multiple seem to apply, pick the most upstream one. (Example: if the agent had no context for a constraint that existed in another file, that's context failure, not constraint failure.)

**Reasoning for the categorization:**

> 2-3 sentences explaining why this category applies. The reasoning is the durable artifact; future readers will use it to calibrate their own categorization.

### Reviewer attestation

| Field | Value |
|---|---|
| Did the human reviewer attest to having read every line of the diff? | Y / N |
| Reviewer | @handle |
| Time spent in review (estimated) | ___ minutes |
| Was the diff size appropriate to the issue scope? | Y / N |

> If the reviewer attested to having read every line and still missed the bug:
> - What specifically did they miss?
> - Why was it missable? (subtle pattern, hidden in unrelated change, missing context)
> - What review discipline would have caught it?

### Was the change in scope?

| Field | Value |
|---|---|
| Was the diff bounded by the issue scope? | Y / N |
| If N, what unrelated changes were introduced? | (list) |

> Per the seventh slop signature, "diff bloat / pattern divergence" is one of the most common failure modes for AI-authored work. If the change was out of scope, this is a major signal.

### Slop signature check

Did the bug match one of the seven slop signatures? Check all that apply. See [`SLOP_SIGNATURE_REFERENCE.md`](SLOP_SIGNATURE_REFERENCE.md) for definitions and examples.

- [ ] **S1 — Tests mocking implementation rather than asserting behavior**
- [ ] **S2 — Deleted edge cases** (null, empty array, network timeout, etc.)
- [ ] **S3 — Silent error swallowing** (`try/except: pass`, `.catch(() => {})`, etc.)
- [ ] **S4 — Weakened validation** (regex loosened, range widened, required field made optional)
- [ ] **S5 — Removed security checks** (permission checks, CSRF, rate limits, sanitization)
- [ ] **S6 — Unnecessary new abstractions** (factory wrapping single function, etc.)
- [ ] **S7 — Diff bloat / pattern divergence** (small task touches many files; conventions diverge)

> If multiple signatures apply, list the primary one first. The primary one is the one whose detection would have prevented the incident; secondary ones are present but not the proximate cause.

**Was this signature detectable by `scripts/slop-detector.py`?**
- [ ] Yes, and the detector did flag it (but the warning was dismissed)
- [ ] Yes, and the detector should have flagged it (heuristic gap)
- [ ] No, the signature is too subtle for current heuristics
- [ ] N/A — no slop signature was present; the failure was in another category

> If the detector's heuristics could be tightened to catch this, link to the issue: [#issue-link]. See [`integration-with-slop-detector.md`](integration-with-slop-detector.md).

### Harness deficiency

What in the harness, if it had existed, would have prevented this? See [`harness-deficiency-checklist.md`](harness-deficiency-checklist.md) for guidance on each option.

Check all that apply. Mark with [P] the primary fix (the one most likely to prevent recurrence) and [S] for secondary.

- [ ] **CLAUDE.md / AGENTS.md content** — a documented invariant or convention that would have steered the agent
- [ ] **A hook** — a CI or pre-merge gate that would have blocked the change
- [ ] **A subagent** (security-reviewer, performance-reviewer, migration-reviewer)
- [ ] **A skill** (canonical pattern the agent could have invoked)
- [ ] **An MCP permission boundary** (the agent shouldn't have had access to do this)
- [ ] **An ADR** (architectural decision the agent should have known about)
- [ ] **An autonomy level downgrade** (this kind of work shouldn't have been done autonomously)
- [ ] **Other:** ___

**For the primary fix [P]:** describe specifically. Don't say "improve the hooks"; say "add a hook that blocks PRs deleting test cases without a corresponding `// REASON:` comment."

---

## Action items

> Each action item: assigned to a specific person, with a specific deadline, with a specific deliverable. "Be more careful" is not an action item.

### Harness changes

| Action | Owner | Deadline | Done |
|---|---|---|---|
| (specific harness change) | @handle | YYYY-MM-DD | [ ] |

### Process changes

| Action | Owner | Deadline | Done |
|---|---|---|---|
| (specific process change) | @handle | YYYY-MM-DD | [ ] |

### Org changes

| Action | Owner | Deadline | Done |
|---|---|---|---|
| (specific org change) | @handle | YYYY-MM-DD | [ ] |

### Postmortem follow-through

| Action | Owner | Deadline | Done |
|---|---|---|---|
| Update `scripts/slop-detector.py` heuristics if applicable | @handle | YYYY-MM-DD | [ ] |
| Add this incident to incident corpus index | @handle | YYYY-MM-DD | [ ] |
| Schedule 30-day check on whether action items shipped | @handle | YYYY-MM-DD | [ ] |

---

## What we got right

> The pendulum often swings too far toward criticism in postmortems. Identify what worked. Future postmortems benefit from knowing what to repeat.

- ...
- ...

## What we got wrong

> Without scapegoating individuals. Process and discipline failures, not "engineer X should have caught this."

- ...
- ...

## Lessons for the team

> The 2-4 things you'd want every team member to internalize from this incident. Different from action items — these are durable observations that change how engineers approach future work.

1. ...
2. ...
3. ...

---

## Postmortem review

> Once the postmortem is final, the postmortem review confirms it's complete and the action items are tracked.

- [ ] Reviewer 1 sign-off: @handle on YYYY-MM-DD
- [ ] Reviewer 2 sign-off: @handle on YYYY-MM-DD
- [ ] Action items entered in tracking system: YYYY-MM-DD
- [ ] Slop-detector heuristic update issue opened (if applicable): [#issue-link]
- [ ] Indexed in incident corpus: YYYY-MM-DD

---

## 30-day follow-up

> Filled out 30 days post-incident. The postmortem is not closed until this is done.

- [ ] All harness action items shipped
- [ ] All process action items shipped
- [ ] All org action items shipped (or formally accepted as deferred with reasoning)
- [ ] Has a similar incident occurred since? (Y/N — if Y, link the related postmortem and reassess action items)
- [ ] Any updates to the original categorization based on what we learned? (Y/N — if Y, document)

**30-day reviewer:** @handle on YYYY-MM-DD
