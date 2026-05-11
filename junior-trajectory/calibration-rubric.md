# Calibration Rubric — Is This Junior On Track?

Specific signals at 6, 12, and 18 months. The rubric is designed to surface "this junior needs different support" early enough to act, and to surface "this junior is genuinely off-track" honestly when that's the case.

The rubric is paired with [`18-month-curriculum.md`](18-month-curriculum.md). Each calibration window corresponds to a phase exit criterion.

## How to use

1. Manager and primary mentor each fill out the rubric independently.
2. Compare. Disagreements are conversations to have before the next step.
3. Calibrate the result against junior peers in the same phase across the org (if any).
4. Run the conversation with the junior. Rubric is shown; coaching is verbal.

The honest assessment matters more than the kind one. A junior who is told they're on track when they're not loses 6+ months of useful course-correction time.

---

## 6-month calibration

Maps to phase 1 exit (review discipline).

### Strong signals (junior is on track)

- [ ] Reviews PRs with substance — comments are specific, not generic
- [ ] Has caught a non-obvious bug in someone else's PR at least once
- [ ] Can articulate the seven slop signatures without prompting
- [ ] Pushes back constructively on PRs; doesn't rubber-stamp
- [ ] Asks clarifying questions in the agent session that improve the output
- [ ] Engaged with the codebase beyond their own tickets — can describe modules they don't own
- [ ] Recognizes when an agent suggestion is wrong and can articulate why
- [ ] Owns at least one minor incident or bug fix end-to-end
- [ ] Postmortems they participate in are useful documents, not boilerplate
- [ ] Mentor describes them as "engaged" not "compliant"

**Calibration:** 8+ of 10 → on track. 5-7 → modest concern; conversation needed. <5 → major concern; structural change needed.

### Caution signals (early intervention warranted)

- [ ] Reviews are mostly rubber-stamps; comments are "LGTM" or absent
- [ ] Cannot explain choices in their own code
- [ ] Specs they write require multiple revisions before agent work begins
- [ ] No record of catching things in review
- [ ] Pushes back on agent suggestions but with vague reasoning ("seems off")
- [ ] Reading time has been crowded out by ticket load
- [ ] Mentor relationship is mostly nominal

**Action if 3+ caution signals:** structural change. Reduce ticket load 50%; increase mentor pairing time; explicit re-set on phase 1 expectations. Re-evaluate at 9 months.

### Hard signals (consider parting ways or significant role change)

- [ ] Cannot articulate the slop signatures even after explicit teaching at multiple sessions
- [ ] Repeatedly ships code with obvious slop signatures the junior reviewed
- [ ] Cannot follow code that they did not write themselves
- [ ] Defensive in 1:1 conversations about feedback
- [ ] Mentor reports the junior is not absorbing teaching
- [ ] No improvement over the 6-month window despite explicit feedback

**Action if 3+ hard signals:** the conversation about role fit. Possible outcomes: extended phase 1, role change (e.g., pivot to QA / Solutions Engineering), or part ways. The honest conversation is kinder than letting the program drift.

---

## 12-month calibration

Maps to phase 2 exit (small features) and the start of phase 3 (harness contribution).

### Strong signals (junior is on track)

- [ ] Ships T1 features solo without senior intervention beyond standard review
- [ ] Specs they write rarely need pre-implementation revision
- [ ] Has shipped multiple T1 features per quarter for the last 2 quarters
- [ ] Has contributed to a T2 feature with senior collaboration
- [ ] Has owned at least one substantive incident, including the postmortem
- [ ] Has fixed at least one bug in the team's existing harness
- [ ] Reviews are now genuinely useful — senior engineers respect them
- [ ] Pushes back on agent output meaningfully and routinely
- [ ] Recognized by team as a productive contributor, not a "junior who needs help"
- [ ] Net signal: someone could leave the team for 2 weeks and the junior could keep their work moving

**Calibration:** 8+ of 10 → on track for L4 trajectory. 5-7 → on track for L3 maintenance, may not yet have L4 trajectory clarity. <5 → 6-month plan needed; the junior is behind the curriculum.

### Caution signals

- [ ] T1 features still require multiple senior interventions
- [ ] Specs are vague; the junior is shipping by trial-and-error rather than by specification
- [ ] Has not shipped any harness contribution, even fixes
- [ ] Has avoided incident ownership
- [ ] Reviews are technically correct but never catch anything substantive
- [ ] Comfortable only with a narrow ticket pattern; freezes on novel work
- [ ] Cannot explain T2 work even when they were on the team

**Action if 3+ caution signals:** scope change. Identify the gap (Direction? Architecture? Engagement?) and design a 3-month intervention. Re-evaluate at 15 months.

### Hard signals

