# Team Conversation Scripts

Verbatim openers for the conversations referenced in the playbooks. Adapt to your voice; the structure and the order of points are what matter.

---

## §1 — Pushing back on a compressed migration timeline

When leadership has decided on a timeline that the playbooks (and your judgment) say is too short.

### Context

The CEO or CFO has issued a directive. Compressed timeline. You believe the playbook timeline (6-9 months) is correct. You need to push back without being insubordinate or hyperbolic.

### Opener (verbatim)

*"I want to share what I'm seeing on the migration timeline. I'm hearing [X] weeks. Based on the data we have from comparable migrations and what I've seen at [previous company / industry], here's my concern.*

*The compressed timeline tends to fail in a specific way: the team's productivity drops 15-20% during the compressed period; the senior engineers who liked the existing tool become the loudest critics of the new one; the platform team spends three months on tooling instead of harness investment. By month 4 the metrics look worse than baseline, which leads to 'AI doesn't work for us' and we lose the program.*

*The pattern that does work is parallel use for one to two quarters, let the team self-select, converge over six to nine months. The total cost — including the dual licensing — is less than the productivity dip from the compressed timeline.*

*Here's what I'm proposing instead: [your specific timeline, with milestones]. The trade-off is [specific cost — extra licensing, slower headcount efficiency gain, etc.]. I'd like to walk through the math with you."*

### Why this works

- Names the failure mode specifically rather than asking for "more time"
- Quantifies the cost of compression (productivity drop, departure risk)
- Quantifies the cost of the proposed alternative
- Reframes from "engineering is being slow" to "engineering is showing the math"

### What to bring to the conversation

- War story 004 from this companion repo, with specifics
- The pre-migration checklist with current scores
- Per-team productivity baseline (from your six-metric dashboard)
- Specific names of senior engineers at retention risk if compression proceeds

### What to NOT do

- Do not threaten to quit. The conversation has nowhere to go after.
- Do not say "the book says we should." Cite the data, not the book.
- Do not promise a specific outcome you can't guarantee. *"I think we can get to 60% adoption in 6 months"* not *"we will hit 60% in 6 months."*

---

## §2 — Generic migration announcement

The all-hands or written communication announcing any tool migration.

### Opener (verbatim)

*"I want to share where we are on AI tooling. Two things to know.*

*First — context. [Existing tool] has been useful and we're not replacing it lightly. The work folks have invested — the [.cursorrules / Copilot configuration / personal patterns] you've built — is real and not wasted. The patterns translate.*

*Second — what we're doing. We're [adding / migrating to] [new tool] for [specific reason]. The timeline is [N months of parallel use, then convergence decision]. During this period, you can use whichever tool fits the task. After [N months], we'll review what's working and decide together.*

*Three things you can do this week if you want to engage:*
*1. Read [migration champion]'s onboarding doc.*
*2. Try the new tool on one task you'd normally do in [old tool]. Tell us how it went.*
*3. If you have concerns about the timeline, the new tool, or anything else, message me directly.*

*The platform team is owning the harness work; [migration champion] is the senior engineer leading the rollout. Questions?"*

### Why this works

- Acknowledges the existing tool's value before introducing the new one
- Names a specific timeline (engineers calibrate around vague timelines badly)
- Frames choice (use whichever fits) rather than mandate
- Invites direct concerns without making the announcement a debate forum
- Names specific people responsible

---

## §3 — Cursor → Claude Code specific

Use the §2 opener with these specifics:

- Existing tool: Cursor
- New tool: Claude Code
- Reason: *"Claude Code's strengths are agentic work — multi-step tasks, planning loops, GitHub Action integration. Cursor's strengths are inline editing and tab completion. We expect most senior engineers will end up using both: Cursor for inner-loop, Claude Code for outer-loop."*
- Timeline: *"Two quarters of parallel use, then we make a consolidation decision based on actual usage."*
- The "what's not changing": *"Cursor stays. Even if we converge on Claude Code as primary, Cursor stays available for inner-loop work. We're not asking anyone to give up Cursor on a deadline."*

---

## §4 — Copilot + Claude Code (additive)

