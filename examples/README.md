# examples/ — Working repos that use the kit

This directory is reserved for fully-working example repositories that exercise the harness end-to-end. The current canonical "working examples" are the starter kits in [`../starter-kits/`](../starter-kits/), which are intentionally minimal but fork-ready.

## Available now

- **[`wild-west-wanted-poster/`](wild-west-wanted-poster/) — a complete greenfield SaaS, built from scratch.** Upload a photo → AI Old-West wanted poster; freemium (5 free/month, $1 = 10 credits). It exercises every load-bearing part of a real product: domain + DNS, Terraform/AWS (VPC, ECS Fargate, RDS Postgres, S3, SQS, SES, Secrets Manager, EventBridge cron), a Next.js app, a queue worker, Stripe payments, and Gemini image generation — with an event-sourced credit ledger and human-gated money/secrets. Start at its [`README.md`](wild-west-wanted-poster/README.md) (the worked-example chapter for Ch 47).

Other longer-form examples (a real bug fix, a refactor, an incident response) are forthcoming. If you have an anonymizable working example to contribute, see [`../CONTRIBUTING.md`](../CONTRIBUTING.md).

## Shipped

| Example | What it demonstrates | Status |
|---|---|---|
| [`wild-west-wanted-poster/`](wild-west-wanted-poster/) | Full greenfield SaaS from scratch: domain, Terraform/AWS, app, queue/worker, Stripe, Gemini, admin, freemium | **shipped** |

## Planned examples

| Example | What it demonstrates | Status |
|---|---|---|
| `bug-fix-walkthrough/` | Full lifecycle of a Tier-2 bug fix through the harness | forthcoming |
| `refactor-walkthrough/` | Strangler-pattern refactor of a legacy module | forthcoming |
| `incident-response-walkthrough/` | Sev-2 with AI-assisted triage and postmortem | forthcoming |
| `migration-walkthrough/` | Cursor → Claude Code migration over two weeks | forthcoming |