- [ ] Velocity is high but quality is poor; reviewers have to push back routinely
- [ ] Repeatedly ships work that shouldn't have been shipped (anti-pattern 1 or 2 still active)
- [ ] Cannot work without specific senior intervention even on routine tickets
- [ ] Has had no growth in scope or depth from month 6 to month 12
- [ ] Mentor reports they no longer have the patience to keep mentoring this junior

**Action if 3+ hard signals:** the harder conversation. The 12-month mark is when "this isn't working" becomes a fair assessment. PIP or transition discussion.

---

## 18-month calibration

Maps to phase 4 exit (first solo design) and L3 → L4 promotion eligibility.

### Strong signals (ready for L4 trajectory)

- [ ] Has led a small T2 design end-to-end, with senior collaboration not direction
- [ ] The design they led is shipped and operating without major issues
- [ ] Has shipped at least one harness component used by other engineers
- [ ] Maintains the harness component (responds to bugs, iterates based on feedback)
- [ ] Reviews carry weight in the team — other engineers route hard PRs to them
- [ ] Has a clear sense of which discipline (Direction / Architecture / Evaluation) is their strongest
- [ ] Has mentored or is informally helping a more junior engineer
- [ ] Can hold their own in a design conversation with seniors
- [ ] Has had at least one stress moment (incident, postmortem, hard customer) and handled it
- [ ] Net signal: the team would notice their absence within 1 week

**Calibration:** 8+ of 10 → ready for L4 trajectory; promotion conversation is appropriate. 5-7 → solid L3, not yet L4. <5 → not yet L3 at the level we'd expect for 18 months in.

### Caution signals

- [ ] Has never led a design, even with heavy senior support
- [ ] Has shipped harness work, but it's been ignored or not adopted by the team
- [ ] Reviews are still primarily on T1 work; senior PRs route around them
- [ ] No clear discipline preference — generalist by default, not by design
- [ ] Has mentored no one
- [ ] Comfortable in their lane; not stretching

**Action if 3+ caution signals:** the trajectory conversation. The junior may be a solid L3 but unlikely to make L4 in the next 6 months without explicit growth plan. Be honest with them. Some L3s stay L3 for a long time and that's fine; don't force a trajectory that isn't there.

### Hard signals

- [ ] Has shown no growth from month 12 to month 18
- [ ] Continues to need senior intervention at a level inappropriate for 18 months in
- [ ] Cannot operate independently in any meaningful scope
- [ ] Team patience is exhausted

**Action if 3+ hard signals:** the role-fit conversation. Eighteen months in is the latest reasonable point for "this isn't going to work." If you're seeing this, the earlier rubrics likely also showed signals; the program drift is the failure, not the junior.

---

## What the rubric will NOT do

- Will not assess soft skills, communication, teamwork. Those are real but not in scope here. Use your standard performance review.
- Will not be objective. The signals are observable but the manager-and-mentor judgment is required. Two managers grading the same junior may disagree by 1-2 signals; that's normal.
- Will not work without honest input from the mentor. If the mentor reports "everything's fine" without specific examples, the rubric is hollow.
- Will not work as a one-time assessment. Run all three checkpoints.

## What to do with the rubric

1. Manager and mentor independently fill out before the calibration.
2. Compare with each other.
3. Sanity check against the team's other juniors at the same phase.
4. Determine the action: continue current plan, intervene, change scope, transition.
5. Have the conversation with the junior — verbally, not by handing them the rubric.
6. Document the action plan, not the rubric, in your private notes.

## How to talk to the junior about the calibration

The conversation is not the rubric. The conversation is the honest assessment of where they are and what comes next. Use the rubric to inform what you say; don't read from it.

For an on-track junior: "You're tracking well. Specifically, [two specific things they're doing well]. The next 6 months should focus on [the next phase]; here's what I want to see by [next checkpoint]."

For a caution-signal junior: "You're solid on [specific things] and I want to make sure you grow on [specific gap]. Here's the plan for the next 3 months: [specific intervention]. Let's check in at [date] to see how it's landing."

For a hard-signal junior: "I've been thinking about how the program is going for you. Some things are working — [specifically what]. Some things aren't — [specifically what]. I want us to talk about whether this role is the right fit, or whether we need to make significant changes. Walk me through how you're thinking about it."

## Companion artifacts

- [`18-month-curriculum.md`](18-month-curriculum.md) — the program the rubric calibrates against
- [`manager-1on1-playbook.md`](manager-1on1-playbook.md) — the cadence that produces the data
- [`anti-patterns.md`](anti-patterns.md) — what the caution and hard signals usually trace back to
- `people/career-ladder/ic-track-additions.md` — the L3 → L4 promotion criteria the 18-month rubric maps to
