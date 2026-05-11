# Mitigation 1 — The AI Reviewer Subagent

The first-pass filter. Per Ch 44 §44.5:

> The AI reviewer subagent on every PR. Not as a replacement for human review — as a first-pass filter. The subagent flags slop signatures, missing tests, and scope creep. The human reviewer reads the subagent output, then reads the diff. Net: 30-40% time saved per PR for the human, with no quality loss observed in most teams (Chapter 14 §14.3).

The single highest-leverage mitigation. Implement first.

## What the subagent does

The AI reviewer subagent runs on every PR. Specifically:

- **Reads the diff** — the agent has full context of what changed
- **Reads the spec / ticket** — knows what the PR is supposed to accomplish
- **Reads the team's CLAUDE.md / AGENTS.md** — knows team conventions
- **Reads relevant skills** — knows the team's review patterns
- **Produces structured review output**

The output covers:

1. **Slop signatures** (per Ch 22 §22.2):
   - S1: Mocking implementation rather than asserting behavior
   - S2: Type errors introduced
   - S3: Style inconsistency with surrounding code
   - S4: Missing tests for changed behavior
   - S5: Comments hallucinated as documentation
   - S6: Unnecessary abstractions
   - S7: Diff bloat / pattern divergence

2. **Missing tests**:
   - Specific behaviors changed without test coverage
   - Specific edge cases not covered

3. **Scope creep**:
   - Files changed that weren't necessary for the spec
   - Unrelated changes bundled into the PR

4. **Architectural concerns**:
   - Layering violations
   - Pattern divergence from team conventions
   - Invariants violated

The output is posted as a comment on the PR; the human reviewer reads it before reading the diff.

## What the subagent does NOT do

- **Approve or reject the PR** — only humans can do that
- **Replace human review** — humans still read the diff
- **Catch everything** — subtle issues require human judgment

The subagent is a first pass. Per Ch 22 §22.3 (the two-tier review):
- Tier 1 (subagent): catches the obvious
- Tier 2 (human): catches the substantive

## Why this saves 30-40% of human review time

Per Ch 44 §44.5: "Net: 30-40% time saved per PR for the human, with no quality loss observed in most teams."

The mechanism:
- The reviewer reads the subagent output first (5-10 minutes for a typical PR)
- Subagent has flagged the obvious issues; the reviewer doesn't have to find them
- The reviewer's attention focuses on the issues the subagent doesn't catch
- The reviewer's read of the diff is faster because the obvious ground is covered

Without the subagent:
- The reviewer finds slop signatures themselves (5-10 minutes)
- Reviewer fatigue accumulates faster
- Some slop slips through (especially under time pressure)

With the subagent:
- The slop signatures are surfaced before review
- The reviewer's energy is reserved for harder issues
- Quality stays high or improves

## Building the subagent

### Where it lives

Typically `.claude/subagents/reviewer.yaml` or equivalent. Per the team's standard subagent infrastructure.

### The prompt

The subagent's prompt covers:
- Read the diff
- Read the spec / ticket
- Read CLAUDE.md and relevant AGENTS.md
- Apply the seven slop signatures
- Apply team-specific patterns (from skills, from CODEOWNERS rules)
- Output structured review

### The output format

A standard format the human reviewer expects:

```markdown
## AI Reviewer — First-Pass Notes

### Slop signatures detected
- [S1] Mocking implementation in `tests/auth_test.py:142` — recommend asserting behavior instead
- [S4] No test added for new error path in `handler.py:88`

### Missing tests
- Edge case: empty input not tested in `validator.py`

### Scope concerns
- `unrelated.py` changes appear unrelated to spec; consider splitting

### Architectural notes
- New direct call to `db_layer` from UI; CLAUDE.md prohibits this — see `services/auth/AGENTS.md`

### What I think looks good
- Migration is well-structured with rollback path
- Test coverage on new feature is solid

---
*This is an automated first-pass review. Human review still required.*
```

The format is consistent so reviewers can scan it quickly.

