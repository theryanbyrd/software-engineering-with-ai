# Customer-Facing AI Disclosure Templates

The customer-comm templates for the questions enterprise customers will ask about your AI tooling. Direct implementation of Ch 31 §31.6 (the attribution toolkit) and Ch 41 (governance and disclosure) of [_Software Engineering with AI: A Practical Handbook for the Claude Code Era_](https://www.linkedin.com/in/ryanbyrd) by Ryan Byrd.

## What's in here

| File | Purpose |
|---|---|
| [`security-questionnaire-answers.md`](security-questionnaire-answers.md) | Comprehensive answers to the AI-tooling questions on security questionnaires (more comprehensive than the executive-strategic-kit version) |
| [`status-page-language.md`](status-page-language.md) | Customer status page language for incidents involving AI-authored code, with examples |
| [`ai-authorship-disclosure-tos.md`](ai-authorship-disclosure-tos.md) | AI authorship disclosure language for customer contracts and ToS |
| [`customer-conversation-scripts.md`](customer-conversation-scripts.md) | Verbatim openers for the conversations with customers' technical buyers and security teams |
| [`disclosure-decision-framework.md`](disclosure-decision-framework.md) | When to disclose, when to not disclose unprompted, and the tradeoffs |

## The book's stance

Per Ch 31 §31.6:

> Most "AI productivity" claims cannot be defended because they were never measured against a control. This section is the credible toolkit: an A/B framework, a PR authorship convention, and the leading indicators for quality decay.

Per Ch 41 (governance):

> Engineers don't have full visibility into AI tooling decisions made at the org level. The disclosure work — to your customers, to your regulators, to your auditors — has to be done at the leadership level with the data the dashboard provides.

The templates here translate the internal discipline (PR tagging, six metrics, the slop-detector) into customer-facing language. The customer doesn't care about your internal CLAUDE.md; they care about whether their data is safe, whether your code is reliable, whether they can trust your delivery.

## When customers ask, why

Three pressures driving customer-side AI scrutiny in 2026:

1. **Their own security teams are asking.** Enterprise customers have been doing AI risk assessments for ~18 months. They have questionnaires; they expect answers.
2. **Their own auditors are asking.** SOC 2 Type II audits now ask about AI usage in code production. Public companies have material disclosures.
3. **Their own customers are asking.** B2B SaaS customers are asking THEIR vendors. The pressure cascades.

The result: even if YOUR customers haven't asked yet, they will within 6-12 months. Be ready.

## Editorial stance — disclosure is the durable position

The templates here lean toward disclosure rather than evasion. Reasoning:

- **Disclosure is hard to undo.** If you commit to disclosing AI authorship and later try to walk it back, customers notice. If you start with non-disclosure and later want to disclose, that's also hard. Pick the durable position; lean toward openness.
- **Customers respect honesty more than perfection.** "We use AI tooling extensively; here's our governance discipline" lands better than "we don't disclose our development methodology."
- **The competitor will disclose.** Even if you wait, your competitors will use AI tooling and disclose. Customers will calibrate against the disclosing competitor.
- **Audit trails matter.** SOC 2 audits, regulatory inquiries, and legal disputes will eventually surface what your codebase looks like. Better to have the disclosure language consistent with reality.

The templates support different levels of disclosure for different contexts. The default lean is toward more disclosure rather than less.

## Who this is for

- VP of Engineering or CTO answering enterprise customer questions
- Customer Success or Solutions Engineering teams handling questionnaires
- Security and compliance leads supporting customer audits
- Legal counsel reviewing customer contracts
- Marketing and communications leads writing public-facing language

## Read first

- Ch 31 §31.6 — the attribution toolkit (PR tagging, six quality decay signals)
- Ch 38 — the procurement side (what your vendors are agreeing to with you)
- Ch 41 — the broader governance context
- `executive-strategic-kit/security-questionnaire-answers.md` — the original (more abbreviated) version of the questionnaire answers
- `incident-postmortem-templates/` — the source of incident-related disclosure language
- `vendor-procurement-runbook/` — the inverse: when YOU'RE the customer evaluating vendors

## What these templates WILL do

- Give you ready language for the questions you'll get
- Calibrate the disclosure level to context (enterprise customer questionnaire vs. consumer-facing ToS vs. SOC 2 audit)
- Build consistency: the same answers across customers, audit, and legal
- Surface the gaps in your disclosure posture before a customer surfaces them

## What these templates will NOT do

- Will not work without legal review. Customer-facing language has legal implications; templates are starting points.
- Will not protect you from misrepresenting your actual practices. If you say "AI is used in 30% of our code" but it's really 80%, that's worse than disclosing 80% honestly.
- Will not eliminate customer concern. Some customers will pull back regardless of your disclosure quality. The templates minimize the unnecessary loss; they don't eliminate the legitimate one.
- Will not work in regulated industries (healthcare, defense, finance) without specialized counsel. The templates are calibrated to general B2B SaaS.

## Companion artifacts

- `executive-strategic-kit/security-questionnaire-answers.md` — abbreviated version
- `incident-postmortem-templates/` — incident response templates
- `vendor-procurement-runbook/` — inverse perspective
- Ch 31 §31.6, Ch 41 — sources
