# Vendor Procurement Runbook for AI Tools

The procurement playbook for AI vendor selection, security review, and contract negotiation. Direct implementation of Chapter 38 of [_Software Engineering with AI: A Practical Handbook for the Claude Code Era_](https://www.linkedin.com/in/ryanbyrd) by Ryan Byrd.

## What's in here

| File | Purpose |
|---|---|
| [`security-review-template.md`](security-review-template.md) | The structured security review every AI vendor goes through before procurement |
| [`data-classification-walkthrough.md`](data-classification-walkthrough.md) | How to use the data classification matrix to determine which AI tools are approved for which data classes |
| [`contract-terms-negotiation-script.md`](contract-terms-negotiation-script.md) | Verbatim language for negotiating data retention, model training opt-out, breach notification, and exit terms |
| [`things-vendors-wont-put-in-writing.md`](things-vendors-wont-put-in-writing.md) | The asks vendors will agree to verbally and refuse on paper — and how to handle |
| [`procurement-checklist.md`](procurement-checklist.md) | The 21-item gate before signing |
| [`renewal-discipline.md`](renewal-discipline.md) | What to re-verify on every renewal — vendors change terms |

## The book's stance

> The questions to ask before signing any AI tool contract. Anything where the answer is "we don't disclose that" is a finding.
>
> — Ch 38 opening

Procurement for AI tools is qualitatively different from procurement for other SaaS:

- The data flowing through is your code (often your most sensitive asset)
- Training-on-customer-data is a real concern with significant precedent of vendor changes
- Model and tokenizer changes can cost you 30%+ token volume overnight
- The market is moving fast; long-term contracts have asymmetric risk

The runbook here is the discipline that protects you from these risks.

## Who this is for

- VP of Engineering or CTO making vendor decisions
- Security / compliance lead reviewing AI tools
- Procurement / Finance lead negotiating contracts
- Platform team lead implementing approved tooling matrix

## Read first

- Ch 38 — vendor risk and procurement (the source)
- Ch 41 — data classification context
- `exec-kit/data-classification-matrix.xlsx` — the company-side framework
- `exec-kit/approved-tooling-matrix-template.xlsx` — the operational matrix
- `migration-playbooks/shadow-ai-to-approved-stack.md` — the cleanup playbook the procurement work prevents needing

## What this runbook WILL do

- Surface the questions that protect you legally and operationally
- Give you specific contract language for the asks that matter
- Calibrate which vendor claims are durable vs. fluff
- Build the institutional discipline that handles year-2 surprises

## What this runbook will NOT do

- Will not eliminate vendor risk. AI vendors are early-stage; surprises happen.
- Will not work without legal counsel. The runbook is the engineering / security side; legal owns the contract.
- Will not produce one-size-fits-all answers. Regulated industries (healthcare, finance, defense) have additional requirements.
- Will not work without engaged procurement. If procurement signs without engineering review, the runbook is bypassed.

## Order of operations

1. **Security review** — [`security-review-template.md`](security-review-template.md). Run this before any contract conversation.
2. **Data classification** — [`data-classification-walkthrough.md`](data-classification-walkthrough.md). Determine which data classes the tool can be approved for.
3. **Contract negotiation** — [`contract-terms-negotiation-script.md`](contract-terms-negotiation-script.md). With the security review and data classification as input.
4. **Watch for the verbal-only asks** — [`things-vendors-wont-put-in-writing.md`](things-vendors-wont-put-in-writing.md). Test their commitment by asking for paper.
5. **Final gate** — [`procurement-checklist.md`](procurement-checklist.md). 21 items.
6. **Sign and document.**
7. **Renewal discipline** — [`renewal-discipline.md`](renewal-discipline.md). Set the calendar reminder for 60 days before renewal.

## Companion artifacts

- `exec-kit/data-classification-matrix.xlsx`
- `exec-kit/approved-tooling-matrix-template.xlsx`
- `exec-kit/security-questionnaire-answers.md` — the questionnaire you'll be asked to answer (and that you'll ask of vendors)
- Ch 38 — the source
- Ch 41 — adjacent compliance context
