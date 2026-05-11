# Weekly Retro Structure

The retro section that runs the triage. Per Ch 44 §44.4 item 4: "Run the failed-one-shot triage every retro."

## When in the retro

The triage section runs near the end of the retro — after the discussion of what went well / what didn't, before the action items. Place it where the team has context but isn't yet rushing to wrap up.

15-20 minutes is sufficient for most teams. If consistently running over, the team may have too many ungrouped failures or the triage is being over-discussed.

## Agenda

### Section 1 — This week's data (3-5 minutes)

The triager (or a designated facilitator) presents:

- **Total agent invocations this week** (from gateway data; rough number)
- **Total failures logged** (from the shared spreadsheet)
- **First-pass classification breakdown** (Score / Question / Opportunity / Train counts)
- **Trend vs last 4 weeks** (rough — are we trending up, down, flat?)

This sets context. The team sees the shape of the week before drilling into specifics.

### Section 2 — Walk the failures (8-12 minutes)

For each logged failure:

1. **Reference the spec / ticket** (link)
2. **Engineer who logged it speaks briefly** (1-2 sentences: what happened)
3. **Confirm classification** (or revise based on discussion)
4. **Identify resolution path** (per [`closing-the-loop.md`](closing-the-loop.md))
5. **Assign owner** (if action is needed)

For most teams, 5-10 failures per week. Walking takes 60-90 seconds per failure when the discussion is focused.

### Section 3 — Patterns (3-5 minutes)

The triager surfaces patterns:

- **Multiple failures on the same module**: legibility ticket for that module
- **Multiple Train failures from the same author**: 1:1 coaching for the author (not in retro; mentioned only)
- **Multiple Question failures on the same work type**: routing or capability gap; flag for next quarterly review
- **Score patterns**: this work type is going well; consider raising autonomy ceiling

Patterns are where the leverage is. Individual failures are interesting; patterns inform structural improvements.

### Section 4 — Action items (2-3 minutes)

The retro's action items section captures:

- Specific Opportunity tickets created (links)
- Specific Train coaching scheduled (private; just "X has 1:1 with manager")
- Specific Question entries flagged for next model review

These items are tracked through the retro's normal mechanism.

## What good triage discussion looks like

Healthy:
- Engineers speak briefly and factually about what happened
- Classifications are confirmed quickly (most failures aren't ambiguous)
- Resolution paths are clear
- Patterns are surfaced when they exist
- Total time stays under 20 minutes

Concerning:
- Every failure becomes a 5-minute debate
- Classifications are revised multiple times
- Resolution paths aren't clear
- Patterns aren't surfaced
- Triage section consistently runs over

## Common discussion patterns

### "I'm not sure if this was Opportunity or Train"

Most common ambiguity. Default to Train; test by improving spec. If that doesn't work, reclassify.

### "The agent should just be smarter"

A frustrated framing of Question. The triager redirects: "Capability is what we have today; what's the actionable bucket — should we route this to humans, escalate to Opus, sharpen the spec?"

### "I think I had 12 failures this week, not the 3 I logged"

The engineer didn't log most failures. The discipline broke down. Coach toward better logging — not punitively.

### "The harness should have caught this earlier"

Sometimes true. The triage is the catching mechanism; the resolution is the harness improvement.

### "I don't think this is a real failure"

The agent produced something the engineer rewrote. Whether it's "real" is a judgment call. Default: if the engineer rewrote substantial parts, it's a failure (likely Train or Opportunity).

## Adapting the structure

### Smaller team (3-5 engineers)

15 minutes is sufficient. Walking 5-7 failures takes 8 minutes; patterns are quick.

### Larger team (10-15 engineers)

20-25 minutes. May need to triage by sub-team. Or do one round of triage covering only patterns rather than individual failures (with the per-failure detail in the spreadsheet).

### Very large team (20+)

Sub-team triage with cross-team aggregate at a higher cadence (monthly). The weekly cadence stays within sub-teams.

### When the team has no failures

The week was quiet. Spend 5 minutes on it anyway:
- Confirm the data (people are logging when they fail)
- Look at the Score data
- Look at trends
- Note what's working

A no-failure week is a positive signal. Don't skip the section to celebrate; use the time to lock in patterns.

### When the team has many failures (20+)

Don't try to walk all 20. Group by:
- Common spec author (Train cluster)
- Common module (Opportunity cluster)
- Common work type (Question or routing cluster)

Walk the clusters, not the individuals.

## Integration with the team's broader retro

The triage is one section of the retro, not the whole retro. The team's normal retro structure (what went well / what didn't / action items) continues; triage slots in as one section.

If the team's retro is already crowded, the triage may need its own 30-minute meeting. Most teams find 15-20 minutes within the existing retro is fine.

## Anti-patterns

### Skipping the section

"We were running over so we skipped triage this week." Once is fine; pattern is not. Skip enough and the discipline collapses.

Mitigation: protect the time. If retros are consistently running over, fix the retro structure, not the triage.

### Triage in isolation

The triage section runs but the action items don't connect to retro action items. Resolutions get lost.

Mitigation: triage feeds the retro's action items section. Same tracking.

### Triage as theater

The team goes through the motions but classifications are perfunctory. No real diagnostic value.

Mitigation: the triager engages substantively. Patterns get surfaced. Real action items result.

### Triage as gotcha

Engineers feel ambushed during triage ("here's your failure list publicly!"). Stop logging.

Mitigation: triage tone is operational. Train coaching is private. Public discussion is about the work, not the engineer.

### Triage without continuity

Each week's triage is independent. No tracking of whether last week's resolutions actually shipped.

Mitigation: open Opportunity tickets are reviewed at the start of the next week's triage section. "Last week's billing-module ticket — what's the status?"

## When to escalate beyond retro

Some failures or patterns warrant escalation beyond the team retro:

- **Multiple Train failures from the same PM**: manager has a structured coaching conversation
- **Multiple Question failures on a work type**: tech lead raises in next quarterly model review
- **Multiple Opportunity failures in a module**: structural harness investment may need approval beyond team capacity
- **Single failure that produced a production incident**: postmortem (separate process)

The retro triage doesn't try to solve every problem; it surfaces the ones that need action and routes appropriately.

## Companion artifacts

- [`triage-process.md`](triage-process.md) — the workflow
- [`the-four-buckets.md`](the-four-buckets.md) — the taxonomy
- [`tracking-spreadsheet-template.md`](tracking-spreadsheet-template.md) — the data structure
- [`closing-the-loop.md`](closing-the-loop.md) — what happens after
- [`reading-the-ratios.md`](reading-the-ratios.md) — the longer view
- Ch 44 §44.4 item 4 — source
