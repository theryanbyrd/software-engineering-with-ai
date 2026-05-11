# Integration with the Slop Detector

How postmortem findings feed back into `scripts/slop-detector.py`. The point: each AI-related incident should either confirm the detector caught the issue OR identify a heuristic gap that gets closed within 1-2 weeks.

## The feedback loop

```
Incident → Postmortem → Slop signature identified → 
  → If detector flagged it: discipline question (why did the team dismiss the warning?)
  → If detector should have flagged it: heuristic gap (open issue, update detector)
  → If detector cannot flag it: signature is too subtle for current heuristic (document; revisit annually)
```

This loop is what turns the slop-detector from a static check into a learning system tied to actual production failures.

## During the postmortem

In the slop-signature section of the postmortem template, the question is asked:

> Was this signature detectable by `scripts/slop-detector.py`?
> - [ ] Yes, and the detector did flag it (but the warning was dismissed)
> - [ ] Yes, and the detector should have flagged it (heuristic gap)
> - [ ] No, the signature is too subtle for current heuristics
> - [ ] N/A — no slop signature was present

Each option triggers a different follow-up.

### Option 1 — Detector flagged it but warning was dismissed

The detector did its job. The team didn't act on the warning. This is a discipline issue, not a tooling issue.

**Investigation:**
- Where in the workflow was the warning dismissed?
- Who dismissed it?
- What was the reasoning at the time?

**Common findings:**
- Reviewer dismissed the warning without investigation ("looks fine, the detector is too noisy")
- The author dismissed the warning because the test suite passed
- The warning was buried in CI output and not surfaced in PR review UI
- The team has a pattern of high-volume dismissals which makes the next dismissal default

**Action items:**
- If the warning was buried: improve the surfacing (PR comment, status check that visibly fails)
- If the warning was dismissed reflexively: review the detector's noise level; if signal is good, address the team practice
- If the warning was correctly dismissed in another case but wrongly here: consider whether the heuristic needs refinement

**Example postmortem entry:**

> The slop-detector flagged this PR with "Possible S5 — security check removal." The reviewer dismissed the warning with the comment "the new endpoint inherits security from the API gateway." This was incorrect; the API gateway's security checks don't cover this code path. Action: improve PR review UI to require an explicit reason for dismissing slop-detector warnings; reviewer dismissals get a CODEOWNERS check on sensitive paths.

### Option 2 — Detector should have flagged it (heuristic gap)

The signature was present, the detector missed it, and a tightened heuristic would catch it next time. This is the highest-value path — the detector becomes more useful.

**Investigation:**
- What's the specific pattern that should have triggered?
- Why didn't the current heuristic catch it?
- Is the new pattern detectable mechanically?

**Action items:**
- Open an issue against `scripts/slop-detector.py` with the pattern
- Implement a new heuristic or refine an existing one
- Re-run the detector against the original PR; verify the new heuristic flags it
- Run the detector against the past 30-90 days of PRs to estimate false positive rate
- Ship the heuristic update if the FP rate is acceptable (typically <5% of PRs flagged)

**Example postmortem entry:**

> The detector did not flag this S2 (deleted edge cases). Investigation: the deleted branches were in the old code that was removed; the detector's current heuristic looks at the new code only. Action: open issue [#detector-42] to add a "branch coverage delta" check that compares cyclomatic complexity of removed code vs. added code. PR with implementation: [link].

### Option 3 — Signature too subtle for current heuristics

The signature was real but mechanical detection isn't feasible without unacceptable false positive rates. This is the rarest case and gets documented for revisit.

**Investigation:**
- What makes detection subtle? Context-dependent? Domain-specific?
- Could a subagent (LLM-based check) catch it where a heuristic can't?
- Is the pattern rare enough that human review remains the right gate?

**Action items:**
- Document in the detector's "known gaps" section
- Consider adding a subagent check (Sonnet-tier review) for the relevant file paths
- Annual review: has detection technology improved enough to reconsider?

**Example postmortem entry:**

> The signature was S6 (unnecessary new abstractions), but the abstraction was sophisticated and looked legitimate. A heuristic check would produce too many false positives. Mechanical detection is not the right gate; senior review is. Action: add to detector's "known gaps" doc. Add CODEOWNERS for files in `src/architecture/` requiring senior review.

### Option 4 — No slop signature applied

The incident is AI-related but doesn't match any of the seven signatures. Document explicitly. Categorize via DeepSet (context, constraint, verification, planning) instead.

**Action items:**
- Update the DeepSet category section accordingly
- Use [`harness-deficiency-checklist.md`](harness-deficiency-checklist.md) to identify the right harness mechanism
- The slop-detector is not the right tool here; don't tighten its heuristics for this kind of failure

## Updating the slop-detector

The maintainer of `scripts/slop-detector.py` reviews postmortem-driven heuristic-gap issues monthly. The cadence:

1. New issues opened from postmortems are tagged `slop-detector-gap`
2. Monthly review: maintainer triages, prioritizes, implements 1-3 per month
3. Each new heuristic is tested against the past 90 days of merged PRs to estimate false positive rate
4. Heuristics with >5% FP rate are tuned or rejected
5. Approved heuristics are shipped with documentation in the detector's README

The detector's CHANGELOG records each heuristic with the postmortem(s) that drove it. This is institutional memory; future engineers can see why each check exists.

## What NOT to do

- **Don't update the detector to catch a one-off pattern.** If the pattern only ever caused one incident, the heuristic isn't durable. Document the pattern in the detector's "known gaps" doc; revisit if it recurs.
- **Don't ship a heuristic that has high FP rate "because we want to catch this kind of thing."** False positives kill detector trust. Engineers learn to ignore noisy detectors. A noisy detector is worse than no detector.
- **Don't expect the detector to catch everything.** The detector is a floor; senior code review is the ceiling. Some signatures (especially S6 and parts of S7) have an irreducible human-judgment component.
- **Don't add a heuristic without testing on historical PRs.** Surprises in production cause incidents. Test on 90 days of merged PRs first.

## Tracking the loop's effectiveness

Quarterly metric: "Of AI-related incidents this quarter, what % involved slop signatures the detector flagged but the team dismissed?"

- 0-10%: detector + team are well-calibrated
- 10-30%: detector is producing useful signals; investigate dismissal patterns
- 30-50%: detector is good but team isn't using it; UX or process problem
- >50%: detector is too noisy and engineers have learned to ignore; tune the heuristics

The metric isn't perfect (it doesn't capture the incidents the detector successfully prevented), but it's directional. A team where the detector catches things the team missed in review is a team learning faster than a team where the detector is silent.

## Companion artifacts

- `scripts/slop-detector.py` — the detector itself
- [`postmortem-template.md`](postmortem-template.md) — where the integration triggers
- [`SLOP_SIGNATURE_REFERENCE.md`](SLOP_SIGNATURE_REFERENCE.md) — the seven signatures the detector targets
- Ch 22 §22.2 — the source of the signatures
- Ch 31 §31.6 — the broader attribution toolkit
