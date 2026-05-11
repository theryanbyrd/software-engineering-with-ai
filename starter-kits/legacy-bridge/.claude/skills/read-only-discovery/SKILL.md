---
name: read-only-discovery
description: Use during the 2-week read-only period on a legacy module. Answers questions about the code without making changes. Captures the Q&A as module-level READMEs and notes about invariants.
allowed_tools: Read, Grep, Bash
---

# Read-Only Discovery

You are exploring a legacy module that nobody currently understands well. You will be asked questions; you may NOT make changes. Your output is the answer + a record of what you learned.

This is the most valuable two weeks of the brownfield migration. Skip it at your peril.

## Process

For each question:

1. **Read the relevant code thoroughly.** Use Grep to find call sites, imports, related files.
2. **Map the surface area.** What functions are public? What's called from outside the module? What's the entry point?
3. **Identify invariants.** What does the code assume about its inputs? Its environment? Its callers?
4. **Look for "weirdness."** Comments referencing departed engineers, unusual control flow, magic numbers, dead-looking code that's actually called.
5. **Answer the question.** Be specific. Cite file:line references.
6. **Capture the Q&A.** Append to the module-level README under a "Discovery notes" section.

## Output format

After answering, write to `<module>/README.md`:

```markdown
## Discovery notes

### What does `compute_user_score` do?

(Q&A captured 2026-05-04)

`compute_user_score(user_id, date)` returns the user's "tier" score for a
given date. It reads from three places:
- `legacy_billing.invoices` (filters by user_id and date range)
- `metrics.user_events` (counts certain event types in a 90-day window)
- `metrics.user_sessions` (averages session duration in a 30-day window)

The output is a dict: `{"score": int, "tier": "A"|"B"|"C", "raw": [int, int, int]}`.

**Invariants observed:**
- The function returns `{"score": 0, "tier": "C", "raw": [0,0,0]}` for any user with no events. This is intentional, not a bug.
- The `raw` list always has exactly 3 elements (counts from the three sources).
- The function uses 90-day and 30-day windows — these are hardcoded.

**Weirdness observed:**
- The tier boundary (`score >= 75 → "A"`, `>= 50 → "B"`, else `"C"`) is hardcoded. There is no config.
- A comment dated 2019 says "// matches legacy billing tier from before reorg" — meaning the boundaries were chosen to match an even older system that may no longer exist.

**Files involved:**
- `legacy/scoring/compute.py:23-89` — main function
- `legacy/scoring/queries.py:11-45` — the three SQL queries
- `tests/legacy/test_scoring.py` — sparse tests, mostly for the score=0 case

**Recommended follow-up:**
- Confirm with [name] whether the "legacy billing tier" referenced in the 2019 comment still has a referent.
- Add the hardcoded tier boundaries to the architecture-as-known.md doc.
```

## What this skill DOES

- Reads code, runs grep, traces references
- Documents what it learned
- Captures invariants and weirdness in writing
- Identifies follow-up questions for human experts

## What this skill does NOT do

- **Make any changes.** This is read-only. If you find yourself wanting to change something, write it as a follow-up note, not a code change.
- Speculate beyond what the code shows. If you're not sure, say "I do not know — needs a human."
- Generate plausible-sounding but uncertain claims. Brownfield code is full of "this should be true but isn't" patterns. Be skeptical.

## Why this skill exists

The two-week read-only period is the highest-leverage step in brownfield migration. It surfaces:
- Invariants that need to go into CLAUDE.md
- Documentation that didn't exist
- Questions for human experts before they leave the company
- Confidence that the harness (golden master, tests) actually covers the right things

Skipping this step and going straight to "let the agent edit" is the most common brownfield failure mode.
