# Technical Product Manager Interview Rubric

The interview structure for a TPM hire calibrated to Ch 42 §42.5's framing. Tests whether the candidate can write executable specs and hold cost-vs-capability conversations with engineering — not whether they can talk about product strategy in the abstract.

This rubric encodes a higher technical bar than a standard PM interview process. Expect a smaller candidate funnel; expect higher signal in the candidates who clear it.

## The five rounds

| Round | Format | Duration | What we're testing |
|---|---|---|---|
| 1. Hiring manager screen | Conversation | 45 min | Background fit; technical depth is real |
| 2. Executable spec exercise | Async | ~2 hours | Can produce an agent-ready spec |
| 3. Cost-vs-capability conversation | Live with EM | 60 min | Can hold a senior engineering conversation |
| 4. Cross-functional simulation | Live, multi-role | 60 min | Can navigate competing priorities and constraints |
| 5. Reference and final fit | Live with team | 60 min | Will the partnership work |

Total candidate load: ~5 hours of substantive interviewing.

We do not run product-sense-without-context rounds. We do not run case studies of the "design Uber for X" variety. They filter for the wrong things.

---

## Round 1 — Hiring manager screen

A conversation to confirm the technical bar is reachable.

### What you're testing

- The technical background is real. They have a CS degree, prior engineering experience, or strong evidence they're operating at a technical bar.
- They've shipped real product work, not just had opinions about it.
- They can discuss AI tooling without bluffing.
- Their writing is good (you'll see this in their materials; cross-check in conversation).

### Sample questions

- "Walk me through a feature you owned end-to-end in the past year. What did you ship, what was the impact?"
- "What does your AI-tooling workflow look like? Do you use it for spec work? Do you read code in PRs?"
- "Tell me about a time you pushed back on engineering's estimate. How did it land?"
- "What's the most technical decision you've made as a PM? What was the trade-off?"

### Calibration

- **Strong:** specific stories, calibrated language, comfortable with technical detail
- **Weak:** generic stories, "I work closely with engineering" without specifics, defensive about technical questions

---

## Round 2 — Executable spec exercise

The differentiating round. Tests whether the candidate can produce a spec an engineer can ship from.

### Setup

We give the candidate three things:

1. A **customer problem description**. ~1 page. Real-shaped. Has ambiguity.
2. A **codebase summary**. ~1 page. What we have, what we don't. Stack, conventions, constraints. (Not the actual codebase — a description sufficient to write a spec for.)
3. A **time budget**. We say "spend up to 2 hours."

The candidate submits:
- The spec itself
- A short cover note (~250 words) explaining design choices

### What we're testing

- Can they identify what the customer actually needs from what they asked for?
- Is the spec specific enough that an engineer with AI tooling can ship from it?
- Did they engage with the codebase summary, or write a spec that ignores existing patterns?
- Are trade-offs articulated, or does the spec read as "and then everything works"?

### Rubric — score each item 0-3

- [ ] **Problem framing:** Does the spec begin with what's being solved (and for whom), or jump to what's being built?
- [ ] **Specificity:** Are the inputs, outputs, data shapes, and failure modes concrete?
- [ ] **Codebase awareness:** Does the spec reference the existing patterns from the codebase summary, or does it propose work that ignores what's there?
- [ ] **Agent-readiness:** Could an engineer hand this to Claude Code or Cursor and ship a substantive first cut without a 30-minute "what does this mean" conversation first?
- [ ] **Trade-off articulation:** Are at least 2 trade-offs named with reasoning, including what was rejected and why?
- [ ] **Scope discipline:** Is the scope appropriate, or has it ballooned beyond what was asked?
- [ ] **Edge cases / failure modes:** Are real failure modes identified, or is the spec happy-path-only?
- [ ] **Writing quality:** Is the spec readable? Tight? No jargon? Would the team forward it without rewriting?

**Total: 24 points possible**

### Calibration thresholds

- 18+ → Strong; advance with confidence
- 13-17 → Adequate; advance if other rounds support
- 9-12 → Weak; decline unless Round 3 is exceptional
- <9 → Decline

### Common failure modes

- **Marketing-document spec.** Reads like a launch announcement. Long on "this will be amazing" and short on "here's what we're building and how it works."
- **Detailed-Jira-ticket spec.** Reads like a senior PM's user story that engineering will rewrite as the actual spec. Too high-level for agent-ready work.
- **Code-without-context spec.** Reads like the candidate started writing the implementation. Too low-level; lacks the why and the trade-offs.
- **No trade-offs.** Spec presents the design as the obvious answer with no acknowledgment that alternatives existed. Calibration miss.
- **Scope drift.** The customer described a small integration; the spec is a 6-month roadmap.

---

## Round 3 — Cost-vs-capability conversation

A live conversation with an engineering manager. The EM presents a real-shaped problem with cost trade-offs; the candidate has to hold the conversation.

### Setup

The EM picks a scenario from a small catalog we maintain. Examples:

- "We're considering using a frontier model for every customer support response. The model would cost $X per response, the response quality would be Y, the alternative is a smaller model at Z cost. Walk me through how you'd think about this."
- "Engineering says shipping the new feature with full AI tooling integration is 6 weeks; without it is 3 weeks but the feature is 60% as useful. How do you frame this trade-off?"
- "Our token spend has tripled this quarter. The CEO is asking why we shouldn't cap usage. What's your view?"

The conversation is live. The EM pushes back; the candidate engages.

### What we're testing

- Do they have working knowledge of AI-tooling economics? Can they distinguish input/output token costs, batched vs. interactive workloads, frontier vs. open-weight pricing?
- Can they hold the conversation under pushback, or do they capitulate / dismiss?
- Do they ask the right second-order questions, or jump to a recommendation?
- Are their trade-offs grounded in specifics or in vibes?

### Rubric — score each item 0-3

- [ ] **Question quality:** Did they ask clarifying questions before recommending? (Volume? Frequency? Sensitivity? Use case?)
- [ ] **Cost fluency:** Do they understand the cost structure they're discussing? (Token pricing, batching, model tiers.)
- [ ] **Capability fluency:** Do they understand what frontier vs. lighter models can and can't do?
- [ ] **Trade-off framing:** Do they frame the trade-off in concrete terms, or in abstract "balance" language?
- [ ] **Pushback engagement:** When the EM pushes back, do they engage substantively or fold?
- [ ] **Honest uncertainty:** Do they say "I'd want to know X before recommending" when appropriate, or pretend to know?
- [ ] **Decision discipline:** Does the conversation produce a recommendation with reasoning, or does it stay theoretical?
- [ ] **Stakeholder awareness:** Do they consider the engineering team, the customer, the CFO, in the framing?

**Total: 24 points possible**

### Calibration thresholds

- 18+ → Strong
- 13-17 → Adequate
- 9-12 → Weak
- <9 → Decline

### Common failure modes

- **No cost fluency.** Candidate cannot reason about per-token pricing or workload economics. Disqualifying for the role.
- **All abstraction.** Candidate talks in "we should weigh X against Y" without specifics. The EM's pushback is asking for specifics; the candidate keeps abstracting.
- **Capitulates on pushback.** EM asks "are you sure?"; candidate immediately reverses.
- **Dismisses the EM's concern.** EM raises a real concern; candidate brushes it off ("we'll figure it out at scale"). Calibration failure.
- **Too quick to recommend.** Candidate gives a confident answer in 90 seconds without asking the questions that would change the answer.

---

## Round 4 — Cross-functional simulation

A scenario where the candidate has to navigate competing priorities. Mock customer, mock engineer, mock designer (or 2 of 3 depending on team availability). 60 minutes.

### Setup

The candidate is briefed on a scenario where:
- A customer wants Feature A with a tight timeline
- Engineering says Feature A as scoped is 6 weeks; a lighter version is 2 weeks
- Design has concerns about the lighter version's UX
- The candidate has to chair the conversation

The mock participants are senior team members playing their roles with real-shaped pushback.

### What we're testing

- Can they chair a meeting that produces a decision?
- Do they listen, or do they interrupt and steer?
- Can they hold competing perspectives in mind without collapsing to one?
- Do they make a decision (or surface that one needs to be made by leadership), or do they punt?

### Rubric — score each item 0-3

- [ ] **Meeting structure:** Does the conversation have a clear arc — issue framed, perspectives heard, decision reached or surfaced?
- [ ] **Listening:** Do they engage with what each role said, or run their own agenda?
- [ ] **Engineering respect:** Do they treat engineering's estimate as data, or argue with it?
- [ ] **Customer empathy:** Do they keep the customer's actual problem in view, or focus only on what engineering can ship?
- [ ] **Design respect:** Do they take design's concern seriously, or dismiss it?
- [ ] **Decision discipline:** Did the meeting produce a decision (or a clear next step toward one)?
- [ ] **Communication:** Was the meeting comfortable? Did they manage time?
- [ ] **Follow-up:** Did they articulate what happens next — who does what, by when?

**Total: 24 points possible**

### Calibration thresholds

- 18+ → Strong
- 13-17 → Adequate
- 9-12 → Weak
- <9 → Decline

### Common failure modes

- **Picks a side immediately.** Candidate sides with engineering or with customer in the first 5 minutes; doesn't hold the tension.
- **Collapses to consensus.** Candidate seeks agreement at all costs; the meeting ends with everyone "aligned" but no real decision.
- **Talks more than they listen.** Candidate's voice dominates the meeting. The mock participants barely speak.
- **Punts the decision.** "Let me think about it and get back to you" when the right move is to decide or to articulate what's needed to decide.

---

## Round 5 — Reference and final fit

Two senior engineers and one designer from the team the TPM would partner with.

### What you're testing

- Will the engineers respect this person?
- Will design enjoy partnering with this person?
- Are there concerns from earlier rounds that need surfacing?

### Format

Conversation. ~45 minutes. Light topics:

- "What's a customer pain point you've been thinking about that we haven't talked about yet?"
- "What would your first 30 days look like if you joined?"
- "What do you need from engineering and design to do your job well?"

### Calibration

Largely a fit conversation. Decline if:
- Engineering team has concerns the candidate isn't technical enough to do the job we described
- Designer has concerns the candidate doesn't take design input seriously
- Hidden red flags surface (defensiveness, evasiveness)

---

## After the interview

### Offer thresholds

- Rounds 2 + 3 both ≥ 18, Round 4 ≥ 13, Round 5 positive → strong yes; move fast
- Rounds 2 + 3 both ≥ 13, Round 4 ≥ 13, Round 5 positive → yes; standard offer
- Mixed (one round strong, one weak) → hiring manager judgment with team input
- Any round below threshold → decline

### When to NOT extend the process

We don't add rounds. If after 5 rounds we don't know, the answer is no.

We don't add a "let me check with leadership" round. The hiring manager has authority within the rubric; if leadership wants different filters, change the rubric, not the individual hire's process.

---

## What this rubric will NOT do

- Will not work for non-technical PM hires. Different role; different filters.
- Will not catch culture issues that don't surface in interview. Reference checks help; perfect filtering is impossible.
- Will not work without engineering buy-in. If engineering doesn't think TPM is real work, the rubric is hollow.
- Will not surface candidates who are technical-but-quiet. Some strong candidates are reserved in conversational rounds; weight the spec exercise heavily for these.

## Companion artifacts

- [`technical-product-manager-jd.md`](technical-product-manager-jd.md) — the role this rubric hires for
- [`se-interview-rubric.md`](se-interview-rubric.md) — adjacent SE rubric
- `people/interview-rubrics/architecture-with-ai.md` — adjacent engineering rubric
- Ch 4 — what an executable spec looks like
- Ch 42 §42.5 — the source
