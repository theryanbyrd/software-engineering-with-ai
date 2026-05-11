# Customer Conversation Scripts

Verbatim openers for the live conversations with customers' technical buyers and security teams about AI tooling. Direct implementation of Ch 31 §31.6 and Ch 41.

These scripts are for the conversations that don't fit a written questionnaire — the live customer call where their CISO or VP Engineering is asking pointed questions and you need to hold your ground without bluffing.

## When these scripts apply

- Customer security review meeting (live, video or in-person)
- Customer renewal conversation where AI usage is on the agenda
- Procurement-stage discovery call with the customer's technical leadership
- Post-incident customer conversation where AI authorship is the topic
- Industry conference where a customer corners you about AI practices

## When these scripts do NOT apply

- Routine sales conversations where AI hasn't come up. Don't proactively raise it; let the conversation flow.
- Conversations with non-technical customer roles. Different audience; different language; usually managed by sales/CS without you.
- Conversations where the customer has already decided to leave. Damage control is a different domain.

## §1 — The opening framing for any customer AI conversation

When a customer raises AI tooling for the first time in a conversation, your first 60 seconds set the tone for the entire interaction.

### The opener (verbatim)

> "Glad you asked. Quick context, then I'll answer specifics.
>
> We use AI tooling extensively in our engineering process. We've used it for about [N] months at production scale. We have an internal governance discipline around it — approved tooling matrix, data classification, review processes. I can walk you through any of those at the level of detail you want.
>
> What I'd like to understand: what's driving the question for you? Is this part of a routine security review, are you working on your own AI governance and want to compare notes, or is there a specific concern? The level of detail I'd give you depends on what you're actually trying to learn."

### Why this works

- **Direct admission of usage.** Doesn't try to minimize.
- **Names governance discipline before being asked.** Signals you've thought about it.
- **Asks what they're actually trying to learn.** A security review needs different detail than a curious-CTO conversation. Most customers will tell you what they're trying to learn, which lets you calibrate.

### What to NOT say in the opening

- *"We use AI tools, but only in limited ways."* — defensive, evasive. Customers can tell.
- *"AI is just one of many tools."* — minimization. Customers will probe harder.
- *"We don't disclose our development methodology."* — hostile. Loses the conversation.

---

## §2 — When the customer is doing routine due diligence

The most common case. The customer's security or compliance team has a checklist. Your job: answer the questions, hand them the documentation, move on.

### Opener

> "Happy to walk through the standard questions. We've answered these for [N] enterprise customers; I'll move quickly through the ones that have standard answers and we can spend more time on anything specific to your situation.
>
> Three things I'd recommend you have for your records: our DPA which lists AI tooling subprocessors, our SOC 2 Type II report which covers our development practices, and the security questionnaire response we'll send you. Want me to start with any of those, or work through your questions first?"

### What you're doing

- Signaling you're prepared.
- Naming the documentation that answers most questions.
- Letting them choose the order — they appreciate the agency.

---

## §3 — When the customer's CISO has a specific concern

Pointed conversation. Their CISO has read about AI tooling risks; they have a specific worry. Your job: address the specific worry; don't give a generic security pitch.

### Opener

> "I want to understand the specific concern. AI tooling covers a lot of ground — there's the development side, the product features side, the data flows, the vendor risk. Each one has different mitigations. What's the specific scenario you're worried about?"

### Why this works

- Forces specificity. Vague concerns produce vague conversations; specific concerns produce solvable problems.
- Names the categories without claiming any of them are concerning. The CISO picks.

### Common follow-ups by category

#### "Concern: your engineers might leak our code to AI vendors"

> "Right. Two parts to that. The mechanical: we have contractual prohibitions on training with our vendors, and we have data classification rules that prevent customer code from flowing to consumer AI tools. The behavioral: we have an internal compliance program that audits this. We had to do a cleanup ~18 months ago when we found shadow AI usage; we've been clean since.
>
> The thing I'd want you to understand: the prohibitions are real but not absolute. An engineer could in principle paste customer code into a personal ChatGPT account on their personal device. The mitigation is the audit program plus the cultural norm; we don't claim it's mathematically impossible.
>
> What level of assurance do you need on this? Because the answer for SOC 2 is different from the answer for a regulator."

