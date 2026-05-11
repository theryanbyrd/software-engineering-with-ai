# Skip-Level Defense

Templates for the conversations when a CEO, CTO, or board member is asking pointed questions about the AI program. Direct implementation of Chapter 61 of [_Software Engineering with AI: A Practical Handbook for the Claude Code Era_](https://www.linkedin.com/in/ryanbyrd) by Ryan Byrd, with the metrics framing from Ch 31 §31.1 and the briefing discipline from Ch 52 §52.6.

## What's in here

| Template | When to use |
|---|---|
| [`six-metric-dashboard-explainer.md`](six-metric-dashboard-explainer.md) | The CEO asks "what are we measuring and why?" The board wants the metrics page. Your first 10 minutes with a new CTO. |
| [`no-the-model-release-didnt-change-our-strategy.md`](no-the-model-release-didnt-change-our-strategy.md) | A frontier model dropped this week. Your CEO sent you the launch tweet at 11pm. The team is asking whether the roadmap changes. |
| [`productivity-plateau-message.md`](productivity-plateau-message.md) | Quarterly review. Velocity is flat or up only modestly. The CEO had been told "AI will 2x productivity." This is the conversation that doesn't get you fired. |
| [`we-are-not-pivoting-all-hands.md`](we-are-not-pivoting-all-hands.md) | A competitor just announced something flashy. Your team is anxious. Your CEO is anxious. The board is asking. The all-hands message that holds the line. |
| [`hostile-skip-level-recognition.md`](hostile-skip-level-recognition.md) | Recognizing the four signals from Ch 61 §61.4 and the script for the one-on-one to address it. |
| [`brief-your-reports.md`](brief-your-reports.md) | Pre-skip-level briefing for your EMs and senior staff: what to say, what NOT to say, the debrief discipline. |

## The book's stance

> The political reality of running engineering in 2026 is that your CEO has more questions than you have time to answer, more anxiety than your data can dispel, and a podcast feed full of people promising things you cannot deliver.
>
> — Ch 61 opening

The templates here are not for ordinary status updates. They're for the conversations where the CEO's anxiety is the actual problem and the data is the tool you use to manage it. Every template assumes:

1. You have the dashboard in working order. Without it, the templates don't land.
2. You have established credibility before the conversation. Templates don't substitute for trust.
3. You are willing to be specific. Vague answers compound CEO anxiety; specific answers reduce it.

## Read first

- Ch 31 — The six metrics. The dashboard is the foundation. Without it, no defense holds.
- Ch 52 §52.6 — Briefing reports for skip-levels. The discipline before the conversation.
- Ch 61 — The skip-level chapter itself. Templates here are operational; the chapter is the strategic frame.

## How to use

These are templates, not scripts. Adapt to your voice, your CEO's communication style, and your specific data. The structure and the order of points are what carries; the verbatim language is example only.

**Read the relevant template before the conversation, not during.** Templates work because they let you anchor on the right structure under pressure. Reading from one in real time makes you sound like you're reading from one.

**Use the dashboard, even if you have to fake-it-til-you-make-it.** A CEO who is shown specific trend lines on six metrics calms down meaningfully even before evaluating the trends. The act of showing the dashboard says "I have this under control" more than the data does.

**Don't escalate prematurely.** Most political friction is absorbable per Ch 61 §61.5. Escalation is a tool, not a default.

## What these templates will NOT do

- Will not save you in a culture where the CEO's relationship to engineering is fundamentally hostile. Templates are for normal political friction in a healthy company.
- Will not work if your dashboard is fictional. CEOs notice when the metrics are window dressing.
- Will not substitute for the Direction / Architecture / Evaluation discipline your team is or isn't doing. The defense templates work because the underlying work is real.
- Will not help with personal-comp conversations, performance management of an EM, or board-level legal/compliance issues. Different domains.

## Companion artifacts

- `exec-kit/board-deck.pptx` — the four-slide quarterly board update
- `exec-kit/ceo-emails/` — written templates for non-skip-level executive comms
- `migration-playbooks/team-conversation-scripts.md` — overlap with §1 (pushing back on compressed timelines) and §6 (holding the line mid-migration)
- `war-stories/` — the failure modes the templates here prevent
