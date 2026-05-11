# Week 1 Curriculum — Day by Day

The structured first week. Per Ch 44 §44.1, the goal is: by end of week, the engineer can ship a small change with senior review and has met the team's review discipline, security stance, and harness expectations.

## Day 1 — Tools and reading

The day most new hires waste because nobody planned for it.

### Goal

By end of day: tools are working; key documents have been read; the engineer knows where things are.

### Specific tasks

#### Morning

1. **Tool installation and access** (90 min)
   - Claude Code installed and configured with team license
   - IDE plugins installed (whatever the team uses — Cursor extension, Continue.dev, etc.)
   - SSO and access to team's private repos
   - Gateway access if the team uses an LLM gateway
   - Read access to team's monitoring tools, even if not deeply
   - Email / Slack / wiki accounts working

2. **Confirm verify command works** (30 min)
   - Pull the team's main repo
   - Run `make verify` (or whatever the verify command is)
   - Confirm it passes on a clean checkout
   - If it doesn't, that's a finding — the buddy investigates with the engineer

#### Afternoon

3. **Required reading — first pass** (3 hours)
   - The company's CLAUDE.md
   - The team's AGENTS.md (if separate)
   - The Approved Tooling Matrix (per `vendor-procurement-runbook/data-classification-walkthrough.md`)
   - The Do-Not-Automate catalog (`do-not-automate-catalog/`)
   - The autonomy ladder (`agent-autonomy-levels/autonomy-ladder.md`)
   - The team's published autonomy ladder for the specific work categories

4. **First-day check-in with manager** (30 min)
   - Manager confirms the engineer is set up
   - Manager surfaces any expectations specific to this engineer (specific work area, specific learning goals)
   - Manager schedules the rest of week 1's pair-driving slots

### What NOT to do on day 1

- Don't open any PRs
- Don't start any substantive work
- Don't propose changes to anything based on first-day reading
- Don't worry if the reading isn't fully internalized — week 1 is a first pass

### Pass criterion for day 1

By end of day:
- All tools working
- Verify command runs successfully
- Engineer can name the team's autonomy level for at least 3 work categories
- Engineer has read the do-not-automate catalog and can identify Tier 1 vs Tier 3 work

---

## Day 2 — Walk the harness

The day that distinguishes AI-native onboarding from generic onboarding.

### Goal

By end of day: the engineer has run a skill end-to-end; understands the subagent roster; has seen at least one hook fire; can navigate `.claude/` confidently.

### Specific tasks

#### Morning — pair-driving session 1 (2-3 hours)

The buddy walks the engineer through the team's harness. Specifically:

1. **The skill library** (60 min)
   - Tour `.claude/skills/` (or wherever skills live)
   - Walk through 3-5 of the most-used skills
   - For each: when do we invoke it, what's it good for, what are the gotchas
   - Pick one skill; engineer invokes it on a sandbox repo end-to-end

2. **The subagent roster** (30 min)
   - Tour `.claude/subagents/` (or wherever subagents live)
   - Walk through the team's standard subagents (planner, implementer, reviewer at minimum)
   - For each: when does it run, what does it produce, how do we interpret its output

3. **The hook library** (30 min)
   - Tour `.claude/hooks/` and CI hooks
   - Walk through the bash firewall, slop-detector, any team-specific hooks
   - Show one hook firing on a deliberate test (e.g., engineer attempts a force-push; hook blocks)

4. **The verify command** (15 min, follow-up from day 1)
   - Walk through what `make verify` actually runs (lint, typecheck, tests)
   - Show what each component catches

#### Afternoon — sandbox session (2 hours)

5. **Engineer runs a skill end-to-end** on a sandbox repo
   - The buddy provides the sandbox or directs the engineer to one
   - Specific task: take a small refactor or doc-update task; run the relevant skill; produce a draft PR
   - The output isn't shipped (it's sandbox); the point is exercising the workflow

6. **Engineer asks questions** about anything that surprised them
   - The harness has invariants the codebase alone won't reveal
   - This Q&A surfaces tribal knowledge

### Pass criterion for day 2

By end of day:
- Engineer has invoked at least one skill
- Engineer has seen at least one subagent run and read its output
- Engineer has seen at least one hook fire
- Engineer can name 3 of the team's most-used skills

---

## Day 3 — Write an agent-ready issue

The day the engineer practices spec clarity.

### Goal

By end of day: the engineer has written and gotten reviewed at least one agent-ready issue from the team's real backlog.

### Specific tasks

#### Morning

1. **Read the team's agent-ready issue template** (30 min)
   - Per the team's PR template / issue template
   - Per the patterns from Ch 19 (if accessible) — "what makes an issue agent-ready"

2. **Pick a real backlog ticket** (30 min)
   - Buddy directs the engineer to a Tier-3 (low-stakes) ticket from the actual backlog
   - The ticket exists; nobody's started it; it's real work

3. **Write the agent-ready version** (90 min)
   - Take the existing ticket; rewrite it as an agent-ready issue
   - Cover: context, scope, acceptance criteria, non-goals, relevant files, test approach
   - Per Ch 19 patterns

#### Afternoon

4. **Review session with buddy** (45 min)
   - Buddy reads the agent-ready issue
   - Substantive feedback: what's clear, what's vague, what's missing
   - Engineer iterates

5. **Second pass + review** (45 min)
   - Engineer revises based on feedback
   - Second review confirms quality

6. **Optional: invoke the agent on the issue in sandbox** (60 min)
   - Run the issue through the team's normal agent workflow in a sandbox
   - Observe what the agent does with the spec
   - Note any places the spec needed to be clearer

