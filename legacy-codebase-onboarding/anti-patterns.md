# Brownfield-Specific Anti-Patterns

The patterns that destroy brownfield modernization programs. Most are extensions of pre-AI anti-patterns; AI tooling makes some of them faster and more catastrophic.

## Anti-pattern 1 — The rewrite instinct

**The pattern:** Engineer or tech lead inherits brownfield code. Reads it for a week. Concludes "this is bad; we should rewrite." Proposes a 6-month rewrite project with AI tooling as the accelerant.

**How it manifests:**
- The proposal has confident AI-tooling claims (e.g., "with Claude Code we can do this in 4 months")
- The proposal has limited engagement with the existing code's actual behavior
- The proposal has a "this will pay off" trajectory with no pre-mortem of what could go wrong
- The proposer hasn't characterized any of the modules yet

**Why it's catastrophic:**
- Per Ch 11 §11.4, large rewrites are almost always the wrong call
- AI tooling does not make rewrites cheaper in any meaningful way; it makes them faster to draft and equally slow to verify, debug, deploy, and stabilize
- The rewrite project crowds out feature work for 6-18 months while delivering negative business value
- At the end, the "new" system has the bugs of the old system that nobody knew were features, plus new bugs

**Mitigations:**
- Use [`characterize-rewrite-leave-alone-rubric.md`](characterize-rewrite-leave-alone-rubric.md) explicitly when the proposal lands. The rubric usually says "no."
- Require the rewrite-readiness check before any rewrite proposal goes to leadership.
- Default to "characterize and strangler-fig" until proven otherwise.
- Specifically require the proposer to write a pre-mortem: "if this rewrite fails, what will the failure look like?"

## Anti-pattern 2 — False coverage from AI-generated tests

**The pattern:** Engineer points AI agent at module without characterization. Agent writes "tests" that pass against current behavior. Coverage metrics improve. Tests are then trusted as a regression gate. Tests don't actually catch behavior changes because they were generated to pass against current code, not to describe expected behavior.

**How it manifests:**
- New tests appear in PR with no review of what they actually test
- The tests assert on internal call patterns rather than observable behavior (slop signature S1)
- Coverage numbers move up but mutation testing scores stay flat
- Real regressions ship despite "tests pass"

**Why it's catastrophic:**
- The team thinks they have a safety net; they don't
- AI agents start running at higher autonomy because "tests catch issues" — but the tests don't catch the issues
- The first regression that escapes is often severe because trust was placed in coverage, not in actual verification

**Mitigations:**
- Mutation testing in CI. Catches tests that don't actually test.
- Require that characterization tests be reviewed for what they assert, not just for whether they pass.
- The rule from Ch 22 §22.2 (S1): "Tests assert behavior, not internals" — explicit in the team's review checklist.
- Run deliberate-breakage exercises: insert a known bug; verify the tests catch it before promoting to MVH Level 2.

## Anti-pattern 3 — The comprehensive plan that never ships

**The pattern:** Tech lead spends 4-8 weeks producing a comprehensive modernization plan. The plan is detailed, well-researched, and addresses every module. The plan is presented to leadership. Leadership approves it. Then the team can't actually start because the plan's first 90 days requires resources or buy-in that doesn't exist. The plan sits.

**How it manifests:**
- The plan is 30+ pages
- The plan covers every module the team owns
- The plan has no "first thing to ship in 30 days" beyond planning artifacts
- After a quarter, leadership asks "where are we on the plan?" and the answer is "still planning"

**Why it's catastrophic:**
- The team's energy went into planning rather than shipping
- The plan ages out as the codebase changes
- Leadership credibility erodes because nothing visible has happened
- When the team finally tries to start, they realize the plan was based on assumptions that aren't accurate

**Mitigations:**
- The plan covers ONE service at a time, not the whole codebase
- The 30/60/90 plan in this folder is the maximum scope of an initial plan
- Ship something small (a module README, a verify command, a single characterization test) within Week 2 of the program
- Re-plan every 90 days based on what was actually learned

