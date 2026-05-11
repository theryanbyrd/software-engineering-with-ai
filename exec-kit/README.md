# Exec Kit

Artifacts for the VP of Engineering with a board meeting in 8 weeks. Designed to be used the week before the meeting, not the week after.

Companion to [_Software Engineering with AI: A Practical Handbook for the Claude Code Era_](https://www.linkedin.com/in/ryanbyrd) by Ryan Byrd, particularly Part VIII (the Mid-Size Playbook), Chapters 51-61.

---

## What's in here

| File | Use when | Chapter |
|---|---|---|
| `90-day-plan.md` | Day 0 of your AI rollout | Ch 51 |
| `board-deck-template.pptx` | Week before your next board meeting | Ch 52 §52.1 |
| `all-hands-deck-template.pptx` | Week 2 all-hands during rollout | Ch 51 §51.3 |
| `roi-calculator.xlsx` | Defending the investment to CFO | Ch 54 §54.5 |
| `data-classification-matrix.xlsx` | Security review with customer | Ch 34, Ch 56 |
| `approved-tooling-matrix-template.xlsx` | CISO countersign at Week 1 | Ch 30 |
| `security-questionnaire-answers.md` | Customer security questionnaire arrives | Ch 56 |
| `vendor-negotiation-scripts.md` | 60-120 days before vendor renewal | Ch 54 §54.11 |
| `ceo-emails/defending-the-investment.md` | Quarterly review email | Ch 52 §52.2 |
| `ceo-emails/pushing-back-on-headcount-cut.md` | When AI is invoked to justify cuts | Ch 52 §52.3 |
| `ceo-emails/podcast-clip-reply.md` | 11pm message about an Anthropic / OpenAI / competitor announcement | Ch 52 §52.4 |

---

## Recommended order of operations

**If you're starting today:**

1. Open `90-day-plan.md` — work through Day 0 actions.
2. Open `approved-tooling-matrix-template.xlsx` — fill in your actual tools, get CISO countersign by Day 7.
3. Skim `security-questionnaire-answers.md` so you know it exists when sales asks.
4. Bookmark the three CEO email templates — you will need at least one within 60 days.

**If your board meeting is in 8 weeks:**

1. Open `90-day-plan.md` — figure out where you are vs. where the plan says you should be.
2. Open `roi-calculator.xlsx` — fill in your real numbers; produce three scenarios (conservative, base, aggressive).
3. Open `board-deck-template.pptx` — populate the four slides with your actual data.
4. Brief your CTO and run the deck by them at least 5 days before the board meeting.

**If a customer just sent an AI security questionnaire:**

1. Open `security-questionnaire-answers.md` — copy answers, customize with your actual vendor names and deployments.
2. Have your CISO review before sending.
3. If the customer asks for more detail, offer a 30-minute NDA call with your CISO on it.

**If your CEO just sent an 11pm podcast clip:**

1. Open `ceo-emails/podcast-clip-reply.md` — pick the variant that fits.
2. Send a three-sentence reply.
3. Go back to bed.
4. In the morning, decide if this is becoming a pattern that needs a calendar conversation.

---

## What's NOT in here

- **An automated dashboard.** Reference dashboards live in `../docs/measurement-dashboards/`. The exec kit is artifacts, not running infrastructure.
- **Your specific company's data.** Templates only. The whole kit is sanitized.
- **Legal advice.** Have your General Counsel review contracts and security questionnaire responses before sending to customers.
- **A guarantee that any of this works.** It's been tested at multiple mid-size companies in 2025-2026 with good results. Your situation will differ. The principles transfer; the specifics need adapting.

---

## Customization workflow

Every template has a customization checklist near the top or bottom. Before using any artifact:

1. Read the checklist.
2. Replace placeholders with actual values from your company.
3. Have the CISO/CTO/CFO review the parts that touch their domain.
4. Save your customized version in your company's docs system; keep this template clean for future use.

---

## Maintenance

These artifacts are tied to mid-2026 vendor terms, model capabilities, and industry data. They will go stale. The companion repo updates quarterly (`v2026.q3`, `v2026.q4`, ...) — when terms change materially, the templates update.

If you find a template that no longer reflects current reality (vendor terms changed, industry data shifted), open an issue at github.com/ryanbyrd/ai-engineering-handbook with the chapter reference and what's stale. Errata are tracked in `CHANGELOG.md` per release.

---

## A final note on tone

These templates are written in Ryan Byrd's voice from the book — direct, evidence-based, willing to push back, professional. When you customize them, keep that tone. The temptation when adapting is to soften the edges. Don't. The whole point is that these conversations are easier when the artifacts are direct.

The CEO will respect a direct email more than a hedged one. The board will respect a four-slide deck more than a sixteen-slide deck. The customer's CISO will respect a specific answer more than a vague one.

Send the email. Show the deck. Have the conversation.
