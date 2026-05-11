# The Six-Metric Dashboard Explainer

The conversation when a CEO, CTO, or board member asks "what are we measuring on the AI program and why?"

This document is two things: (1) the verbatim explainer you can adapt for the conversation, and (2) the discipline behind it so you don't end up defending a dashboard you can't actually maintain.

## The opening framing (verbatim — 2 minutes)

> "Six metrics. Five quantitative, one qualitative. Trend lines, not point-in-time.
>
> Three of the six measure outcomes — what the team is shipping. Three measure inputs — what's powering it. Together, they tell us whether the AI investment is producing real engineering output or just usage.
>
> The single most important thing I want you to take away from this dashboard is the *ratio* between metrics 3 and 5. Velocity rising while quality stays flat means the program is working. Velocity rising while quality degrades is the failure mode that almost destroyed the program at three companies I've watched closely. We track both because either alone is misleading.
>
> Two minutes per metric, then I'll show you the current state and the trend lines."

## The six metrics — verbatim explanations

Use these one at a time as the CEO asks. Don't pre-load all six; let curiosity drive.

### Metric 1 — AI Token Usage per Developer (median, weekly)

> "What it is: median tokens per active developer per week, broken down by model tier. Not mean — median, because a few power users skew the mean badly.
>
> What it tells us: adoption. If this is below the company-wide median for our tier, the rollout isn't landing. If it's well above, we may be on track for a budget surprise we should plan for.
>
> What it does NOT tell us: productivity. A developer using more tokens isn't necessarily more productive — sometimes it's the opposite. We do not use this metric to evaluate individuals.
>
> Source: pulled from Claude Code's OpenTelemetry export and the Anthropic Analytics API. Updates daily.
>
> Current trend: [your number]. We're tracking [up/flat/down] over the quarter, which is [healthy/concerning/expected]."

### Metric 2 — Code Maturity Score (1-10, LLM-graded against a rubric)

> "What it is: every PR diff, plus a five-band rubric describing what code looks like at each level, fed to a frontier model that scores the diff with reasoning. Team-level moving average.
>
> What it tells us: are we shipping code that looks like junior intern work, mid-level work, or senior work? The trend matters more than the absolute number — a team consistently at 6.0 that drifts to 5.4 is sending a signal.
>
> What it does NOT tell us: whether the code is *correct*. The model is grading shape, not behavior. We rely on tests and review for correctness.
>
> Calibration: we've validated the LLM grader against human grades on a 50-PR sample of our own codebase. Inter-rater agreement is within 1 point 87% of the time. We re-validate quarterly because the underlying model changes.
>
> Current trend: [your number]. The rubric is in [link to internal doc]."

### Metric 3 — Features Delivered to Bugs Introduced Ratio

> "What it is: count of features shipped to production divided by count of bugs introduced in the same window. Monthly.
>
> What it tells us: are we shipping value or shipping rework? This is the inverse of DORA's 'change failure rate.'
>
> The definitions matter. We define a 'feature' as anything mapped to a user-facing story; we define a 'bug introduced' as a defect with a verified root cause in code merged in the past 60 days. We don't count operational issues (cert expiry, dependency CVE) because those aren't AI-tooling-influenced.
>
> What it does NOT tell us: customer impact severity. A 1:0.2 ratio with one severity-1 customer outage is worse than a 1:1 ratio of trivial bugs. We track severity-1s separately.
>
> Current trend: [your number]."

### Metric 4 — Lead Time from User Story to Production

> "What it is: median time from when a story enters 'in progress' to when the related code is in production with feature flag on. DORA's 'lead time for changes' with the feature-flag adjustment.
>
> What it tells us: speed.
>
> Median, not mean. P90 if asked.
>
> What it does NOT tell us: what should and shouldn't ship. A two-day lead time on the wrong feature is worse than a six-day lead time on the right one. Direction discipline is upstream of this metric.
>
> Current trend: [your number]."

### Metric 5 — Story Points Delivered

> "What it is: team velocity. We track the trend, not the absolute number, because absolute story-point values are not comparable across teams.
>
> What it tells us: quantity.
>
> What it does NOT tell us anything useful in isolation. Read alongside metric 3. Velocity rising with metric 3 flat or improving is the success pattern. Velocity rising with metric 3 deteriorating is the failure pattern.
>
> Current trend: [your number]."

### Metric 6 — Predictability: 1 − (standard deviation / average) of committed vs delivered points

> "What it is: how reliably we deliver what we commit to. A team that consistently delivers 35 ± 3 points scores higher than a team that delivers 50 ± 25 points.
>
> What it tells us: this is the most underrated metric on the board. Predictability is what makes the rest of the company able to plan around engineering. AI tooling can hurt this metric — agents are good at generating optimism but not at calibrating commitments — and we watch for it.
>
> What it does NOT tell us: speed in absolute terms.
>
> Current trend: [your number]."

## The seventh metric (qualitative) — failed-one-shot triage

> "Once a week, a senior engineer reviews the agent sessions where the agent failed to one-shot a task. Five-minute review. The output is a one-line note per case: did the agent fail because the spec was unclear, because the codebase had a hidden constraint, because the model is genuinely worse at this kind of work, or because the engineer prompted poorly.
>
> Four categories. Trends across them tell us where to invest.
>
> This is qualitative, weekly, low-overhead. It's the metric that catches things the dashboard can't."