### The model

Per `cost-discipline-runbook/model-routing-rubric.md`, the reviewer subagent typically runs on Sonnet — substantive enough to catch real issues, cheap enough to run on every PR.

For high-stakes paths (auth, billing, migrations), consider escalating to Opus per `agent-autonomy-levels/forbidden-categories.md`.

### The trigger

The subagent runs:
- On PR open (initial review)
- On PR update (re-review when commits are pushed)
- On request (engineer can invoke explicitly)

Don't run on every commit (too expensive); run on PR-level events.

## What good subagent output looks like

Healthy:
- Catches real issues (slop signatures, missing tests, scope creep)
- Output is consistent across PRs
- False positive rate <10% (output the human reviewer dismisses)
- False negative rate is qualitative (does the human still find issues the subagent missed? sometimes yes, but the volume is reduced)

Concerning:
- High false positive rate (reviewer ignores subagent output)
- Catches obvious issues but misses substantive ones
- Output format inconsistent (reviewer can't scan it efficiently)

## Tuning the subagent

The subagent's heuristics drift over time:
- New patterns emerge (a new convention in the codebase)
- Old patterns deprecate (a pattern the subagent flags is no longer wrong)
- New slop signatures emerge

Quarterly review of the subagent:
- Pull recent subagent outputs
- Compare to actual issues humans found
- Update the subagent's prompt / patterns based on the gap

If the subagent's false positive rate is climbing, engineers learn to ignore. Tune to keep it relevant.

## Common implementation issues

### Subagent output is too long

The subagent produces 50 bullet points per PR. The reviewer skims; misses important issues.

Mitigation: limit output to 5-10 most-important findings. Anything else goes in a "lower priority" section.

### Subagent output is too generic

Every PR gets the same boilerplate. Reviewers ignore.

Mitigation: subagent's prompt requires specific findings. If no slop signatures detected, say so explicitly.

### Subagent runs but output isn't read

Reviewers approve PRs without reading the subagent output. Defeats the purpose.

Mitigation: workflow integration. The subagent's output is in the PR description or pinned comment; reviewers see it before approving.

### Subagent's findings are wrong

The subagent flags issues that aren't real. Reviewers learn to dismiss.

Mitigation: tuning. The subagent's prompt gets better through iteration.

### Subagent quality drops as model changes

A new model release shifts subagent behavior. Output quality degrades or improves.

Mitigation: include the subagent in the quarterly model lineup review (per `evals-and-benchmarks-runbook/quarterly-model-lineup-review.md`). Test whether the subagent's quality changes.

## Cost

Per `cost-discipline-runbook/`, the subagent has cost. Approximate:
- $0.10 - $0.50 per PR review (Sonnet, typical PR size)
- Across 100 PRs/week: $10-50/week per team

Compared to engineer time saved (30-40% of review hours), the cost is negligible.

## Anti-patterns

### Subagent as replacement for human review

Some teams treat the subagent's approval as sufficient. Quality erodes; the subagent doesn't catch everything.

Mitigation: the subagent is a first pass. Human review remains required.

### Subagent without team-specific tuning

A generic subagent prompt is used. Output is generic; doesn't catch team-specific patterns.

Mitigation: per Ch 14 §14.3, subagents are tuned to the team. Generic templates are starting points, not final products.

### Subagent that doesn't update

Built once; not maintained. Patterns drift; subagent becomes stale.

Mitigation: quarterly subagent review.

### Subagent that's too aggressive

Flags everything as a slop signature. Reviewers stop trusting the output.

Mitigation: tune toward precision over recall. Better to miss some issues than to over-flag.

## Companion artifacts

- `governance/subagents/` — where the subagent lives
- Ch 14 §14.3 — the AI reviewer subagent pattern
- Ch 22 §22.2 — the seven slop signatures
- Ch 22 §22.3 — two-tier review
- `cost-discipline-runbook/model-routing-rubric.md` — model selection
- Ch 44 §44.5 mitigation 1 — source
