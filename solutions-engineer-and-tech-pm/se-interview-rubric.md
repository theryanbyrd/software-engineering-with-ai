# Solutions Engineer Interview Rubric

The interview structure for an SE hire calibrated to Ch 42 §42.5's framing. Tests whether the candidate can do the work — write code in customer environments, design agent-ready specs, hold a system-design conversation with AI tooling in the room — not whether they can talk about it.

This rubric is the SE-specific counterpart to `people/interview-rubrics/architecture-with-ai.md`. Where there's overlap, this document is the SE-specific instance and the engineering rubric is the general one.

## The five rounds

| Round | Format | Duration | What we're testing |
|---|---|---|---|
| 1. Hiring manager screen | Conversation | 45 min | Background fit; engineering history is real |
| 2. Customer-environment coding | Async exercise | ~3 hours | Can drop into unfamiliar codebase and ship |
| 3. Spec workshop simulation | Live with engineer | 60 min | Can produce an agent-ready spec from discovery |
| 4. Architecture-with-AI conversation | Live | 60 min | Can hold senior-level system-design conversation |
| 5. Reference and final fit | Live with team | 60 min | Will the partnership work |

Total candidate load: ~6 hours of substantive interviewing.

We do not run a separate behavioral round. We do not run a "case study" round. We do not run more than this. Process longer than ~6 hours produces no incremental signal and loses good candidates to companies that respect their time.

---

## Round 1 — Hiring manager screen

The first conversation. Not a deep dive; a calibration that the candidate can clear the basic technical bar to make the rest of the process worth running.

### What you're testing

- Engineering background is real. They've shipped production code; they have specific stories.
- AI tooling fluency is real. They can describe what they actually do with AI tools day-to-day.
- They understand what an SE role is — not a sales role, not a support role.
- Communication is good. The conversation doesn't leak energy.

### Sample questions

- "Walk me through the most technically interesting customer engagement you've had in the past year. What did you build, what was the outcome?"
- "What does your AI-tooling workflow look like when you're working in a customer's codebase you've never seen before?"
- "Tell me about a time you pushed back on what a customer said they needed."
- "What would you say is your strongest engineering skill, and what's something you'd want to grow on?"

### Calibration

- **Strong (move forward):** specific stories, real engineering substance, calibrated about strengths and gaps
- **Weak (decline):** vague stories, "I worked closely with engineers" without specifics, no real engineering depth, AI tooling described as "I use ChatGPT sometimes"

---

## Round 2 — Customer-environment coding exercise

The most differentiating round. Tests whether the candidate can do the actual work.

### Setup

We give the candidate three things:

1. A **sanitized customer-like codebase**. We use a stripped-down public reference repo with our SDK pre-installed. Not our codebase; a stand-in that's representative of customer environments.
2. A **discovery summary**. ~1 page. The customer wants X integration, here's what their stack is, here's what they've already built, here's what their constraints are.
3. A **time budget**. We say "spend up to 3 hours; we expect 2." Be honest about budget; candidates who go over should not be penalized but should note it.

The candidate works async. They submit:
- A working integration (or partial integration with explicit blockers documented)
- A short write-up (~500 words) of what they built and why
- The git history of how they got there (we look at the commits, not just the result)

### What we're testing

- Can they orient in an unfamiliar codebase?
- Do they ask the right questions before coding?
- Does their code fit the conventions of the codebase they're in?
- Do they use AI tooling productively in this environment, or do they freeze?
- Is the write-up something a customer's engineering team would respect?

### Rubric — score each item 0-3 (0=absent, 1=weak, 2=adequate, 3=strong)