## Anti-pattern 4 — The tech lead who tries to do it all

**The pattern:** New tech lead inherits brownfield codebase. Becomes the primary engineer doing characterization, the primary owner of the harness, the primary author of CLAUDE.md, the primary reviewer of every brownfield PR. Burns out in 4-6 months.

**How it manifests:**
- Tech lead's calendar is dominated by brownfield work
- Other engineers on the team aren't doing brownfield work because "the tech lead has it"
- Documentation, harness, and characterization tests are all "going to be written when [tech lead] has time"
- Tech lead's morale degrades visibly over weeks

**Why it's catastrophic:**
- Brownfield work is too big for one person; it needs distribution
- When the tech lead burns out, the program stops
- Other engineers don't develop brownfield skills
- The institutional knowledge becomes one person; if they leave, the program restarts from zero

**Mitigations:**
- Per Ch 11 §11.6, name owners for each module — owners are the responsible party for that module, not the tech lead
- Distribute the harness work: each engineer contributes a skill, hook, or CLAUDE.md section
- Tech lead's role is orchestration and review, not execution; if execution is dominating their time, scope is too large
- Pair-driving with other engineers (per `junior-trajectory/pair-driving-guide.md`) so brownfield skills spread

## Anti-pattern 5 — Skipping the read-only AI phase

**The pattern:** Engineer is told to use AI agents on legacy code. Configures the agent with write access from day 1. Agent makes changes; some are wrong; some pass tests but break behavior. Engineer concludes "AI doesn't work on legacy code."

**How it manifests:**
- Agent is configured with full write access from the start
- The first wave of agent changes lands in PRs that have to be heavily revised
- Engineer reports "AI tools are unreliable on this codebase"
- Team starts limiting AI usage to greenfield only

**Why it's catastrophic:**
- The conclusion is wrong (AI works on legacy code IF the harness is in place)
- The team loses the productivity lever AI tooling could have provided
- The harness work that would have made AI tooling work doesn't get done because AI was tried and failed
- The team becomes culturally hostile to AI tooling — this lasts for years

**Mitigations:**
- Per Ch 11 §11.6 Principle 5: "Read-only AI for the legacy module first. Before letting an agent edit the legacy module, let it answer questions about it for two weeks."
- Configure agent permissions explicitly to read-only on legacy modules until characterization is in place
- The 30/60/90 plan in this folder allocates Days 8-14 specifically to read-only AI sessions
- When AI agents fail on legacy code, the question is "what's the harness gap?" not "is AI broken?"

## Anti-pattern 6 — Promoting modules to higher MVH levels prematurely

**The pattern:** Module reaches MVH Level 1 (mapped). Engineer is excited, wants to use AI agents at higher autonomy. Promotes the module to Level 2 or Level 3 before tests actually catch deliberate breakage. First regression escapes.

**How it manifests:**
- Module promotion happens based on time, not on demonstrated capability
- "Tests pass" is treated as sufficient; "tests catch" is not verified
- Module is operating at autonomy level higher than the harness supports
- Regressions ship; team blames the agent

**Why it's catastrophic:**
- The MVH levels exist to encode where the harness can support which level of autonomy. Premature promotion makes the levels meaningless.
- Once a regression has shipped, trust in the harness erodes; team falls back to manual review for everything; the harness becomes decorative.

**Mitigations:**
- MVH Level promotion requires demonstrated capability: tests catch deliberate breakage, owner can confidently review changes, 30 days of stable operation at the current level.
- Per `starter-kits/legacy-bridge/MVH_LEVELS.md`, the graduation criteria are explicit. Use them.
- Don't promote based on calendar or based on "we feel ready."
- When in doubt, stay at the lower level for another 30 days.

## Anti-pattern 7 — Hiding the brownfield work from leadership

**The pattern:** Engineer or tech lead correctly identifies that brownfield work is unglamorous, and concludes that leadership wouldn't appreciate it. Hides the work behind feature-delivery framing. When leadership notices that feature delivery has slowed, the conversation about why is harder than it would have been.

