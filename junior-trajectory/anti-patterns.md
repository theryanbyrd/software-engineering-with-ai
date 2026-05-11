# Anti-Patterns That Kill Junior Development

Specific patterns that produce engineers who never develop, with mitigations. Direct implementation of Ch 42 §42.3's warning:

> Don't use juniors as rubber-stamp reviewers. This was the dominant antipattern of 2024–25. It produces engineers who never built the pattern library that lets them spot slop. By 18 months in, they're harder to retrain than a fresh hire.

The chapter names the headline antipattern. This file catalogs the others.

## Anti-pattern 1 — Rubber-stamp reviewer

**The pattern:** The junior is assigned PR reviews on agent-authored work without senior pre-review. They learn that "approve" is the safe answer; senior engineers don't push back on their reviews because there's no actual review happening. The junior gets credit for "doing reviews" without ever building review judgment.

**How it manifests:**
- Junior approves PRs in 30-90 seconds with comments like "LGTM!" or no comments at all
- Junior's review approval rate is ~98% (compared to 60-75% for senior reviewers)
- The junior cannot articulate, when asked, what specifically they checked
- Bugs ship that the junior reviewed but didn't catch, repeatedly

**Why it's catastrophic:**
- Engineering judgment is built on pattern recognition, which is built on examples of "this looked fine but turned out broken." Without the consequence of catching things or missing them, no patterns form.
- After 12-18 months as a rubber-stamp reviewer, the junior has the appearance of seniority (years of experience, ticket count, review volume) without the substance. They are then promoted into roles they can't perform.
- Per Ch 42 §42.3, rubber-stamp juniors are harder to retrain than fresh hires by 18 months in.

**Mitigations:**
- Phase 1 of the curriculum requires senior pre-review on every junior review for 8 weeks.
- The junior's reviews must include specific findings (or "I have no findings" with reasoning). "LGTM" alone is a no-go.
- Track the junior's review accuracy: when bugs ship that they reviewed, did they have a chance to catch it? Coach on the misses.
- Mentor reviews 2-3 of the junior's reviews per week and points to what they would have caught.

## Anti-pattern 2 — Agent-only output engineer

**The pattern:** The junior writes specs and prompts; the agent writes the code; the junior copies and ships. The junior never internalizes the patterns the agent is producing because they don't engage with the code as code.

**How it manifests:**
- Junior cannot explain decisions in their PR description ("the agent suggested X")
- Junior's code looks like every other agent's code: same patterns, same library choices, same commenting style
- Junior cannot debug their own work without re-prompting the agent
- The junior's PR descriptions are short and vague; their commit messages are agent-generated
- Junior in code review pushes back with "the agent thinks X" rather than "I think X because Y"

**Why it's catastrophic:**
- Engineering judgment is built on internalizing patterns. The junior who only ships agent output never builds the patterns themselves.
- When the agent is wrong, the junior cannot recognize it because they have no independent model of what the code should look like.
- In incidents, the junior cannot debug. Their first move is to re-prompt the agent, which often produces a confidently-wrong answer.

**Mitigations:**
- Pair-driving discipline ([`pair-driving-guide.md`](pair-driving-guide.md)) explicitly trains the junior to engage with what the agent produced, not just accept it.
- The mentor occasionally asks the junior to re-implement a small section of agent output by hand. Not as punishment; as exercise.
- Code reviews on the junior's PRs include the question "Did you engage with this code or just ship it?" If the junior can't explain a non-trivial choice, the PR goes back.
- The junior takes turns writing agent-free code — small functions, scripts, glue code — to keep the muscle.

## Anti-pattern 3 — Over-tickets, no depth

**The pattern:** The junior is shipping 3-4 T1 tickets per sprint by month 5. The team celebrates the velocity. The junior has no time to read code, contribute to harness, or do design work. By month 12, they're a fast T1 shipper who can't function on T2.

