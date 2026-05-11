# The 3-workstream pilot that learned more than it shipped

## Setting

A mid-size US-based engineering organization running its first serious AI-tooling pilot. Q1 2026. Three workstream leads, each a senior engineer with three or more years of agent-assisted development. The platform team had already shipped a starter skill library, a subagent roster, and a hook framework. Claude Enterprise seats and approved token budget. By the readiness scorecard in Appendix H of the handbook, the team scored 47 — readiness work needed but not blocking. They started anyway.

## Situation

Three workstreams ran in parallel, each with its own pilot lead and its own auditor agent:

1. **Tickets and proportional rigor** — a Slack-resident ticket-architect assistant, workshopping incoming feature requests and producing T1/T2/T3 specs at proportional depth, with an auditor agent flagging thin specs.
2. **Legibility and AI-readability** — auditing the company's primary repository for AGENTS.md gaps, missing READMEs, and ambiguous naming, paired with a "legibility copilot" subagent that drafted READMEs on demand.
3. **Infrastructure and verification** — an autonomous SRE-style agent that could investigate alerts and apply low-blast-radius fixes (rotate a secret, restart a node), paired with a validation auditor that ran every proposed action through a dry-run plus a deterministic safety check.

The goal: ship working agents at the appropriate autonomy level for each workstream within six weeks.

## What happened

The first three weeks produced almost no shippable output and a great deal of education. Nine specific lessons came out of the first run, in roughly the order they hurt:

1. **README self-containment matters more than budgeted.** Generated READMEs referenced "the team's standard testing approach" — meaningless to the next agent that read them.
2. **`/tmp` on macOS is per-user and aggressively cleaned.** Two SRE-agent runs lost intermediate state. Lesson: project-local `.agent/scratch/`, not `/tmp`.
3. **The mega-PR problem is real.** The legibility copilot, given "improve AGENTS.md across the repo," produced a 2,400-line PR touching 47 files. Rejected, broken into 11 smaller PRs. Total wallclock longer; total reviewer time shorter; merge confidence higher.
4. **Auditor agents hallucinate findings to seem useful.** The legibility auditor flagged "missing test coverage" on packages that had robust tests in non-default locations. Fix: prompt addition — *"If no findings, say so explicitly. Do not invent issues to seem useful."*
5. **Naming confusion: staging / testing / preprod / QA.** The SRE agent ran a recovery against the wrong environment because the runbook said "staging" and the company had three environments called staging in different documents. Validation auditor caught it before the second step. Closest call of the pilot.
6. **Parallel/sequential ambiguity in tickets.** "Update the README, add the missing tests, and rename the ambiguous module" got attacked all at once and produced a tangled diff.
7. **`agents.md` casing matters in some toolchains.** Two tools were case-sensitive; three repos ended up with three different casings before someone noticed.
8. **`mkdir -p` saved them repeatedly; `mkdir` cost them.** Directory-not-found failures led the agent into scattered partial state on retry.
9. **`gh` CLI scoped to read-only tokens beat the GitHub MCP for cross-repo reads.** Fancier wasn't better.

## What they did

Two practices proved themselves repeatedly and were elevated to mandatory for the second run:

**The inverted brief.** When a workstream lead asked Claude in plan mode "what context do you need to do this well?" before writing the spec, the resulting spec was sharper, the agent's first attempt was closer, and the failed-one-shot rate was lower. When a lead skipped this and wrote the spec from their own assumptions, failure rates went high enough that the next session almost always started over.

**The four-bucket Friday triage.** Five-minute Score / Question / Opportunity / Train classification on the week's failed attempts. Each Opportunity became a legibility ticket the next week. Each Train became a coaching note for the spec writer. Each Question became a calibration data point for which model to use next time.

For the second three-week run:
- Hooks enforced the PR size limits absolutely — no overrides.
- Inverted brief required on every T2 and T3 ticket; T1 tickets skipped it intentionally.
- `agents.md` casing, environment naming, `/tmp` usage all moved to CLAUDE.md and a pre-commit hook.
- Auditor agents got the "do not invent findings" clause and a regression test that fed them a clean diff to confirm they returned "no findings" appropriately.
- Friday triage moved from nice-to-have to required, with a shared spreadsheet.
- `gh` CLI got wrapped in a thin company script enforcing read-only tokens and logging cross-repo reads.

## Outcome

Wallclock time-to-merged-PR on equivalent T2 work dropped roughly 40% compared to the first run. Token cost stayed roughly flat — the harness investment didn't show up as cheaper sessions; it showed up as fewer wasted sessions. Reviewer time per PR dropped substantially.

By the fifth week, the team had a working ticket-architect, a working legibility auditor, and a working SRE agent operating at a low-blast-radius autonomy level. None of those agents were building themselves; the engineers were still doing the architectural and direction work. But the agents were taking on tier-appropriate execution, and overall throughput was visibly higher than the pre-pilot baseline.

The most valuable artifact of the pilot was the lessons document this story is drawn from.

## Lesson

**The harness compounds across workstreams.** Every hook, skill, and AGENTS.md addition that came out of one workstream made the other two faster. By the end of the pilot, the team had shared infrastructure that would have taken months to build deliberately.

**The pilot's success was not measured by the agents' success.** It was measured by what the team learned about how to operate them. The agents were the means; the operational knowledge was the end.

## What would have prevented it

The first-run failures were largely the predictable ones from chapters 6, 19, and 21 of the handbook (README self-containment, PR size limits, ambiguous environment names). A two-week pre-pilot harness sprint focused on encoding those lessons into hooks and templates would have absorbed most of the first run's pain. The trade-off: it would have delayed the pilot start by two weeks and produced a less dramatic learning curve. The team chose to learn the hard way; teams reading this can choose otherwise.

---

**Source:** Appendix L §L.1–L.4 of _Software Engineering with AI_ by Ryan Byrd
**Submitted:** May 2026
