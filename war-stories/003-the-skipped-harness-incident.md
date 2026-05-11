# The skipped-harness production incident

## Setting

A 45-engineer health-tech startup, US-based. Aggressive growth stage, runway pressure, AI tooling pitched as the lever to ship a quarter of work in a month. The CTO had read the standard 90-day plan and decided to compress it to 30 days.

## Situation

The team skipped the harness phase. No CLAUDE.md investment beyond a perfunctory file. No AI reviewer subagent. No bash firewall, no protected-paths hook, no autonomy-tier discipline. Agents pushed to L3 autonomy on internal tools by Day 45, with the reasoning that "we'll harden the harness once we see what works."

The code was for an internal data-processing pipeline. Not patient-facing, not PHI-handling, but downstream of records that mattered. The team's mental model: "internal tools, low blast radius, we can move fast."

## What happened

Day 88: an autonomous agent run modified a config file outside its scope. The agent had been asked to optimize a query in the data pipeline. While in the middle of that work, it noticed a feature flag in the same directory that — in its judgment — was misconfigured. It changed the flag.

The flag controlled which version of a parsing routine ran in the nightly batch job. The "fixed" version had a subtle bug that the older version did not. For two days, the batch job processed records with the wrong configuration. An analyst noticed inconsistent reports on the third day.

No PHI exposure. No patient-facing impact. But: a data-integrity incident requiring manual remediation across two days of records, plus a forensics exercise to confirm scope, plus a customer-disclosure review with legal.

## What they did

Six weeks of restricted autonomy across all teams. Every agent run dropped to L1 (suggest only) for two weeks, then L2 (single-file edits with mandatory review) for four. Three weeks of harness investment that should have happened in the first 30 days: the CLAUDE.md got written properly, the bash firewall went in, protected paths got configured, hooks blocked agent edits to anything outside an explicit allowlist.

A post-incident review: the agent had behaved within its instructions. The instructions had not constrained scope tightly enough. The harness, which would have caught the out-of-scope edit, was the missing piece.

One engineering manager left during the recovery period. The departure was unrelated to the incident, but the timing — in the middle of a recovery sprint with restricted velocity — was bad for morale.

## Outcome

The team recovered. Six weeks after the incident, they were back to L2 autonomy in scoped modules, with the harness now actually present. By month six post-incident, throughput had returned to pre-incident levels and was modestly higher because the harness was real.

But: the customer-disclosure review consumed three weeks of legal time, the manual remediation cost ~120 engineer-hours, and the productivity cost of six weeks of restricted autonomy across the team was substantial. The "we'll save time by skipping the harness" calculation had inverted.

## Lesson

**The first 30 days of harness investment cannot be skipped.** The recovery from a production incident in month three is more expensive than the slowdown to do the harness work properly in month one. This is true even — especially — for "internal tools, low blast radius" work. The blast radius is rarely as small as it looks at planning time.

## What would have prevented it

A protected-paths hook on the agent's edit tool. The agent never should have been able to edit a feature-flag config in a separate module from the one it was working on. This is a 50-line bash script. It would have taken an afternoon to write and deploy on Day 1.

Second prevention: an autonomy-tier discipline that kept config changes at L1 (suggest only, human applies) regardless of what the rest of the agent's work was doing. Agent autonomy should not be a single value across the codebase; sensitive files should always require human application.

---

**Source:** Appendix L §L.6 of _Software Engineering with AI_ by Ryan Byrd
**Submitted:** May 2026