**How it manifests:**
- Junior's velocity is high; their depth is shallow
- Junior is uncomfortable with anything outside their narrow ticket pattern
- Junior cannot lead a design conversation, even on small scope
- Junior's harness contribution is zero or a single drive-by fix
- Junior plateaus at L3 with no clear path to L4

**Why it's catastrophic:**
- Engineering depth is built in the time *between* tickets. Squeezing out the between-time produces engineers who scale linearly but never grow.
- The junior who's been a fast T1 shipper for 18 months has not built the muscles needed for T2 or harness work. The promotion path is closed.
- The high velocity in year one masks the development gap; it surfaces in year two when the junior cannot grow.

**Mitigations:**
- Manager actively reduces the junior's ticket load by 40-50% during phase 1, despite pressure. This is the hardest part of the program.
- 4-8 hours per week is reserved for harness work in phase 3, on the calendar, defended.
- Promotion criteria include depth, not just velocity. The L3 → L4 line requires harness contribution, not just T1 throughput.
- The 1:1 cadence asks "what did you read this week" and "what design did you participate in" alongside "what did you ship."

## Anti-pattern 4 — The senior who won't let go

**The pattern:** The mentor is doing the junior's work. The junior writes a draft; the senior rewrites it. The junior opens a PR; the senior makes 30 commits on top of it. The junior gets credit for shipping; the actual learning has been outsourced.

**How it manifests:**
- The junior's PRs have substantial commits from the senior
- The junior's git history shows lots of "small fixes" from the senior just before merge
- The junior cannot ship without the senior's involvement, even at 12+ months
- The junior is reluctant to take ownership in incidents because "the senior knows it better"

**Why it's catastrophic:**
- The junior never builds independent capability.
- The senior burns out from doing two jobs.
- When the senior is on PTO, the junior cannot function.
- The junior is dependent on this specific senior; can't transfer to another team.

**Mitigations:**
- Senior responsibility is mentorship, not implementation. The senior reviews; they don't rewrite.
- 1:1 between manager and senior asks "are you doing the junior's work?" The senior often won't realize they are.
- Mentor rotation every 6 months prevents over-dependence on one senior.
- Manager occasionally spot-checks: ask the junior to walk through a recent PR and explain every line. If they can't explain large chunks, the senior was doing the work.

## Anti-pattern 5 — Mentor by appearance, not by practice

**The pattern:** The senior is "the mentor" but doesn't actually mentor. They're on call, they're leading another team, they're traveling. The junior has a name but no real support. The 1:1s happen 50% of the time and last 15 minutes.

**How it manifests:**
- 1:1s skipped or shortened repeatedly
- Mentor doesn't review the junior's reviews
- Pair-driving sessions don't happen on the cadence
- Junior cannot name what they learned from the mentor in the past month

**Why it's catastrophic:**
- The program looks active on paper but produces nothing.
- The junior fills the vacuum with whatever pattern is closest — often anti-pattern 1 or 2.
- By 12 months, the junior has the same skill level as month 0 plus 12 months of bad habits.

**Mitigations:**
- Mentor responsibility is on the senior's perf review, with specific deliverables (1:1s held, reviews of junior's reviews, pair-driving sessions, postmortem participation).
- If the senior's calendar can't accommodate the mentorship, they shouldn't be the mentor. Reassign.
- Backup mentor (the second senior in the 2:1 ratio) covers when the primary is unavailable.
- Manager 1:1 with the junior asks "is the mentorship working?" at least quarterly.

## Anti-pattern 6 — Junior as the AI tooling expert

**The pattern:** The junior arrived enthusiastic about AI tooling. The team treats them as the AI expert. They lead training sessions. They write the team's CLAUDE.md. By month 9, they've shipped lots of "AI tooling work" and very little engineering work.

**How it manifests:**
- Junior is the go-to person on every AI tooling question
- Junior leads training sessions for senior engineers (this is backwards)
- Junior's tickets are mostly "AI tooling" tickets, not feature/bug work
- Junior at 18 months has unusual breadth of AI tooling knowledge but cannot ship a T2 feature

