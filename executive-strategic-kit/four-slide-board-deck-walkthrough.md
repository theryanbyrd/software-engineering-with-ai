# Four-Slide Board Deck Walkthrough

What each slide should say, what NOT to add. Per Ch 52 §52.1:

> Resist the urge to add slides. The board does not want more detail. The board wants confidence that you have a clear plan and honest numbers.

This file is the substance behind `exec-kit/board-deck-template.pptx`. The template gives you the shell; this gives you what to put in it.

## The four slides

### Slide 1 — Posture

**What goes on the slide.** One sentence stating the company's AI posture. Per Ch 52 §52.1:

> "We are pursuing investment posture: we will add AI capacity on top of current headcount, expecting throughput up and quality flat-to-rising, with a six-month review against named metrics."

**Adapt to your company's actual posture.** Three common postures:

#### Investment posture (most common)

> "We are pursuing investment posture: we add AI capacity on top of current engineering headcount. The expectation is throughput up, quality flat-to-rising, with a six-month review against named metrics."

This is the default. Most companies in 2026 are here.

#### Substitution posture (uncommon, sometimes appropriate)

> "We are pursuing substitution posture: we are reducing engineering headcount by N% in the year, with AI tooling absorbing the work. Throughput is held flat; quality is the primary measurement; review at twelve months."

Companies with hard cost pressure choose this. Be explicit that throughput is held flat — substitution + acceleration is the incoherent posture (per [`hype-rebuttal-table.md`](hype-rebuttal-table.md) hype claim 1).

#### Discovery posture (uncommon, narrow situations)

> "We are pursuing discovery posture: we are evaluating AI tooling against three specific work types over the next 90 days. Headcount and throughput targets are unchanged. Decision points at the end of each 30-day cycle."

Early-stage companies or specific situations where the data isn't yet available to commit.

**Why one sentence.** The board has 30 seconds for this slide. They need to leave knowing the company's posture, full stop.

**What NOT to add to slide 1:**
- Detailed strategy
- Multiple postures listed for evaluation
- Conditional language ("we will probably ...")
- Vendor names
- Dollar figures (those are slide 2)

### Slide 2 — Investment

**What goes on the slide.** Four lines:

1. The committed dollar figure for the year (or quarter, depending on cadence)
2. The named outcomes the investment is committing to
3. The named owner
4. The review cadence

**Example:**

> **Investment**
> 
> - $1.4M annual: $900K Anthropic + $200K platform team headcount + $300K training and tooling
> - Named outcomes: 12% throughput gain on tier-2 work over 12 months; quality flat or rising; cost in budget
> - Owner: VP of Engineering
> - Review: quarterly with the board; monthly internal

**Why these specifics.**

- **Dollar figure** — the board is approving money; they need to see what they're approving.
- **Named outcomes** — this is what the dollar figure is buying. Per [`realistic-roi-message.md`](realistic-roi-message.md).
- **Named owner** — accountability has a face. Often the VPE; sometimes the CTO; sometimes a specific platform lead.
- **Review cadence** — when the board will see progress. Quarterly is standard.

**What NOT to add to slide 2:**
- Detailed cost breakdowns by team or by tool
- Vendor pricing tables
- Comparison to competitors' spend
- ROI ratios with three significant figures

The board doesn't want the spreadsheet on the slide. They want the headline figure and the commitment. The spreadsheet is in the appendix or in a follow-up.

### Slide 3 — Metrics

**What goes on the slide.** The six-metric dashboard from Ch 31, with **trend lines, not point-in-time numbers**. Per Ch 52 §52.1:

> Trend lines, not point-in-time numbers. Annotations on what's tracking and what's lagging.

**Example layout:**

| Metric | Last quarter | This quarter | 12-month target | Status |
|---|---|---|---|---|
| Adoption (% active in 7 days) | 65% | 78% | 90% | On track |
| Throughput (lead time, days) | 4.2 | 3.7 | 3.0 | On track |
| Quality (features-to-bugs ratio) | 4.1 | 4.3 | 4.5 | On track |
| Maturity (LLM-graded score) | 6.2 | 6.5 | 7.0 | On track |
| Predictability (1 − σ/μ) | 0.78 | 0.82 | 0.85 | On track |
| Cost (per active dev/month) | $185 | $190 | $150-250 | Within range |

(The actual deck slide is sparklines, not a table — visual.)

**Why trend, not point-in-time.** The board needs to see direction, not just a number. A point-in-time of 12% throughput gain doesn't tell them whether it's heading to 15% or 8%. The trend tells them.

**Annotations.** "What's tracking" and "what's lagging" — explicit. Don't make the board figure out which trend is good and which is bad.

