# People — JDs, Career Ladder, Interview Rubrics, Perf Reviews

The HR-adjacent artifacts for an AI-native engineering organization. Direct implementation of Chapter 60 of [_Software Engineering with AI: A Practical Handbook for the Claude Code Era_](https://www.linkedin.com/in/ryanbyrd) by Ryan Byrd, with companion material from Chapters 5, 42, and 59.

These are templates. Adapt to your company's existing rubric structure rather than wholesale-replacing what you have.

## What's in here

```
people/
├── README.md                              ← this file
├── jds/                                   ← job description templates
│   ├── senior-engineer-ai-native.md
│   ├── platform-engineer-harness.md
│   ├── engineering-manager-ai-native.md
│   ├── senior-engineer-direction.md
│   ├── senior-engineer-architecture.md
│   ├── senior-engineer-evaluation.md
│   └── _TEMPLATE.md
├── career-ladder/
│   ├── README.md                          ← how to add AI-fluent rubric items to your ladder
│   ├── ic-track-additions.md              ← IC L3-L7 with the new bottleneck disciplines
│   └── manager-track-additions.md         ← M1-M3 additions
├── interview-rubrics/
│   ├── README.md
│   ├── pr-review-exercise.md              ← live or async PR review (replaces LeetCode for senior)
│   ├── architecture-with-ai.md            ← architecture conversation rubric
│   └── harness-component.md               ← "tell me about a recent harness component you shipped"
└── perf-reviews/
    ├── README.md
    ├── harness-contribution.md            ← the new perf review section
    ├── ai-authorship-attribution.md       ← reflection prompt
    └── review-discipline.md               ← assessing reviewer quality
```

## Three changes Ch 60 recommends to your existing rubrics

These are not radical. They are extensions:

1. **Re-leveling.** L4-to-L5 promotion criteria explicitly include harness contribution. Code review judgment becomes a leveling criterion in its own right. Direction / Architecture / Evaluation depth (Ch 5 §5.2) maps onto leveling.
2. **Performance reviews.** Three new sections — harness contribution, AI authorship attribution, review discipline.
3. **Hiring updates.** Stop using LeetCode-style algorithm interviews as the sole signal for senior engineers. Add a real PR review exercise. Add an architecture-with-AI conversation. Add the "tell me about a recent harness component you shipped" question.

## What this is NOT

- **Not a comp band template.** Comp bands depend on geography, market, and company stage. The book recommends a 10-20% premium at the senior tier (Ch 60 §60.2) for engineers with 3+ years of credible AI tooling experience; the actual numbers belong in your comp committee, not in a public template.
- **Not a complete leveling rubric.** These are additions to whatever you already have, not a from-scratch ladder. Replace what's missing in your existing system; do not try to swap the whole thing.
- **Not legal advice.** JDs and perf review templates need review by your HR/legal team, especially around protected categories, accommodation language, and jurisdictional variation.

## How to use these templates

1. **Read them with your existing rubrics open.** Mark which items are additive versus changes.
2. **Run them past your most senior engineers.** If they don't recognize the signals, the templates won't predict the work.
3. **Pilot before publishing.** Use the new interview rubrics on 2-3 candidates before retiring the old ones; calibrate before scale.
4. **Update quarterly.** AI tooling moves fast. The template that worked in Q1 2026 may need adjustment by Q4. The career ladder additions in particular benefit from quarterly review.

## A note on the "AI-fluent IC track"

Ch 60 doesn't propose a separate track for AI-fluent engineers. It updates the existing IC track to recognize the new signals — harness contribution, code review judgment, depth in Direction / Architecture / Evaluation. Beware of vendors selling you a separate "AI engineer" career ladder; that path tends to ghettoize the AI-fluent engineers and create a two-tier system. The book's recommendation, encoded in these templates, is to integrate the signals into the existing ladder.

## What we will (and will not) accept as PRs to this directory

PR welcome:

- New JD templates for roles not yet covered (Solutions Engineer, Tech PM, Staff+ engineering specializations)
- Better interview rubrics, particularly anonymized examples that worked
- Calibration notes (e.g., "we tried PR review exercise X, here are the misses we caught")

PR not welcome:

- Specific company comp band numbers
- Anything that names a specific candidate
- Vendor-pitching content disguised as a rubric
- Items that contradict the book's editorial stance without explanation

— Ryan Byrd
