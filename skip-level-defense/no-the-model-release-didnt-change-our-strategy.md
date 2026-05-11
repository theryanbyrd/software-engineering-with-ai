# "No, the Model Release Didn't Change Our Strategy" Memo

The template for the conversation when a frontier model dropped this week, your CEO sent you the launch tweet at 11pm, and the team is asking whether the roadmap changes.

This template is calibrated to a specific failure mode: companies that pivot every time a vendor announces something. Pivoting on each release is how you end up with a tool stack that's eight different vendors deep, none of which got past pilot, all of which the team has to maintain.

The book's stance:

> The vendor that was clearly best last quarter is rarely clearly best this quarter. [...] Standardize on one model family for stability. Do not chase every benchmark win. Switching is expensive in retraining, retesting, and harness adaptation.
>
> But switch when a new model is markedly better on your internal benchmark — not the public one. "Markedly" means at least 5 points on aggregate score and a clear pattern across multiple task types in your evaluation set. A 1–2 point bump is noise; a 5+ point bump is signal.
>
> — Ch 27 §27.x

## When to use this template

- A vendor announced a new model with bold benchmark claims (yesterday or this week)
- Your CEO has texted, emailed, or DM'd asking some variant of: *"Should we be using this?" / "Why aren't we on this?" / "Is our strategy still right?"*
- The team is buzzing in Slack about the announcement
- Your senior engineers are asking the same question informally

## When NOT to use this template

- The new model is genuinely a category change (this happens 1-2x per year, not 1-2x per month)
- Your benchmark suite has run on it and shown a 5+ point aggregate improvement
- Your internal team has been asking for a capability the new model genuinely provides
- You've already validated the new model on your evaluations

If any of these apply, don't push back — the template would be wrong. Run the migration playbook instead.

---

## Template — written response (CEO email or Slack DM)

**Subject: Quick take on [model name] launch**

> Hey [CEO name],
>
> Saw the [model name] launch and wanted to give you my read before EOD so you have something for [board call / investor meeting / Friday all-hands].
>
> **Bottom line:** No change to our strategy this week. We'll evaluate properly over the next 2-3 weeks against our internal benchmark suite. If the data supports a switch, we'll plan it; if not, we'll keep moving on the current stack. Both outcomes are fine.
>
> **Specifically what I'm doing this week:**
> 1. Running our internal benchmark (the eight-task suite) against [new model] — results in [day of next week]
> 2. Sampling 10-15 representative real-work prompts from senior engineers, running them on both — comparing transcripts, not just outcomes
> 3. Checking the new model's pricing, rate limits, and API stability claims against our actual usage patterns
>
> **What I'm watching for:**
> - 5+ point improvement on our aggregate benchmark score (1-2 points is noise; 5+ is signal)
> - Improvement specifically in our T2 tier (where most real work lives)
> - No significant regression in any tier
> - Pricing that doesn't make our budget worse
>
> **What I'm specifically NOT doing:**
> - Pivoting the roadmap based on the launch keynote
> - Asking the team to immediately try the new model on production work
> - Re-opening the vendor selection from six months ago based on this single release
>
> Pivoting on each model release is the failure mode that ends with a tool stack that's six vendors deep and the team can't maintain. Vendor's that was clearly best last quarter is often not clearly best this quarter; the metric we should optimize is not "are we always on the latest" but "are we making progress on our work."
>
> Happy to walk through the eval framework if useful — it's the same one we use for every release. Will send a one-paragraph update next [day] when results are in.
>
> [your name]

---

## Template — quick verbal version (the 11pm phone call)

> "I saw the [model] launch. Here's the read.
>
> First — no panic. Vendor announcements aren't strategy events; benchmark results on our work are. We don't know yet whether this is signal or marketing.
>
> Second — what I'm doing about it. Running our benchmark suite against the new model this week. If we see a 5+ point aggregate improvement, we plan a migration; if not, we don't. I'll have data by [day].
>
> Third — what I want from you. I want you to NOT promise anyone anything about us being on this model until we have the data. The team is anxious about pivoting; vendors are anxious to claim wins. We don't help either by committing prematurely.
>
> If the data supports a switch, you'll hear from me [day]. If not, you'll hear from me [day]. Either way, we'll be on a stable footing within 10 business days."

---

## Template — internal Slack message to the engineering channel

This is the parallel comm. Send before or simultaneously with the CEO message — never after. The team is your earlier-warning system; they're going to ask anyway.

