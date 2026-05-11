# The Four Buckets

The taxonomy: Score, Question, Opportunity, Train. Per Ch 19 §19.5 and Ch 31 §31.5.

## Score — the agent succeeded

### Definition

The agent produced a PR that:
- Passed verify
- Matched the spec
- Was merged with light or normal review (no substantial rework)

### What to capture

For each Score:
- **Tier** (T1/T2/T3 per Ch 19 §19.5)
- **Model used** (Haiku / Sonnet / Opus)
- **Time** (from spec to merged PR)
- **Cost** (from `cost-discipline-runbook/cost-attribution-per-pr.md`)
- **Notes** (anything worth remembering — what made the spec work; what made the harness work)

### Why Score matters

Score isn't just the success column. It's evidence of where the system works. Per Ch 31 §31.5: "Score counts rise" is what success looks like over time.

The Score data drives:
- Routing decisions (this work type works on Sonnet; don't escalate to Opus)
- Autonomy decisions (this work type has a track record of success; consider raising autonomy ceiling per `agent-autonomy-levels/raising-and-lowering-autonomy.md`)
- Spec patterns (specs that produced Score outcomes are templates for similar work)

### What looks like Score but isn't

- **Score with substantial rework**: the agent produced a PR but the engineer rewrote half of it before merge. That's closer to a Train or Opportunity outcome — the harness/spec didn't actually deliver.
- **Score that didn't match spec**: the agent produced a PR that merged but doesn't do what the spec asked. That's a review failure, not a Score.
- **Score that introduced incidents later**: the PR merged but produced a production issue 2 weeks later. Per `incident-postmortem-templates/`, this becomes a postmortem; reclassify as Train, Opportunity, or Question depending on root cause.

## Question — the model can't do this work yet

### Definition

The failure is a genuine capability gap. The model is not capable of this kind of work reliably regardless of how good the spec is or how complete the harness is.

### What to capture

For each Question:
- **What the work was** (task type; specific challenge)
- **What the agent failed at** (specific aspect; not just "couldn't do it")
- **What was tried** (different prompt; different model; different harness; what didn't help)
- **Decision** (route to humans for now; revisit on next model release)

### Why Question matters

Question is the bucket that informs:
- Model selection: if Question failures cluster on specific work types, that's a routing signal
- Vendor escalation: persistent Questions on a vendor's model are feedback to the vendor
- Capability planning: knowing what the model can't do is useful for roadmap decisions

Per Ch 31 §31.5: "Question counts fall stepwise when new models drop." A new model release should reduce Question failures in some categories. If it doesn't, that's a signal too.

### What looks like Question but isn't

- **Question that's actually Train**: the model could do it with a better spec; the engineer assumed it was capability gap. Test by improving the spec; if it then succeeds, it was Train.
- **Question that's actually Opportunity**: the model could do it with the right context; the engineer assumed capability gap. Test by adding the missing context; if it then succeeds, it was Opportunity.

The discipline: don't classify as Question without ruling out Train and Opportunity first.

### Resolution path for Question

1. Document the capability gap
2. Route the specific work to humans (per `agent-autonomy-levels/forbidden-categories.md` if the work is high-stakes)
3. Re-test on next model release
4. If the gap closes: celebrate; update routing
5. If the gap persists: it's a known limitation; build around it

## Opportunity — the harness was missing something

### Definition

The agent could do the work — but the harness was missing context, fixtures, contracts, or documentation the agent needed.

### What to capture

For each Opportunity:
- **What was missing** (specific: a README; a fixture; an ADR; an AGENTS.md section)
- **Where it should live** (which file; which directory)
- **Who can fix it** (typically the team that owns the relevant module)
- **Estimated effort** (minutes / hours / days)

### Why Opportunity matters

Per Ch 31 §31.5:

> A team that is improving will see Train and Opportunity counts fall over months as PMs sharpen and harnesses fill in gaps.

Opportunity failures are the team's harness backlog made visible. Each Opportunity is a specific, addressable gap.

### Common Opportunity patterns

- **Missing fixture**: the agent didn't have realistic test data; couldn't write tests
- **Missing AGENTS.md section**: the agent didn't know about a key module's conventions
- **Missing skill**: the agent had to figure out a repeatable pattern from scratch
- **Missing CODEOWNERS**: the agent didn't know who reviews this kind of change
- **Missing ADR**: the agent didn't have the context for why a system was designed a certain way
- **Stale documentation**: the docs said one thing; the code did another; the agent followed the docs

### What looks like Opportunity but isn't

- **Opportunity that's actually Train**: the spec was vague; the agent didn't have what to do. Better spec might have prevented the need for additional context. Test by sharpening spec.
- **Opportunity that's actually Question**: even with the missing context, the model wouldn't have succeeded. Test by adding the context manually and retrying.

### Resolution path for Opportunity

1. Document what was missing
2. Open a "legibility ticket" per Ch 19 §19.5
3. Assign owner (the team that owns the relevant module)
4. Ship the harness improvement
5. Verify: re-attempt similar work; the agent succeeds

The team's harness improves over time as Opportunities are closed.

## Train — the spec was insufficient

### Definition

The failure was caused by an unclear, incomplete, or contradictory spec. A better spec would have prevented the failure.

### What to capture

For each Train:
- **What was unclear** (specific: ambiguous requirement; missing edge case; contradictory acceptance criteria)
- **Who wrote the spec** (PM, engineer, AI assistant — for coaching purposes; not blame)
- **What the better spec would have said**

### Why Train matters

Per Ch 19 §19.5:

> This becomes a coaching loop: the assistant flags the gap, the PM upgrades the spec, the team's general spec quality rises over time.

Train failures are the team's spec-writing skill made visible. Each Train is a coaching opportunity.

### Common Train patterns

- **Vague acceptance criteria**: "the feature should work well" — doesn't specify what "work" means
- **Missing edge cases**: what happens when input is empty? What happens at scale? What happens when external service is down?
- **Contradictory requirements**: section 2 says X; section 5 implies not-X
- **Missing non-goals**: spec says what to build but not what NOT to build; agent over-builds
- **No example**: spec describes the behavior abstractly; an example would make it concrete

### What looks like Train but isn't

- **Train that's actually Opportunity**: the spec was clear but the agent didn't have surrounding context. Specs can't be infinitely comprehensive; some context belongs in the harness.
- **Train that's actually Question**: even a perfect spec wouldn't have made the model capable. Test by writing the perfect spec and retrying.

### Resolution path for Train

1. Document the spec gap
2. Coach the spec author (in 1:1, not publicly)
3. Use the coaching to inform the team's spec template / examples
4. The team's spec quality rises over time

Per Ch 19 §19.5, the ticket-writing assistant ("Tixie pattern") is one operational mitigation: an AI that workshops specs with PMs surfaces these gaps before the spec hits the implementing agent.

## Distinguishing the buckets in practice

Many failures are ambiguous. Use this triage flow:

```
Did the agent succeed?
  Yes → Score
  No → continue

Would a better spec have made it work?
  Yes → Train
  No → continue

Would more context (docs, fixtures, AGENTS.md) have made it work?
  Yes → Opportunity
  No → continue

Is this a model capability gap?
  Yes → Question
  No → check assumptions; usually it's actually Train or Opportunity in disguise
```

When in doubt, default to Train or Opportunity rather than Question. Question implies "we can't fix this"; Train and Opportunity imply "we can fix this." The bias toward fixable buckets is correct most of the time.

## Per Ch 31 §31.5 — what the ratios mean

| Pattern | Diagnosis | Action |
|---|---|---|
| Mostly Train | Direction issue (Ch 5) | Spec coaching; PM training |
| Mostly Opportunity | Architecture/Legibility issue (Part II) | Harness investment |
| Mostly Question | Model selection / scope mismatch (Ch 26) | Routing changes; capability boundaries |
| Mostly Score | System working | Raise autonomy ceiling for that work type |

## Companion artifacts

- [`triage-process.md`](triage-process.md) — the workflow
- [`weekly-retro-structure.md`](weekly-retro-structure.md) — when triage runs
- [`closing-the-loop.md`](closing-the-loop.md) — what happens after triage
- [`reading-the-ratios.md`](reading-the-ratios.md) — interpreting trends
- Ch 19 §19.5, Ch 31 §31.5 — sources