### Pass criterion for day 3

By end of day:
- Engineer has produced at least one agent-ready issue that the buddy considers shippable as a spec
- Engineer can articulate what made the spec good (and what made earlier versions worse)

---

## Day 4 — Ship a Tier-3 PR

The day the engineer's first real work goes through the team's normal workflow.

### Goal

By end of day: the engineer has opened a PR, run the team's review process, and (ideally) had the PR merged.

### Specific tasks

#### Morning — plan and implement (3 hours)

1. **Pick or use yesterday's agent-ready issue**
   - Continue from day 3's issue, or pick another Tier-3 backlog item

2. **Run the plan/implement/review loop** (per Ch 20 if accessible)
   - Plan: what the change is, what files are affected, what tests are needed
   - Implement: with AI assistance at L1 (suggest only, engineer approves each edit)
   - Engineer runs verify locally; confirms passing
   - Engineer opens a draft PR

#### Afternoon — review

3. **PR review with buddy** (60 min)
   - Buddy reviews the PR substantively
   - Walks through the seven slop signatures (per Ch 22 §22.2) live, looking for them in the engineer's diff
   - Specific feedback on:
     - Scope discipline (is the diff bounded by the issue?)
     - Test discipline (are tests substantive or mock-heavy?)
     - Style consistency (does it match team conventions?)

4. **Address feedback; re-review** (60 min)
   - Engineer addresses the feedback
   - Buddy re-reviews

5. **Merge if ready** (15 min)
   - If the PR is ready, merge it
   - If not, identify what's needed; queue for tomorrow if possible

### Pass criterion for day 4

By end of day:
- A PR has been opened (merged or near-merged)
- The engineer has demonstrated the team's review discipline
- The engineer has identified at least one slop signature in their own work (caught by the buddy or by themselves)

If merge didn't happen on day 4, that's fine — happens often. Day 4 is "first PR open," not necessarily "first merge."

---

## Day 5 — Prompt-injection exercises

The security-discipline day.

### Goal

By end of day: the engineer has run all six prompt-injection exercises (per `prompt-injection-test-suite/`) and discussed findings with the team's security lead.

### Specific tasks

#### Morning — exercises (3-4 hours)

1. **The six exercises** (per `prompt-injection-test-suite/test-cases/`)
   - Test 1: poisoned issue body
   - Test 2: malicious PR comment
   - Test 3: poisoned web page
   - Test 4: poisoned log line
   - Test 5: cross-repo exfil attempt
   - Test 6: credential-in-output

   Engineer runs each in a sandbox, observes the outcome, records pass/fail.

#### Afternoon — discussion with security lead (60-90 min)

2. **Discussion** with the team's security lead
   - Walk through findings from the six exercises
   - Discuss what passed, what failed, what was surprising
   - Connect to the team's broader security discipline
   - Surface the engineer's questions about agent security

3. **Reflection** (30 min)
   - Engineer reflects on the week
   - Buddy and engineer discuss: what's clicking? What's still confusing?
   - Plan for week 2

### Pass criterion for day 5

By end of day:
- All six prompt-injection exercises run; results recorded
- Discussion with security lead complete
- Engineer can articulate the threat model and the defensive layers

### What this day requires

- Security lead's time (90 min in the afternoon) — schedule in advance
- Sandbox environment for the exercises — typically a test repo or test workspace

If the security lead's time isn't available on day 5, the discussion can slip to early week 2; the exercises themselves should still happen on day 5.

---

## End of week 1 — overall pass criterion

The engineer:
- Has all tools working
- Has read and can navigate the foundational documents
- Has invoked skills, subagents, and hooks
- Has written an agent-ready issue
- Has shipped (or near-shipped) a Tier-3 PR
- Has run the prompt-injection exercises
- Has met with the team's security lead
- Knows what L1 certification requires and has a path to it

This is the foundation. Days 8-30 turn it into sustained productivity ([`days-8-to-30.md`](days-8-to-30.md)).

## What can go wrong in week 1

### "Day 1 reading takes too long"

Some engineers want to internalize everything before moving on. Day 1 is a first pass; depth comes through use.

Mitigation: buddy explicitly says "this is a first pass; we'll deepen as you use the harness."

### "Tool setup is broken"

Common, especially in less-mature platforms. The engineer's day 1 spent debugging tools rather than reading.

Mitigation: platform team owns onboarding-experience reliability. Treat tool setup friction as a P2 incident in the platform team's queue.

### "Buddy is over-committed"

The buddy was assigned but is in heavy other work. Pair-driving sessions get rescheduled.

Mitigation: buddy duties are explicit time commitment, not "I'll fit it in." Per `platform-team-charter/`'s discipline of named ownership.

### "Engineer pushes for more autonomy"

Some engineers (especially senior hires) want to ship at L2 or L3 in week 1. The discipline says no.

Mitigation: certification gates are real (per `agent-autonomy-levels/certification-gates.md`). L2+ requires earned discipline, not just experience.

### "Day 4 PR isn't ready by end of day"

Common. Don't push to merge unfit code.

Mitigation: it's fine if day 4 ends with a draft PR; week 2 finishes it.

## Companion artifacts

- [`days-8-to-30.md`](days-8-to-30.md) — what comes next
- [`reading-list.md`](reading-list.md) — the reading curriculum
- [`pair-driving-milestones.md`](pair-driving-milestones.md) — pair-driving structure
- [`l1-certification-checklist.md`](l1-certification-checklist.md) — the day-30 gate
- [`buddy-and-manager-roles.md`](buddy-and-manager-roles.md) — who does what
- Ch 44 §44.1 — source
