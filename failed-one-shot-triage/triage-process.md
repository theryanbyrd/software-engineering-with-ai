# Triage Process

The actual workflow — when, how, by whom. Per Ch 31 §31.5: "Capture this in the standup or weekly review. Do not bother building elaborate tooling for it; a shared spreadsheet works."

## Who triages

The team's tech lead, engineering manager, or designated platform-team representative. One person per cycle; the role can rotate.

The triager doesn't decide alone — the weekly retro is where the team validates the classifications. The triager prepares; the team confirms.

## When to triage

### Throughout the week — capture as it happens

When an agent invocation fails to produce a merged PR on the first run, the engineer logs it in the shared spreadsheet:
- Date
- Engineer
- Spec / ticket reference
- What was tried (model, prompt, etc.)
- What happened (specific failure mode)
- Initial classification (engineer's first guess)

This isn't the triage itself — it's the data collection. The triage happens at the retro.

### At the retro — classify and decide

The triager (or facilitator) walks through the week's logged failures. For each:
1. Confirm the classification (Score / Question / Opportunity / Train)
2. Identify the resolution path
3. Assign owner if action is needed

This takes 10-15 minutes for most teams; the bulk of the work is the data collection during the week.

## What gets triaged

**Failures**, specifically: agent invocations that didn't produce a mergeable PR on first run.

This includes:
- Agent gave up
- Agent produced wrong code (failed verify)
- Agent produced code that engineer had to substantially rewrite
- Agent produced code that engineer rejected outright

Successes (Score) get logged for the trend data, but they don't need triage — the classification is unambiguous.

## What does NOT get triaged here

- **Production incidents** that came from AI-authored code: those go through `incident-postmortem-templates/` separately. Reference back to triage data if relevant.
- **Spec issues that didn't reach the agent**: if a spec was rejected before invocation, that's PM workflow, not triage.
- **Tooling failures**: agent crashed; gateway returned error. Those are platform issues, not triage data.

## The triage workflow per failure

### Step 1 — Engineer logs the failure

When a failure happens, the engineer captures:
- Spec reference (link to ticket)
- Model used
- Approximate cost (from gateway data)
- What the agent did wrong (1-2 sentences)
- Initial guess at classification

This takes 60-120 seconds per failure. Don't make it expensive or engineers will skip it.

### Step 2 — Triager reviews before retro

Before the retro, the triager:
- Reads through the week's logged failures
- Spots patterns (multiple failures on the same module; multiple Train failures from the same PM; multiple Question failures on the same work type)
- Drafts the triage classification (may differ from engineer's initial guess)

### Step 3 — Retro discussion

In the retro:
- Walk through each failure (5-10 per week is typical for a team of 5-8 engineers)
- Confirm or revise classification
- Identify resolution path
- Assign owner

### Step 4 — Resolution

Per [`closing-the-loop.md`](closing-the-loop.md), each bucket has a different resolution path:
- Score → no action (logged for trend data)
- Question → flag for next model release; route to humans for now
- Opportunity → open legibility ticket; harness improvement
- Train → coach spec author; iterate

### Step 5 — Track

The shared spreadsheet (per [`tracking-spreadsheet-template.md`](tracking-spreadsheet-template.md)) is the canonical record. Per Ch 31 §31.5: "do not bother building elaborate tooling."

## How to handle ambiguous cases

Many failures could be classified as multiple buckets. Conventions:

### "Could be Train or Opportunity"

Default to Train. A better spec is almost always cheaper than a harness improvement. Try the spec fix first; if that doesn't work, reclassify as Opportunity.

### "Could be Opportunity or Question"

Test by adding the missing context manually and retrying. If the agent then succeeds, it was Opportunity. If still fails, it's Question.

### "Could be Train or Question"

Test by writing a perfect spec and retrying. If the agent succeeds, it was Train. If still fails, it's Question.

The discipline: don't default to Question. Train and Opportunity are fixable; Question implies "we can't help." Most failures classified as Question by engineers turn out to be Train or Opportunity on closer examination.

## Tone

Triage is harness-focused, not engineer-focused. Specifically:

- "The agent failed" not "the engineer failed"
- "The spec was unclear" not "the PM is bad at writing specs" (unless coaching specifically; even then, in 1:1)
- "The harness is missing X" not "we should have known to add X"

The triage data feeds harness improvement. If engineers feel surveilled, they stop logging failures, and the discipline collapses.

## Anonymity

For the team's trend data, classifications are typically anonymous. The Train coaching is private (1:1); the team doesn't see "PM Alice's Train ratio." The Opportunity work is public (it's about the harness, not the engineer).

Some teams identify failures by author for internal use; the test is whether engineers continue to log honestly. If logging drops, anonymity is the fix.

## Cadence

Weekly retro. Don't skip — even when the week was quiet, walking the data takes 5 minutes.

If the team is too small to support weekly retros, monthly is acceptable but loses some signal. Less than monthly: the discipline becomes performative.

## What the triager needs

- Access to the shared spreadsheet
- Engineering judgment to distinguish the buckets
- Authority to assign owners for Opportunity work
- Time during retro (15-20 minutes for the triage section)

## Anti-patterns

### Triage without action

Failures are logged and classified; no resolution happens. The data isn't useful.

Mitigation: every classified failure has a resolution path and an owner. Per [`closing-the-loop.md`](closing-the-loop.md).

### Triage as performance review

The triage data is used in performance reviews ("Engineer X had Y failures last quarter"). Engineers learn to game by not logging or reclassifying.

Mitigation: explicit boundary. Triage is operational, not evaluative.

### Triage by committee

Every failure debated extensively. The retro time is consumed; triage feels heavy.

Mitigation: the triager prepares; the team validates quickly. Most failures take 30 seconds to confirm.

### Triage tool overhead

A custom tool is built for triage. Maintenance overhead exceeds the value.

Mitigation: per Ch 31 §31.5, a shared spreadsheet works. Don't build elaborate tooling.

### Triage without follow-through on Train

Train failures keep happening from the same author; coaching doesn't materialize.

Mitigation: 1:1 coaching is the resolution. If the manager doesn't run the coaching, Train accumulates.

### Triage that misses pattern data

Each failure is triaged in isolation; patterns across failures aren't surfaced.

Mitigation: the triager looks for patterns before the retro. "We have 4 Opportunity failures this week, all in the billing module — let's get a billing legibility sprint scheduled."

## Companion artifacts

- [`the-four-buckets.md`](the-four-buckets.md) — the taxonomy
- [`weekly-retro-structure.md`](weekly-retro-structure.md) — when this runs
- [`tracking-spreadsheet-template.md`](tracking-spreadsheet-template.md) — the data structure
- [`closing-the-loop.md`](closing-the-loop.md) — what happens after
- Ch 31 §31.5, Ch 19 §19.5 — sources