**Why it's catastrophic:**
- AI tooling expertise without underlying engineering depth is fragile. The tooling will change; the engineering judgment is durable.
- The junior has not built the engineering pattern library that makes AI tooling actually useful.
- The role becomes a trap: the junior is "the AI person" and cannot transition out.

**Mitigations:**
- The junior is not the team's AI expert. The team's AI expertise is distributed among seniors.
- The junior contributes to harness work in phase 3 (aged 9-15) but does not lead the team's AI tooling strategy.
- The junior writes a SKILL.md, not the team's overall CLAUDE.md philosophy.
- Manager redirects "AI tooling" tickets to seniors; gives the junior real engineering work.

## Anti-pattern 7 — The "high-performer" trap

**The pattern:** The junior is exceptional. They picked up the codebase fast; they ship clean code; reviews are strong. The team starts treating them like a senior. They're given senior responsibilities (incident command, design ownership, mentor for a future junior) before they're ready.

**How it manifests:**
- Junior is given responsibilities matching L4 or L5 by month 12
- Junior is praised heavily in public forums
- Junior is given fewer formal supports (skipped 1:1s, no mentor pair-driving) because "they don't need it"
- Junior's depth in the underlying disciplines is shallower than the breadth suggests

**Why it's catastrophic:**
- The high-performer doesn't get the foundation that the curriculum is designed to build. They learn to skim, not to go deep.
- They burn out when the responsibilities exceed the foundation.
- They look senior on the outside and are vulnerable inside.
- The team is shocked when, in their first real architecture conversation, they can't hold their own.

**Mitigations:**
- Run the curriculum even on high-performers. Compress some phases (especially phase 1 if their review judgment is genuinely already there) but don't skip.
- Give early responsibilities incrementally. The high-performer who handles a small incident in month 6 with no problems can lead a small one in month 12; not month 8.
- Manager 1:1 explicitly checks: are the supports still happening? The high-performer's mentor is more likely to skip the pair-driving sessions; resist.
- Calibration at 12 months is the same rubric as for any junior. High-performers don't get a free pass.

## Anti-pattern 8 — Compensation gap

**The pattern:** The junior is paid the company's standard "junior" comp band, which is calibrated to 2022 market expectations. The market for engineers who can clear the 2026 junior bar (reads diffs critically, runs an agent session, contributes to harness) has moved. The junior leaves at month 14.

**How it manifests:**
- Junior receives competing offers at 30-40% above their current comp at month 12
- Junior signals frustration about comp in the 1:1
- Junior's friends in the same role at other companies are paid significantly more

**Why it's catastrophic:**
- The 18 months of investment walks out the door.
- The replacement junior starts the curriculum from month 0; you've lost the year.

**Mitigations:**
- Per Ch 42 §42.3: "Hire fewer juniors and pay them more." Comp at the floor is a false economy.
- Real comp review at month 6 and month 12. If the junior is on track, comp moves.
- The retention conversation (per `people/career-ladder/`) starts at month 9, not month 14 when the offer arrives.

## When you spot an anti-pattern

The 1:1 is the surfacing mechanism. If the manager runs the cadence and asks the right questions ([`manager-1on1-playbook.md`](manager-1on1-playbook.md)), most anti-patterns surface within 4-8 weeks.

The fix is rarely "tell the junior to stop." The fix is usually a structural change — reduce ticket load, change the mentor, defend harness time, recalibrate comp. The junior is responding to the incentives the team set up; change the incentives.

## Companion artifacts

- [`18-month-curriculum.md`](18-month-curriculum.md) — the program designed to prevent these patterns
- [`manager-1on1-playbook.md`](manager-1on1-playbook.md) — the cadence that surfaces them
- [`calibration-rubric.md`](calibration-rubric.md) — the assessment that catches them
- Ch 42 §42.3 — the source
