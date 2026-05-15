# 90-Day VP of Engineering Plan

**Companion to:** Chapter 51 of _Software Engineering with AI_ by Ryan Byrd.

**How to use:** Import this file into Notion (or your tool of choice), assign owners and dates, treat it as your live operating doc for the next 90 days. The checkboxes are real — check them as you go.

**Compress timeline at your own risk.** Section 51.10 lists what this plan sacrifices. Section 51.11 lists what you should refuse to compress. Read both before adapting dates.

---

## Day 0 — The day you decide to do this

- [ ] Write one-page strategy memo (posture, 90-day target, board commitment, what you will NOT do)
- [ ] Forward memo to CEO and CTO before close of business
- [ ] Identify named platform owner (yourself temporarily if needed)
- [ ] Identify pilot team (6-10 engineers; strongest senior bench, not most enthusiastic)
- [ ] Block your calendar for next 90 days — protect 30% for this work

**Owner:** VP Eng
**Deliverable:** Strategy memo sent
**Pass criterion:** CEO and CTO have replied (any reply, even "noted")

---

## Week 1 — Foundation

- [ ] Stand up cost gateway (LiteLLM, Bifrost, or hand-rolled). 80% coverage is enough.
- [ ] Pull existing AI tooling spend across all vendors. Map to specific developers.
- [ ] Document shadow AI you discover (don't punish disclosure)
- [ ] Write the approved tooling matrix (Chapter 30). One page, 3-5 tools max.
- [ ] CISO countersign on tooling matrix
- [ ] Schedule all-hands talk for end of Week 2
- [ ] Draft all-hands talking points (posture, scope, what's NOT happening)

**Owner:** Platform Eng + VP Eng
**Deliverable:** Cost dashboard live, tooling matrix signed
**Pass criterion:** You can show the CFO per-developer spend on demand

---

## Week 2 — Pilot stand-up

- [ ] Pilot team reads CLAUDE.md/AGENTS.md from book appendices
- [ ] Pilot team runs them against their repo, identifies gaps
- [ ] Ship working `verify` command for pilot team's repo (THIS IS THE WEEK 2 PRIORITY)
- [ ] Write first hooks: bash-firewall, protected-paths
- [ ] Run all-hands talk
- [ ] Post all-hands FAQ in shared doc (the questions you didn't get to)

**Owner:** Pilot team lead + Platform Eng
**Deliverable:** Working verify command in pilot repo
**Pass criterion:** Pilot team can run `npm run verify` (or equivalent) and it actually verifies something

---

## Weeks 3-4 — Pilot in motion

- [ ] Pilot team starts shipping work through harness
- [ ] Track failed-one-shot ratios from day one (shared spreadsheet is fine)
- [ ] Begin code-review pairing for any junior on pilot team (2 hours/week per junior)
- [ ] Run AI-readiness scorecard (`scripts/ai-readiness-audit.py`) against pilot repo
- [ ] Publish the score (act of measuring matters more than the number)
- [ ] Cost dashboard shows per-developer median, weekly trend
- [ ] Friday triage: 5-min Score/Question/Opportunity/Train classification on weekly failures

**Owner:** Pilot team
**Deliverable:** First three weeks of pilot data
**Pass criterion:** You can answer "is the pilot working?" with data

---

## Day 30 — First decision point

- [ ] Pilot team produces first internal write-up (what worked, what broke, what's missing)
- [ ] Triage decision: GO (add second team) / HOLD (buy another 4-6 weeks)
- [ ] If HOLD: communicate why; do NOT roll out. Recovery from bad rollout is 6 months.
- [ ] If GO: identify second team, start their onboarding
- [ ] Brief CEO/CTO with honest numbers and next-30-day plan

**Owner:** VP Eng
**Deliverable:** Day 30 review document
**Pass criterion:** Decision made and communicated; no team is added if metrics don't support it

---

## Days 31-60 — Harness investment

- [ ] Build out standard skill library (Chapter 13). Pilot team's failures are the spec.
- [ ] Onboard second team (2-week onboarding per Chapter 44)
- [ ] Vendor terms review: re-read every AI vendor contract
- [ ] Document vendor-terms gaps (training opt-out, BAA status, etc.)
- [ ] Write canonical answer to "do you use AI in code generation?" (see `security-questionnaire-answers.md`)
- [ ] If sales has already asked: send the answers proactively to the affected accounts

**Owner:** Platform Eng + VP Eng
**Deliverable:** 8-12 skills committed; 2 teams operational
**Pass criterion:** Second team's metrics are tracking similar to pilot team's

---

## Day 60 — Honesty checkpoint

- [ ] 60-day review with CTO. Honest numbers.
- [ ] Identify what's tracking, what's lagging
- [ ] If lagging: adjust board commitment NOW (not at Day 90)
- [ ] Re-forecast spend for remainder of quarter
- [ ] Update CFO if forecast has shifted

**Owner:** VP Eng + CTO
**Deliverable:** Honest 60-day report
**Pass criterion:** No surprises at Day 90

---

## Days 61-90 — Controlled expansion

- [ ] Add teams 3 and 4 (pace-limited by platform capacity)
- [ ] Run first prompt-injection exercise (Chapter 37)
- [ ] Document findings; update hooks if needed
- [ ] Prepare board materials: metrics dashboard, cost dashboard, failed-one-shot triage, incident log
- [ ] Schedule board prep meeting with CTO/CEO 1 week before board

**Owner:** VP Eng + Platform Eng
**Deliverable:** Board deck (4 slides)
**Pass criterion:** Board materials reviewed and approved by CEO before the meeting

---

## Day 90 — Board

- [ ] Deliver four-slide deck (see `board-deck-template.pptx`)
- [ ] Communicate next-90-day plan
- [ ] Get commitment for next quarter (investment level, headcount, expected outcomes)
- [ ] Send post-board summary to engineering team within 48 hours

**Owner:** VP Eng
**Deliverable:** Board commitment for next quarter
**Pass criterion:** You walk out with: (1) approved budget, (2) approved next-quarter targets, (3) no surprises

---

## OKRs for the quarter

**Quarterly objective:** Establish baseline AI-native engineering capability without compromising delivery quality.

| KR | Metric | Target | Source | Status |
|---|---|---|---|---|
| KR1 | Deployment frequency | At or above quarterly baseline | DORA | |
| KR2 | Median lead time, tier-2 tickets | -8% to -12% from baseline | DORA | |
| KR3 | Change failure rate | At or below baseline | DORA | |
| KR4 | MTTR | At or below baseline | DORA | |
| KR5 | Failed-one-shot ratio (pilot team) | Downward trend by Day 60 | Internal | |
| KR6 | Slop incidence | <10% of merged PRs | PR tags | |
| KR7 | Mutation score (pilot modules) | ≥70% (or baseline if higher) | Mutation tester | |
| KR8 | Per-dev token spend (median) | Within budget | Cost gateway | |
| KR9 | Pilot team adoption | 100% on approved tooling | Tooling matrix | |
| KR10 | CISO countersign on tooling matrix | By Day 7 | Document | |

---

## What this plan sacrifices (and is OK with)

- Local LLM deployments — defer to year 2
- Bespoke internal MCP servers — use community ones
- Multi-team consensus on conventions — pilot's conventions become template
- L3+ autonomy — earn it later
- Bespoke metrics dashboards — use cost gateway + standard observability
- Internal certification program — informal use of autonomy levels for now

## What you should refuse to compress

- The harness investment in first 30 days
- The security review (vendor terms, CISO countersign)
- The all-hands talk
- The Day 30 honesty checkpoint
- Saying NO at Day 30 if the pilot isn't ready

---

## Reading this plan in three minutes (the elevator version)

If you only have time for the bullets:

1. **Day 0:** Memo, owner, pilot team, calendar.
2. **Week 1:** Cost gateway, tooling matrix, all-hands scheduled.
3. **Week 2:** Verify command. All-hands talk.
4. **Weeks 3-4:** Pilot ships, metrics tracked.
5. **Day 30:** Honest decision: go or hold.
6. **Days 31-60:** Build out harness, onboard second team, vendor review.
7. **Day 60:** Renegotiate commitment if data demands it.
8. **Days 61-90:** Add teams 3-4, prep board.
9. **Day 90:** Board, next-quarter plan.

---

*Last updated: [DATE]. Check this back into your team's project tool and update as you go. The plan is a living document, not a one-time deliverable.*