Different framing because nothing is being replaced.

### Opener

*"We're adding Claude Code to the stack alongside Copilot. Copilot is staying — there's no migration here. Different tools for different work.*

*Where Copilot keeps doing what it's been doing: inline completions, PR summaries, repository-level analysis.*

*What Claude Code is being added for: agentic workflows, multi-step changes, the planner / implementer / reviewer pattern, GitHub Action integration.*

*Initial rollout: [senior tier — name the criteria]. After two quarters we'll review and decide whether to expand to broader rollout, hold the line, or sunset the addition.*

*Cost: shared transparently. We're adding $[N] in licensing for [M] seats; that lands the AI tooling line at $[total]. The CFO has been briefed and we have explicit budget for two quarters of evaluation.*

*Questions about the criteria for the senior tier? Talk to your manager. Questions about the tool itself? [Migration champion] is running early adopter onboarding."*

### What to add for sensitive contexts

If your company is cost-pressured: *"We are not requesting additional headcount or new initiatives during this evaluation period. The expected ROI of the new tool is [specific metric] in [N quarters]; if we don't hit it, we cancel."*

---

## §5 — Shadow AI cleanup announcement

The all-hands message that opens the discovery phase. The amnesty framing is critical.

### Opener (verbatim)

*"I want to address AI tooling governance directly. Two things.*

*First, where we are: we know that some folks have been using AI tools — ChatGPT, Claude.ai, Replit Agents, others — that aren't on our approved tooling matrix. This is normal in 2026; it has happened at most companies our size. It happened because the tools are useful and our governance hadn't kept pace. That's on us as a leadership team, not on individuals who tried to do their work effectively.*

*Second, where we're going: we're formalizing AI tooling governance over the next two months. To do that, we need to know what's actually being used. Here's the deal:*

*1. We are running a self-disclosure period for the next four weeks. Tell us what you've been using on company work. There is no penalty for disclosure during this period — that is a leadership commitment we will honor.*
*2. After the self-disclosure period, we'll categorize each tool: approve and procure, approve with restrictions, replace with something equivalent we already have, or block. We'll communicate the decision per tool, with reasoning.*
*3. After the decisions, we'll provide migration support for any tool that's being replaced. You will not be left to do the migration alone.*
*4. Personal time, personal projects: out of scope. We're cleaning up usage on company code.*

*The form for self-disclosure is [link]. Anonymous if you want; we'll de-anonymize only at the aggregate level for tool-categorization decisions.*

*Questions, concerns, or context I should know about? Direct message me. The intent here is governance, not enforcement theater."*

### Why this works