#### "Concern: your AI-authored code might have bugs that hurt us"

> "Real concern. The framing I'd push back on slightly: AI-authored code has bugs at roughly similar rates to human-authored code, with different failure patterns. The mitigation isn't 'don't use AI tools'; it's 'have review and test discipline that catches both kinds of bugs.'
>
> Specifically, we run [verify command, slop detector, code maturity scoring, etc.] on all changes. We've had [N] incidents in the past year that traced to AI-authored code; we've published the post-incident reviews. The pattern: when we have an incident with AI-authored code, the failure was usually a gap in the review process, not the AI tooling per se.
>
> The thing I want to be honest about: bugs will happen. Our discipline is to catch them earlier and post-mortem them honestly, not to claim we've eliminated them."

#### "Concern: your AI vendors might have a breach that affects us"

> "Vendor risk is real. Our position: we treat AI vendors like any other subprocessor. They're listed in the DPA. They've been through our security review. We have contractual breach notification commitments. Their certifications [SOC 2, ISO 27001, etc.] are in our records.
>
> The specific concern with AI vendors that's slightly different: their training-data practices. We have explicit contractual prohibitions on training with our data, and we audit compliance through periodic vendor reviews. If you want, I can connect you with our procurement team for the specific language."

#### "Concern: AI tooling will eventually replace your engineers and quality will degrade"

> "Honest answer: we don't know how this plays out long-term. Right now, AI tooling is a productivity multiplier for skilled engineers, not a replacement. Our engineering headcount has grown [or held steady], not shrunk. The skills required to use AI tooling effectively are themselves senior engineering skills.
>
> What we measure: code quality (we use a maturity scoring rubric), defect rates, customer-impacting incidents. We track these monthly. If we saw quality degrade, we'd respond. We haven't seen it.
>
> The thing I'd offer: I can share our quality dashboard at a high level under NDA. The numbers are stable."

---

## §4 — When the customer wants you to commit to specific AI restrictions

The customer is asking for a contractual commitment that goes beyond your standard ToS/DPA. Your default posture is to decline; sometimes you'll accept narrowly-scoped commitments.

### Opener (when declining)

> "I understand the request. We don't typically agree to that for a specific reason: maintaining a separate development pipeline for individual customers is operationally complex and creates risk that the carve-out gets missed. We'd rather have one consistent practice across all customers.
>
> What I can offer: explicit commitments about the things you actually care about — for example, the prohibition on training on your data, the approved tooling matrix, the review processes. Those are real commitments we make to all customers. Would those address the underlying concern?"

### Opener (when accepting narrowly)

> "Let me make sure I understand the specific commitment you're asking for, then we'll discuss what's feasible. Walk me through what you want — exactly which restriction, on which scope, with what exception language."

Then: actually understand the request, run it by legal, give a real answer. Don't commit verbally to anything contractual without legal review.

---

## §5 — When the customer asks about a specific past incident

Customer has read your status page or PIR archive and is asking about a specific incident. Your job: direct them to the public document; provide additional context only if material.

### Opener

> "Happy to talk through that one. The canonical detail is in our public post-incident review at [link]; have you had a chance to read it?
>
> [If yes:] What questions does it leave open?
> [If no:] Quick summary: [3-sentence verbal version of the PIR]. Read the public version when you have time; if it leaves questions, I'm happy to talk specifics."

### Why this works

- Directs them to the canonical answer. Avoids you giving an answer that diverges from the public record.
- Doesn't add detail beyond the public document. The public version is the canonical answer.
- Offers follow-up if needed.

### What to NOT do

- Add color or context that isn't in the public PIR. If the public PIR is incomplete, that's a separate problem; don't fix it in real-time over a customer call.
- Speculate about what other vendors' similar incidents look like. Invites comparison you don't want.
- Apologize again beyond what's already public. Repeat-apologizing reads as guilt; the public PIR is the apology.