- [ ] **Codebase orientation:** Did they read existing code before writing new code?
- [ ] **Question quality:** Did they identify ambiguities in the discovery summary and either resolve them with reasonable assumptions (documented) or flag them for follow-up?
- [ ] **Convention matching:** Does their code look like it belongs in the codebase, or does it look like dropped-in code from a different stack?
- [ ] **AI tooling use:** Is there evidence of productive AI tooling use? (Commit history, prompt artifacts, references in the write-up.) We are NOT looking for "didn't use AI" or "used AI for everything"; we're looking for calibrated use.
- [ ] **Working software:** Does it actually run? Does it pass the test cases we provided?
- [ ] **Edge case handling:** Did they think about failure modes (the customer's API is down, malformed input, auth failures), or did they ship the happy path only?
- [ ] **Write-up quality:** Is the write-up something we'd be comfortable forwarding to a customer's CTO? Specific, structured, no marketing language?
- [ ] **Time discipline:** Did they finish in budget, or did they go significantly over without explanation?

**Total: 24 points possible**

### Calibration thresholds

- 18+ → Strong; advance with confidence
- 13-17 → Adequate; advance if other rounds support
- 9-12 → Weak; advance only if Round 3 is exceptional and we're calibrating for early-career
- <9 → Decline

### Common failure modes (informational for the grader)

- **Codebase ignored.** Candidate writes code in their own preferred style, ignoring the conventions of the codebase. The most common failure. The customer's engineers will reject these PRs.
- **AI-output-only shipping.** The git history shows one large commit with no exploration, the code style is the AI's default style, the candidate cannot explain choices in the write-up. Anti-pattern 2 from the junior trajectory; an SE that ships only AI output is worse than a junior because they're customer-facing.
- **Over-engineering.** The discovery said "small integration"; the candidate built a 2,000-line framework. Calibration failure.
- **Under-engineering.** The discovery said "production-grade integration"; the candidate built a 50-line script with no error handling. Calibration failure in the other direction.
- **Time over-budget without acknowledgment.** Candidate spent 6 hours on a 3-hour exercise. Acceptable if they say "I went over budget; here's why and what I'd cut to fit"; not acceptable if they pretend it was 3 hours.

---

## Round 3 — Spec workshop simulation

The candidate runs a discovery-and-scoping conversation with one of our engineers playing a customer. The candidate's job: produce an agent-ready spec by the end of the 60 minutes.

### Setup

- Our engineer plays a customer who wants a specific integration. They have a real-shaped problem with real-shaped ambiguity.
- The "customer" answers questions but doesn't volunteer information. The candidate has to ask.
- At the 45-minute mark, the candidate spends 10-15 minutes writing the spec. Live, in a shared doc.
- The final 5 minutes: the candidate walks the engineer through the spec.

### What we're testing

- Can they hold a discovery conversation that surfaces real requirements?
- Can they distinguish "what the customer asked for" from "what the customer needs"?
- Can they produce a written spec under time pressure?
- Is the spec agent-ready — meaning, an engineer could hand it to an agent and ship?

### Rubric — score each item 0-3

- [ ] **Discovery discipline:** Did they ask clarifying questions before proposing solutions?
- [ ] **Listening:** Did they incorporate what the customer said into the spec, or did they barrel through with a preconceived design?
- [ ] **Push-back appropriately:** When the customer asked for something problematic, did they push back constructively?
- [ ] **Scope discipline:** Is the scope appropriate for what was discussed, or did it drift?
- [ ] **Spec specificity:** Is the spec concrete — specific endpoints, specific data shapes, specific failure modes — or is it hand-wavy?
- [ ] **Agent-readiness:** Could an engineer hand the spec to an agent without 30 minutes of "what does this mean" first?
- [ ] **Trade-off articulation:** Are trade-offs named? Is there at least one "we're choosing X over Y because Z"?
- [ ] **Communication:** Was the conversation comfortable? Did the candidate set the customer at ease?

**Total: 24 points possible**

### Calibration thresholds

- 18+ → Strong
- 13-17 → Adequate
- 9-12 → Weak
- <9 → Decline

### Common failure modes

- **Solo-designs.** Candidate barrels through with their own design without listening to the customer. The customer's actual problem doesn't make it into the spec.
- **Spec is too vague.** "Build an integration that handles webhooks" is not agent-ready. "POST /webhooks/customer-events accepting JSON with shape X, validating Y, persisting to table Z, returning 200 on success" is.
- **Spec is too detailed.** Candidate writes a 4,000-word document for a 200-line integration. Calibration failure.
- **Capitulates on every request.** Customer asks for something problematic; candidate agrees without understanding the implication. The spec ships pain to engineering.

---

## Round 4 — Architecture-with-AI conversation

A live system-design conversation. The candidate has AI tooling available; how they use it (or don't) is part of the signal.

This round is adapted from `people/interview-rubrics/architecture-with-ai.md`. See that document for the general rubric. SE-specific notes below.

### SE-specific calibration

- The problem should be a **customer-shaped** system-design question, not a pure infrastructure design. Example: "A customer wants to integrate our event stream with their data warehouse, processing 10M events/day with their data lineage requirements. Walk us through how you'd architect the integration."
- We're testing whether they can hold the architecture conversation with the customer's senior engineers, not whether they can architect a search system from scratch.
- Specifically watch for: do they translate from architecture terms to customer-impact terms naturally? Can they say "this design choice means your team's incident on-call rotation will look like X" — making it real?

### Common SE-specific failure modes

- **Abstract architecture without customer context.** Candidate gives a textbook event-streaming design without grounding it in the customer's situation.
- **AI tooling avoidance.** Candidate refuses to use AI tooling even when it would help. Signals miscalibration with the role.
- **AI tooling over-reliance.** Candidate prompts the AI for the design and reads it back. Signals lack of independent depth.

---

## Round 5 — Reference and final fit

Two senior engineers from the partner team(s) the SE will work with. Less interview, more "are we going to work well together."

### What we're testing

- Will the senior engineers respect this person's technical voice?
- Will this person work well with the team's communication style?
- Are there hidden concerns from the prior rounds that surface in conversation?

### Format

Open conversation, ~45 minutes. We avoid yet-another-coding-question. We do ask:

- "Walk me through how you'd ramp on our codebase if you joined."
- "What's a customer engagement you'd want to lead in the first 90 days?"
- "What would you need from us in your first month?"

### Calibration

This is largely a fit conversation. Specific blockers:

- **Engineering team has concerns about the candidate's depth.** Even with strong Rounds 2-4, if the engineers we'd want partnering with this person don't trust the technical voice, decline.
- **Communication style is a poor match.** Hostile, defensive, or evasive in the conversation. Less common after 4 rounds of process but worth checking.
- **The candidate has concerns about the role.** Sometimes Round 5 reveals "I'm not actually sure about this." Take it seriously; better to surface now than after offer.

---

## After the interview

### The debrief

Standard hiring loop debrief. Each interviewer brings their notes, scores their rubrics, and the hiring manager facilitates a conversation about strengths and gaps.

### When to make an offer

- Round 2 ≥ 18, Round 3 ≥ 18, Round 4 strong, Round 5 positive → strong yes; move fast.
- Round 2 ≥ 13, Round 3 ≥ 13, Round 4 adequate or better, Round 5 positive → yes; standard offer.
- Mixed signals (one round strong, one weak) → hiring manager judgment with input from the team.
- Any round below threshold → decline. Don't talk yourself into it.

### When to extend the process

We don't extend for additional rounds. If after 5 rounds we don't know, the answer is no. The temptation is to add a "let's have one more conversation"; resist it. The decision rarely improves.

---

## What this rubric will NOT do

- Will not catch personality issues that don't surface under interview conditions. Reference checks help; perfect filtering is impossible.
- Will not calibrate for early-career candidates the same way. The rubric assumes 5+ years of engineering background; for less experience, lower the calibration thresholds and weight Round 2 more heavily.
- Will not work in companies where engineering doesn't respect the SE function. Cultural respect upstream of the hiring process.

## Companion artifacts

- [`solutions-engineer-jd.md`](solutions-engineer-jd.md) — the role this rubric hires for
- [`tpm-interview-rubric.md`](tpm-interview-rubric.md) — adjacent rubric for TPM roles
- `people/interview-rubrics/architecture-with-ai.md` — the general architecture conversation rubric
- `benchmarks/tasks/T2-add-api-endpoint.md` — the engineering-task template that inspired Round 2
- Ch 42 §42.5 — the source