## The "what we deliberately don't measure" section

If the CEO asks about a metric you don't track, this is the response:

> "We deliberately don't measure that. Here's why.
>
> Lines of code: rewards verbosity. AI tooling generates more lines per fix, which would distort.
> Number of commits or PRs in isolation: rewards small PRs regardless of substance.
> Suggestion acceptance rate: doesn't correlate with productivity. Engineers who critically reject suggestions often outperform those who accept everything.
> AI usage volume per individual: as I mentioned in metric 1, this is a leading indicator of adoption, not of performance. Using it for performance evaluation breaks the metric — engineers gam it.
> Hours spent coding: surveillance metric with no productivity signal. We don't track it.
>
> The list of what NOT to measure is in [Ch 31 §31.2]. Happy to walk through any specific one."

## Common follow-up questions and verbatim responses

### "Why don't we have a single number that tells us if it's working?"

> "Because no single number is honest. The closest we have is the ratio between metric 3 (quality) and metric 5 (velocity), and that's a *direction*, not a number. If a vendor is selling you a single number, the number is gamed.
>
> What I can tell you is whether the trend lines are coherent — meaning velocity, quality, and predictability are moving in directions that suggest real productivity gains rather than just usage. Right now they [are / are not], and here's what I'm seeing in each."

### "How does this compare to industry benchmarks?"

> "Industry benchmarks for AI tooling are noisy. The METR 2025 RCT and the 2026 follow-up are the highest-quality empirical work; both show large dispersion across teams. DORA's 2025 and 2026 reports show AI-using teams have wider performance distribution than non-AI teams — meaning the top is higher and the bottom is lower.
>
> What I'd compare us to is *ourselves* eight months ago. We're [X% better / flat / Y% worse] on the composite that matters for our work."

### "Can we add a metric for [thing]?"

> "Probably yes, with a caveat. Every metric is a small operational tax to maintain. The six we have is calibrated to the load the platform team can sustain. If we add one, I want to retire one. Tell me what problem the new metric would solve, and I'll show you which of the six is the weakest match for our situation."

### "How long until the AI investment shows up in [revenue / cost / a number the CEO cares about]?"

> "AI tooling is infrastructure. Like other infrastructure, it shows up in the metric *one level upstream* of the leadership-facing number. Our metrics 3, 4, and 5 are leading indicators of customer-feature throughput, which is leading-indicator of revenue.
>
> If our dashboard is healthy for two consecutive quarters, you should see it in product-side metrics in quarter three. If our dashboard is healthy for three quarters and product-side metrics haven't moved, we have a different problem — the engineering throughput isn't being aimed at things that matter, which is upstream of engineering."

### "I heard [vendor / influencer] claim [N]x productivity gains. Why aren't we seeing that?"

> "Most published claims are based on benchmarks that don't translate to real engineering work, or on small studies with severe selection effects. The METR RCT — the strongest empirical work — found mid-single-digit productivity *losses* for senior engineers in their first weeks with AI tooling, before gains. Real teams in real codebases produce 15-30% gains *after* significant investment in harness and process. The vendor's 2x is essentially never replicable.
>
> If you're hearing claims that don't match what I'm telling you, send them to me directly. I'll either explain why the claim doesn't apply, or I'll update my expectations. Either is fine."

## When you don't have the data the CEO is asking for

> "I don't have that data right now. Here's what I do have, and here's what it would take to get the data you're asking for. I can [build it in N weeks / source it from vendor X for Y dollars / approximate from existing data with caveats]. Which would you prefer?"

This response works because it doesn't pretend, it offers options with costs, and it returns the decision to the CEO. CEOs respect "I don't know yet" much more than fabricated answers.

## What this explainer will NOT do

- Will not work if the dashboard isn't actually maintained. The CEO will ask for a specific data point and you'll have to admit it's stale or fictional. Build the dashboard before relying on it.
- Will not save you if the metrics are bad. If velocity is flat AND quality is degrading AND predictability is deteriorating, the dashboard is doing its job by telling you the program isn't working. Don't shoot the messenger.
- Will not work in a single conversation if the CEO is anxious. Plan for three conversations across two weeks rather than one big set-piece briefing.

## Setup before the conversation

1. **Pull the latest data.** Yes, even if the dashboard updates automatically. The CEO will ask about a specific number; you should know it cold.
2. **Annotate the trend lines.** Write 3-4 sentences per metric on what's tracking and what's lagging. Bring them on a printout, not a phone.
3. **Practice metric 3 specifically.** It's the most likely to get pushed back on. The CEO will ask "but how do you know the AI didn't introduce subtle bugs?" Have the answer ready.
4. **Decide what you'll commit to before the conversation.** If asked "what are you targeting for next quarter?" you should not be improvising.

## Companion artifacts

- `scripts/ai-readiness-audit.py` — the discipline upstream of the dashboard
- `scripts/slop-detector.py` — automated input to metric 2 quality grading
- `exec-kit/board-deck.pptx` — the slide deck that visualizes this dashboard
- Ch 31 — the source for everything in this template