> Hey team —
>
> Quick note on the [model] launch since folks are asking.
>
> **Where we are:** still on [current model]. No change to our stack this week.
>
> **What I'm doing:** running our benchmark suite against [new model] over the next 2 weeks. If we see a meaningful improvement on our work (5+ point aggregate), we'll plan a switch. If not, we'll stay put. Either is fine.
>
> **Why we don't pivot on each release:** model leaderboards reorder weekly. Standardizing on one family for stability is the strategy. Switching is expensive (retraining, retesting, harness adaptation); a 1-2 point bump on a public benchmark isn't worth the cost.
>
> **What I'd love from you:** if you want to try [new model] on a non-production task and report back, do it. Tag me with what worked and what didn't. Don't run it on customer code yet; we haven't done the security review.
>
> More once the eval is done.
>
> [your name]

---

## What "5+ points on aggregate" actually means

The CEO will ask. Have this ready:

> "Our internal benchmark has eight tasks across three difficulty tiers. Each task has a rubric scored 0-100. The aggregate is the mean across the eight.
>
> A 1-2 point shift is noise — same agent, same model, different runs of the same task can vary by that much. A 5+ point shift, with consistent direction across multiple task types, is signal.
>
> 'Markedly better' for us looks like: aggregate score moves from baseline X to X+5 or higher, AND at least four of the eight individual tasks improved, AND no task got significantly worse. That's the bar."

This phrasing converts an emotional question ("is the new model better?") into a quantitative one ("did it pass our specific bar?"). The conversion is the defense.

## What to do when the CEO pushes back

### "But [influencer] is saying it's a game-changer"

> "Most public influencer takes are within 24-48 hours of a launch, before any real work has been done with the model. The takes that hold up at 30 and 60 days are usually different from the launch-week takes. We'll have our own data in 2-3 weeks; that's what I'd anchor on."

### "But [competitor company] is already on it"

> "We don't know what they actually shipped or what their real workflow looks like; we know what their CTO posted on LinkedIn. Even if they're on it, we don't know whether it's working for them yet — the early-adoption period is often messy and unflattering. I'd rather be three weeks late and right than three weeks early and wrong."

### "Can we at least pilot it?"

> "Pilot meaning what specifically? If you mean 'have a few engineers try it on side projects' — yes, that's already happening informally. If you mean 'announce a switch and start migrating production workflows' — no, not before the eval. The cost of an aborted migration is much higher than the cost of waiting two weeks for data."

### "What if our eval is wrong?"

> "Possible. The eval is calibrated to our work, not to all possible work. If the new model is dramatically better on something we don't currently do, the eval would miss it. The mitigation is the qualitative complement — I'm asking senior engineers to try the new model on their hardest recent problems and report transcripts. The eval and the qualitative side together are reasonably hard to fool."

### "I just want us to be on the best thing"

> "Same. The disagreement isn't about the goal; it's about how we know what 'best' means for our specific work. The eval IS the discipline of being on the best thing. Without it, we're optimizing for being on the latest thing, which is different and worse."

## What to do when you actually should switch

If the eval supports a switch — 5+ point aggregate improvement, consistent across task types — the conversation becomes the migration playbook. Reference [`migration-playbooks/`](../migration-playbooks/) and follow the parallel-then-converge pattern. Even with strong eval results, you don't rip-and-replace mid-quarter.

The CEO will sometimes interpret "we should switch" as "switch this week." It isn't. Surfacing the eval result is the start of the migration conversation, not the end.

## What this template will NOT do

- Will not work if you don't actually run an internal benchmark. The phrase "5+ points on aggregate" is meaningless without a benchmark suite. See [`benchmarks/`](../benchmarks/) for the discipline.
- Will not work if you've previously pivoted on each release. The CEO has learned that "we'll evaluate" means "we'll switch in 6 weeks." Establish the discipline before relying on this template.
- Will not work for vendor exits or terminations. If the vendor is shutting down or a contract is being terminated, that's a forced migration. Different playbook.

## Companion artifacts

- [`benchmarks/`](../benchmarks/) — the eval that makes this conversation possible
- [`migration-playbooks/`](../migration-playbooks/) — the migration discipline if the eval supports switching
- `exec-kit/ceo-emails/` — overlapping written templates for executive comms
- Ch 27 — the model routing chapter
- Ch 31 — the metrics that make the dashboard work