- Acknowledges the leadership failure (governance hadn't kept pace) before asking for individual disclosure
- Specific timeline (four weeks)
- Specific commitment (no penalty for disclosure)
- Specific scope (company code, not personal time)
- Specific follow-through (migration support, not just policy)
- Invites direct contact for nuanced situations

### What to NOT do

- Do not include any "we already know who's been using what" language. Even if true, it kills the amnesty.
- Do not list specific tools by name as "the ones we're worried about." Lists trigger defensiveness.
- Do not say "we are launching a security review." That language activates the wrong frame.

---

## §6 — Holding the line on the timeline mid-migration

When pressure builds at month 4 to compress the remaining timeline.

### Context

The migration is in Phase 2. Some metric (productivity, adoption, sentiment) is wobbly. Leadership is asking *"can we accelerate?"* Your judgment is to hold the line.

### Opener

*"I want to address the question of accelerating the timeline. I understand the pressure: [specific metric] is [direction]. I share the impatience.*

*Here's why I'm recommending we hold the line. The migrations that succeed run their full timeline because the work in months 4-7 is what makes month 8's consolidation succeed. If we compress now, we save 4-6 weeks; if we mishandle the consolidation, we lose 6-12 months recovering. The asymmetry is severe.*

*What I'm proposing instead: [specific intervention to address the wobbly metric without changing the overall timeline]. We'll see whether [metric] responds in [specific timeframe]. If it doesn't, we have a different conversation."*

### Why this works

- Acknowledges the underlying concern instead of dismissing
- Names the asymmetry between compression risk and current cost
- Offers a specific alternative intervention
- Reserves the option to revisit if the alternative fails

---

## §7 — Senior engineer at risk during migration

When a specific senior engineer has signaled they may leave over the migration.

### Context

A senior engineer has either explicitly said they're considering leaving, or has been visibly disengaged from migration work, or is your highest-flight-risk engineer per the retention list. The conversation is direct, in-person if possible, focused on hearing first.

### Opener

*"I wanted to make sure we talk one-on-one about the migration. I know it's been a lot — the [existing tool] you've built up matters, and the new tool isn't a perfect substitute for everything. I want to hear from you specifically about what's been working, what's been frustrating, and what would change the experience for you.*

*Before you answer — I'm not here to talk you into the migration. I'm here to figure out what we need to change about the approach so this works for you. If we need to slow down for you specifically, that's a real option. If we need different harness investment, that's a real option. If you'd rather stay on [existing tool] longer, that's also a real option.*

*What's the most frustrating part of this for you right now?"*

### Why this works

- Acknowledges investment in the existing tool explicitly
- Frames as listening, not selling
- Lists specific options that show the conversation is real (slow down, different investment, stay on existing tool)
- Opens with a specific question rather than a vague *"how are you?"*

### What to NOT do

- Do not lead with retention pitch. The retention play (comp, credit, mobility) comes after listening, not before.
- Do not ask *"are you happy?"* Generic. Engineers don't answer generic questions in this conversation honestly.
- Do not make commitments you can't keep. Better to say *"I'd want to see if we can do that"* than to overcommit and back out.

### After the conversation

- Document what was said (in your own private notes, not in HR systems unless it escalates)
- Make the specific changes you committed to within 1-2 weeks
- Follow up: *"You mentioned [specific concern]. Here's what we changed: [specific change]. How is it landing?"*
- If the engineer leaves anyway, the conversation was still right; you reduced the harm and learned for next time

---

## §8 — Conversation with the CFO mid-cleanup

When the dual licensing during a migration has produced a sticker-shock conversation.

### Context

Month 3-4 of a parallel-use period. The CFO sees a bigger AI tooling line item than they remembered approving. Conversation is needed.

### Opener

*"I want to walk you through the AI tooling line item before there's any surprise. The number is [specific dollar amount]; it's running [N]% above last quarter's pre-migration baseline. Here's why and here's the timeline.*

*The dual licensing is for [N more months] per the migration plan we agreed on at [date]. After that, we sunset [tool A] or [tool B] depending on the consolidation decision in month [N]. The expected steady-state line item after consolidation is [specific number] — that's [lower / same / higher] than the pre-migration baseline.*

*The risk if we cut the dual licensing now: the migration becomes a forced consolidation, productivity drops 15-20%, and we likely lose 2-3 senior engineers over the next two quarters. The cost of replacing those engineers — recruiting, ramp time, lost continuity — is roughly $[number]. So the dual licensing is much cheaper than the alternative.*

*What I want to make sure you have is the dashboard. Per-team spend, per-engineer cost, productivity correlation. Update monthly. Want to walk through it?"*

### Why this works

- Surfaces the number before the CFO does
- Specific timeline back to baseline
- Quantifies the cost of the alternative (forced consolidation)
- Offers the dashboard as the durable solution
- Reframes from "explain the spend" to "let's review the dashboard together"

### What to NOT do

- Do not minimize ("it's just a few thousand dollars")
- Do not be defensive
- Do not promise the spend will go down faster than your data supports
- Do not surface this conversation only when forced; proactive is much better received

---

## When NOT to use these scripts

These scripts work for the most common scenarios. They will not work in:

- A toxic culture where leadership is explicitly hostile to engineering judgment. The script's framing assumes good-faith debate; in toxic cultures, no script saves you.
- A regulatory or legal-driven cleanup. Lawyers should write that language, not engineering managers.
- An incident-driven conversation. Different domain; use your incident response practice.
- A conversation about an individual's performance. Different domain; use your performance management practice.

If your situation doesn't match the scripts, write your own with the same disciplines: acknowledge first, name specifics, offer concrete alternatives, invite direct contact.