**How it manifests:**
- Status updates emphasize feature delivery; brownfield work is buried
- Brownfield deliverables (golden master tests, READMEs, harness components) don't appear in roadmap reviews
- Leadership is surprised when feature delivery slows; can't trace it to the brownfield investment
- The conversation about brownfield investment happens during a crisis, not during normal planning

**Why it's catastrophic:**
- Leadership not aligned on the work means the work gets cut when pressure rises
- The team's actual investments are hidden, which is bad for trust
- The credit for brownfield work doesn't accrue; engineers who do it are perceived as slow
- The cycle perpetuates: brownfield work continues to be hidden because it's unrewarded

**Mitigations:**
- Use [`first-conversation-with-leadership.md`](first-conversation-with-leadership.md) to align early
- Make brownfield deliverables explicit in roadmap reviews — "this quarter we'll bring Service X to MVH Level 2" is a valid roadmap item
- Communicate brownfield wins clearly. "Stripe webhook regression caught by golden master test before it shipped" is a story worth telling.
- Per `promotion-and-leveling-rubric/`, brownfield work appears in the leveling criteria; reward it visibly.

## Anti-pattern 8 — The "we'll document it later" trap

**The pattern:** Engineer characterizes a module. Tests work. Verify command runs. Engineer doesn't write the module README because "I'll do it next week." Next week, another module is in progress. The README never gets written. The institutional knowledge stays in the engineer's head.

**How it manifests:**
- Modules at MVH Level 2 with no README
- Knowledge about the module's behavior is in the heads of 1-2 engineers
- New engineers can't onboard to the module without those engineers
- AI agents working in the module hit avoidable confusion that a README would have prevented

**Why it's catastrophic:**
- The whole point of brownfield work is to convert tribal knowledge into recoverable artifacts
- Without the README, the characterization tests are necessary but not sufficient
- When the engineer leaves, the module regresses to MVH Level 0
- Future engineers (and agents) re-learn the same things

**Mitigations:**
- Per Ch 11 §11.6 Principle 6: "AI-assisted documentation as a side effect. As engineers work in legacy modules, capture the agent's questions and the answers in module-level READMEs."
- The MVH Level 2 graduation criterion explicitly includes "README exists at module level with: purpose, entry points, known gotchas." No README, no Level 2.
- Configure agent sessions to capture Q&A; commit the resulting documentation to the README.
- Reward the documentation work visibly; engineers who write good READMEs save the team weeks of confusion.

---

## When you spot an anti-pattern

The 30/60/90 plan in this folder includes weekly checkpoints; the 1:1 cadence in `junior-trajectory/manager-1on1-playbook.md` (adapted for brownfield context) is the surfacing mechanism.

The fix is rarely "tell the engineer to stop." The fix is structural:

- For the rewrite instinct: require the rubric and the rewrite-readiness check before any rewrite proposal advances
- For the comprehensive plan: cap the plan scope at one service; require shipping in week 2
- For the tech lead doing it all: distribute the work formally; named owners per module
- For premature promotion: enforce the MVH graduation criteria mechanically (not by calendar)

## What this catalog will NOT do

- Will not catch every anti-pattern. New ones emerge as AI tooling evolves. Add to this list as you find them on your team.
- Will not work in a culture that punishes engineers for naming the rewrite instinct. The discipline is upstream of the catalog.
- Will not work without leadership engagement. Some anti-patterns are leadership-driven; engineers can't unilaterally fix them.

## Companion artifacts

- [`30-60-90-day-plan.md`](30-60-90-day-plan.md) — the structure that prevents the patterns
- [`characterize-rewrite-leave-alone-rubric.md`](characterize-rewrite-leave-alone-rubric.md) — defends against anti-pattern 1
- [`first-conversation-with-leadership.md`](first-conversation-with-leadership.md) — defends against anti-pattern 7
- `junior-trajectory/anti-patterns.md` — adjacent catalog for junior development
- Ch 11 — source