---

## §6 — When the customer presses on your specific tool choices

Sometimes the customer wants you to defend why you use Vendor X versus Vendor Y. Your job: don't engage at the vendor-level; redirect to your governance discipline.

### Opener

> "Tool selection is something we revisit regularly. We use [vendor] currently for [specific reason]. We benchmark alternatives quarterly. We've changed tools when our internal benchmark showed a 5+ point improvement on alternatives; we haven't changed when the improvement was marginal.
>
> The thing I'd want to clarify: are you asking because you have a specific concern with [vendor], or because you want to understand our process for picking and switching? The answer would be different."

### Why this works

- Names the discipline (regular re-evaluation) without committing to specific vendors.
- Distinguishes between "concern with this vendor" (something to address) and "curious about your process" (something to share).

---

## §7 — When you don't know the answer

Inevitable. The customer asks something specific and you don't have the data on hand. The honest answer is the right answer.

### Opener

> "Honest answer: I don't have that data with me. I want to give you the right answer rather than make one up. Here's what I'll do: [specific commitment — pull the data and send by N, get our [team] to follow up by N, set up a follow-up call with [the right person]]. Does that work?"

### Why this works

- Honesty about not knowing. CEOs and CISOs respect this.
- Specific follow-up commitment. Vague "we'll get back to you" is suspicious; specific commitment is professional.
- Offers a real path forward.

### What to NOT do

- Improvise an answer. The customer notices; the wrong answer creates a bigger problem than "I don't know."
- Punt without committing to follow-up. "Good question, I'll have to check" without specifics is interpreted as "I'll never get back to you."

---

## §8 — When the conversation goes sideways

The customer is hostile. They've decided you're untrustworthy, or they have an agenda, or someone on their team is anti-AI for ideological reasons. Your job: stay calm; don't escalate; offer specific paths forward.

### Opener

> "I hear that you're frustrated. I want to make sure we're addressing the actual concern. Walk me through specifically what would change your assessment — what data would you need, what commitment would you need, what conversation with whom?
>
> If the concern is fundamental — meaning, no commitment we could reasonably make would address it — that's also useful to understand, even if it ends in 'we're not the right vendor for you.' I'd rather know that now than later."

### Why this works

- Acknowledges the emotion without absorbing it.
- Asks for specificity about what would change the customer's mind.
- Names the possible-bad-outcome ("not the right vendor") openly. Surfaces it from "the elephant in the room" to "thing we could acknowledge."

### What to NOT do

- Get defensive.
- Promise things you can't deliver to calm them down.
- Dismiss the concern as unfounded.
- Cut the conversation short to escape it.

---

## What these scripts will NOT do

- Will not work in a culture where you're not actually doing the governance discipline. Customers can tell when answers are theater.
- Will not work without rehearsal. The "verbatim" framing in this document means "memorize the structure, internalize the language, deliver in your voice." Reading from a script live is worse than improvising.
- Will not work if the wrong person is in the room. The senior technical lead has these conversations; not the salesperson, not the lawyer alone.

## Setup before the conversation

1. **Bring the data.** Quality dashboard, security questionnaire response, DPA reference. Don't promise to send things later that you should have brought.
2. **Brief the salesperson.** They're in the room; they should know what the conversation is about and what role they're playing (usually: present, not driving).
3. **Pre-decide your bottom line.** What commitments are you willing to make? What requests will you decline? Knowing this in advance prevents in-meeting capitulation.
4. **Practice the openers.** Once each, out loud. Sounds awkward in writing; works in practice.

## Companion artifacts

- [`security-questionnaire-answers.md`](security-questionnaire-answers.md) — the written counterpart
- [`status-page-language.md`](status-page-language.md) — for incident-related disclosure
- [`ai-authorship-disclosure-tos.md`](ai-authorship-disclosure-tos.md) — the contract language behind the verbal commitments
- [`disclosure-decision-framework.md`](disclosure-decision-framework.md) — when to disclose what
- `migration-playbooks/team-conversation-scripts.md` — adjacent discipline for internal conversations