**What NOT to add to slide 3:**
- All seven metrics (the seventh is the failed-one-shot triage ratio per Ch 31 §31.5; that's an internal metric, not a board metric)
- Detailed cuts by team (those are in the platform team's internal dashboard)
- Industry comparisons in detail (one annotation is fine; a table isn't)
- Acceptance rate, lines of code, token usage per individual — these are explicitly NOT to measure per Ch 31 §31.2

### Slide 4 — Risks

**What goes on the slide.** Three to five named risks with named mitigations. Per Ch 52 §52.1:

> Include at least one external risk (vendor terms change) and one internal (autonomy drift).

**Example:**

| Risk | Mitigation |
|---|---|
| Vendor pricing or terms change | Quarterly model lineup review; no long-term contracts; routing flexibility documented |
| Autonomy drift (agents doing more than approved) | Tier-1 do-not-automate catalog; CODEOWNERS gates; monthly autonomy audit |
| Quality decay under throughput pressure | Six leading indicators monitored monthly per Ch 31 §31.6 |
| Reviewer burnout (single point of failure) | Six mitigations from Ch 44 §44.5 in implementation; tracked quarterly |
| Regulatory change (EU AI Act, US sectoral regulation) | Legal review quarterly; data classification matrix maintained |

**Why these specifics.**

- **Named risks** — the board cannot help with vague risks. Specific risks invite specific board engagement.
- **Named mitigations** — for each risk, what we're doing. Not "we are aware of this" but "here is the operational response."
- **External + internal** — both. Pure external risks make the board feel powerless. Pure internal risks make the board worry about execution.

**What NOT to add to slide 4:**
- Risks you haven't operationalized a mitigation for
- Risks that are actually opportunities ("AI moves so fast we can't keep up" is not a risk; it's an industry observation)
- Risks the board can't act on
- Generic risks ("AI might be over-hyped") without specific mitigation

## What NOT to add to the deck overall

Per Ch 52 §52.1: "Resist the urge to add slides."

Specific things engineers want to add but shouldn't:

- **Vendor architecture diagrams** — the board doesn't read architecture
- **Detailed competitor comparisons** — usually leads to board members asking why competitor X chose differently; opens debates that don't help
- **Token usage breakdowns** — operational; not board-level
- **Engineering org charts** — the board sees these elsewhere
- **Roadmaps with dates beyond the next quarter** — speculative; commits you to specifics
- **Slides explaining what an LLM is** — patronizing; the board has been on Twitter
- **A "what we learned" slide** — the metrics slide is the learning; explicit "we learned" is awkward

If you find yourself wanting to add a fifth slide, ask: what question is this slide answering? If the question isn't on the board's mind, the slide is wasted.

## Pre-meeting preparation

Per Ch 52 §52.7:

> Templates are tools. Adapt to voice, do not skip them.

Before the meeting:

1. **Pre-brief the CEO** — the deck should not be a surprise. The CEO sees it 3-5 days ahead; you incorporate their feedback.
2. **Pre-brief any board members who have specific interest** — typically a board member with engineering background, or one who has been vocal on AI questions.
3. **Pre-brief your own engineering leadership** — your direct reports should see the deck before the board does. They might be in the meeting; they will definitely be talking about it after.
4. **Validate the metrics with the platform team** — make sure every number on slide 3 is defensible.
5. **Read the deck aloud once** — does it tell a coherent story? If you stumble, the slide needs work.

## In-meeting delivery

Five minutes for the deck. Five minutes for Q&A. Maybe ten minutes if the board wants to engage substantively.

Common board questions:
- "What if we doubled the investment?" (Anchor: throughput gain isn't linear in investment; current commitment is calibrated.)
- "What are competitors doing?" (Anchor: most competitors are at similar postures; the visible 50% cuts are usually marketing.)
- "What's the worst case?" (Anchor: slide 4. The risks and mitigations.)
- "How confident are you?" (Anchor: the metrics. "Three of six are tracking; two are early; one is showing concerning signal — here's what we're doing about it.")

Don't oversell. Don't undersell. The board respects calibrated confidence.

## After the meeting

- **Follow up within 24 hours** with the deck PDF and a one-paragraph email summarizing what was discussed and what was committed.
- **Adjust the operational plan** if the board surfaced a concern that requires action.
- **Update the deck for next quarter** — based on what landed and what didn't.

## Anti-patterns

### The 30-slide deck

A VPE produces a 30-slide deck because "the board needs to see everything." The board reads slides 1, 4, 30. The middle is wasted; the discussion is stunted.

Mitigation: stay disciplined at four slides. Appendix slides exist if the board asks; they aren't presented.

### The hype deck

A VPE produces a deck full of "AI is transforming everything" framing. The board members who have done their homework recognize the hype; trust erodes.

Mitigation: per Ch 46, push back on hype with evidence. Even in the board context.

### The defensive deck

A VPE produces a deck that's mostly "here's why this is hard" without the trajectory. The board reads it as the VPE making excuses.

Mitigation: the metrics slide shows direction. The risks slide shows ownership. Defensive isn't the right register.

### The deck that contradicts the dashboard

The board deck shows numbers that don't match the operational dashboard. A board member who has access to both notices.

Mitigation: per `metrics-and-measurement-infrastructure/`, the dashboard is the source of truth. The deck is a view of the dashboard.

### The deck that's been the same for four quarters

The same deck, different numbers. Board members perceive lack of strategic evolution.

Mitigation: the four-slide structure is durable; the substance evolves. Each quarter, what's new (a model release, a posture shift, a risk that emerged, a mitigation that worked) shows up.

## Companion artifacts

- [`realistic-roi-message.md`](realistic-roi-message.md) — slide 2 substance
- [`what-number-do-i-commit-to.md`](what-number-do-i-commit-to.md) — slide 2 numbers
- [`hype-rebuttal-table.md`](hype-rebuttal-table.md) — for board questions about hype
- [`worked-examples-as-case-studies.md`](worked-examples-as-case-studies.md) — for board questions about concreteness
- `exec-kit/board-deck-template.pptx` — the operational template
- `metrics-and-measurement-infrastructure/reference-executive-dashboard.md` — the dashboard slide 3 references
- Ch 52 §52.1 — source
