# Worked Example — Building "Wild West Wanted Poster" from Scratch

> Companion to *Software Engineering with AI*, Chapter 47 (Worked End-to-End Examples).
> This is the full greenfield case study the book promises: a real, deployable SaaS
> built from an empty directory to production with an agent at the keyboard — domain,
> infrastructure, application, payments, AI, the lot. Every artifact referenced below
> lives in this directory.

## What we're building

**Wild West Wanted Poster** (`wildwestwanted.com`) — upload a selfie, get an
AI-generated Old-West "WANTED — DEAD OR ALIVE" poster of yourself.

- **Freemium:** 5 free generations per month.
- **Paid:** $1 buys 10 credits. 1 poster = 1 credit.
- **Surface area:** email sign-up (magic link), a one-screen generator, a buy-credits
  flow, and an admin backend for user/credit/generation management.

It is deliberately small enough to read end-to-end and complete enough to exercise every
moving part a real product has: a domain, TLS, a VPC, an application server, a database,
object storage, a queue, a background worker, transactional email, a monthly cron, a
payment vendor, and an external AI vendor. Nothing is faked or hand-waved.

## The end state

```
                         Route53 (wildwestwanted.com) ── ACM TLS
                                      │
                                   ALB :443
                                      │
        ┌─────────────────────────────▼──────────────────────────────┐
        │            ECS Fargate "web"  (Next.js 14, App Router)       │
        │  upload UI · magic-link auth · credits · Stripe checkout ·   │
        │  admin backend · /api/* route handlers                       │
        └───┬───────────────┬───────────────┬───────────────┬─────────┘
            │ write          │ enqueue        │ presign        │ verify+grant
            ▼                ▼                ▼                ▼
        RDS Postgres     SQS jobs queue     S3 (uploads,     Stripe (Checkout
        (event-sourced   ──────┐            posters)          + webhook → +10)
         credit ledger)        │
                               ▼
        ┌──────────────────────────────────────────────────────────┐
        │        ECS Fargate "worker"  (Node 20 SQS consumer)        │
        │  download upload → Gemini image → sharp poster composite → │
        │  upload poster → mark done → SES "your poster is ready"    │
        └──────────────────────────────────────────────────────────┘
                               ▲
        EventBridge Scheduler ─┘  (1st of month 00:00 UTC → grant 5 free credits)
```

Secrets live in AWS Secrets Manager and are injected into the ECS tasks as environment
variables. Images are built to ECR. Everything is provisioned by Terraform in
[`infra/terraform/`](infra/terraform/).

## How we drove the agent (the meta-layer)

This example practices what the book preaches, so the *method* is part of the artifact:

- **Agent-ready issues (Ch 19).** Each phase below started as a scoped issue with
  acceptance criteria and a test plan. The actual issues are in
  [`docs/agent-ready-issues.md`](docs/agent-ready-issues.md).
- **A single `verify` (Ch 7) and CI (Ch 8).** `tsc --noEmit` + lint for `web/` and
  `worker/`, `terraform fmt -check && validate`, and a schema-load smoke test — wired in
  [`.github/workflows/ci.yml`](.github/workflows/ci.yml).
- **Autonomy levels (Ch 32).** Application code (UI, route handlers, worker logic) was
  run at higher autonomy; anything touching money, auth, secrets, or `terraform apply`
  was gated to human review — see [`docs/cost-and-governance.md`](docs/cost-and-governance.md).
- **Repo legibility (Ch 6).** [`CLAUDE.md`](CLAUDE.md) and [`AGENTS.md`](AGENTS.md) at the
  example root tell the agent how the pieces fit, so it stops re-discovering the layout.
- **Event sourcing (the tracker pattern, reused).** Credits are an append-only ledger,
  not a mutable balance column — the same idea as the application tracker elsewhere in
  this repo. Balance is `SUM(delta)`. You can always reconstruct how a user got to zero.

## The build, phase by phase

### Phase 0 — Domain and DNS
Register `wildwestwanted.com`, delegate it to a Route53 hosted zone, and issue a
DNS-validated ACM certificate for the apex and `www`. Terraform owns the zone, the cert,
and the alias records to the ALB. Full steps (including registrar NS delegation) are in
[`docs/domain-and-dns.md`](docs/domain-and-dns.md); the resources are in
[`infra/terraform/dns.tf`](infra/terraform/dns.tf).

### Phase 1 — AWS foundation (Terraform)
A 2-AZ VPC (public + private subnets, one NAT), ECR repos for the two images, an ALB with
HTTP→HTTPS redirect, an ECS cluster, RDS Postgres in private subnets, two S3 buckets, an
SQS queue + DLQ, SES domain identity, least-privilege IAM task roles, and Secrets Manager
entries. Apply order and prerequisites are in
[`infra/terraform/README.md`](infra/terraform/README.md). The state backend (S3 + DynamoDB
lock) is in [`backend.tf`](infra/terraform/backend.tf).

### Phase 2 — Data model (Postgres)
Seven tables, defined in [`db/schema.sql`](db/schema.sql) and migrated via
[`db/migrations/`](db/migrations/): `users`, `auth_tokens`, `credit_ledger` (append-only),
`monthly_grants` (idempotency for the monthly free 5), `generations`, `payments`, and
`webhook_events` (Stripe idempotency). The credit balance is never stored — it is summed
from the ledger. See [`docs/data-model.md`](docs/data-model.md).

### Phase 3 — The application server
A single Next.js 14 app ([`web/`](web/)) serves the user UI, the admin backend, and the
JSON API as App Router route handlers. It runs as the ECS "web" service behind the ALB.
DB access is a shared `pg` pool ([`web/lib/db.ts`](web/lib/db.ts)); sessions are signed
JWTs in an HttpOnly cookie ([`web/lib/auth.ts`](web/lib/auth.ts)).

### Phase 4 — Freemium and credits
[`web/lib/credits.ts`](web/lib/credits.ts) implements the rules: `getBalance` sums the
ledger; `spendOneCredit` runs inside a transaction with an advisory lock so two
simultaneous uploads can't overspend the last credit; purchases and monthly grants append
positive deltas. First sign-up grants 5 credits. See [`docs/freemium-credits.md`](docs/freemium-credits.md).

### Phase 5 — Uploads and S3
`POST /api/upload` validates the file (type/size with zod), spends a credit in the same
transaction that creates the `generations` row, stores the original to the private uploads
bucket, and enqueues the job. Posters are written to a second private bucket and served to
the browser via short-lived presigned URLs ([`web/lib/s3.ts`](web/lib/s3.ts)). Raw uploads
expire after 30 days via an S3 lifecycle rule.

### Phase 6 — Queue, worker, and the AI vendor (Gemini)
The worker ([`worker/`](worker/)) long-polls SQS. For each job it marks the generation
`processing`, downloads the upload, calls **Gemini** (`gemini-2.5-flash-image` via
`@google/genai`) to restyle the portrait as a sepia Old-West mugshot
([`worker/src/gemini.ts`](worker/src/gemini.ts)), composites the "WANTED / DEAD OR ALIVE /
$REWARD" frame with `sharp` ([`worker/src/poster.ts`](worker/src/poster.ts)), uploads the
result, marks it `done`, and emails the user. If anything fails, it marks the generation
`failed` and **refunds the credit** (an append `+1 'refund'` to the ledger) — failures are
on us, not the customer. See [`docs/queue-and-worker.md`](docs/queue-and-worker.md).

### Phase 7 — Email (SES)
SES sends two things: the magic-link sign-in email and the "your poster is ready"
notification ([`web/lib/ses.ts`](web/lib/ses.ts), [`worker/src/ses.ts`](worker/src/ses.ts)).
The SES domain identity, DKIM, and a custom MAIL FROM are provisioned in
[`infra/terraform/ses.tf`](infra/terraform/ses.tf). Production access (out of the SES
sandbox) is a manual AWS request — noted in [`RUNBOOK.md`](RUNBOOK.md).

### Phase 8 — Payments (Stripe)
"Buy 10 credits for $1" creates a Stripe Checkout session
([`web/app/api/checkout/route.ts`](web/app/api/checkout/route.ts)). On
`checkout.session.completed`, the webhook
([`web/app/api/stripe/webhook/route.ts`](web/app/api/stripe/webhook/route.ts)) verifies the
signature, dedupes on `webhook_events`, records the payment, and appends `+10 'purchase'`
to the ledger. The webhook reads the **raw** request body for signature verification — a
classic footgun the book's prompt-injection/untrusted-input discipline flags. See
[`docs/stripe.md`](docs/stripe.md).

### Phase 9 — Cronjobs (monthly reset)
EventBridge Scheduler fires on the 1st of each month and runs a one-off ECS task — the
worker image with a `reset-monthly` command
([`worker/src/monthly-reset.ts`](worker/src/monthly-reset.ts)). It grants each user 5 free
credits for the current `YYYY-MM`, idempotent via `monthly_grants` so a retry never
double-grants. Defined in [`infra/terraform/eventbridge-cron.tf`](infra/terraform/eventbridge-cron.tf).

### Phase 10 — Admin backend
[`web/app/admin/`](web/app/admin/) is gated by `requireAdmin` (allow-list via
`ADMIN_EMAILS`). It shows totals (users, generations by status, credits issued vs spent,
recent sign-ups) and supports manual credit adjustments — every adjustment is itself a
ledger event with a reason, so the audit trail stays intact.

## Security and governance

- **Untrusted input is everywhere.** Uploaded images and the user's display name flow into
  the AI prompt and the rendered poster. The worker treats them as data, never
  instructions, and the prompt is constructed so user text can't redirect the model
  (Ch 36). File type/size are validated before anything touches S3 or Gemini.
- **Secrets never live in the repo** (Ch 34). `.env.example` documents names only; real
  values come from Secrets Manager via the ECS task definition.
- **Least privilege** (Ch 32–35). The web task role can presign its buckets and enqueue;
  the worker role can read uploads, write posters, send SES, and read its secrets — and
  nothing else.
- **Money and migrations are human-gated.** The credit math, the Stripe webhook, and every
  `terraform apply` were reviewed by a person. This is exactly the Do-Not-Automate posture
  from Ch 33.

## Cost discipline (unit economics)

The whole point of the freemium meter is that inference isn't free. Rough per-poster
economics (label: **[projection]**, in the spirit of the book's number discipline — plug
in current vendor prices before quoting these):

| Item | Approx. |
|------|---------|
| Gemini image generation, 1 poster | ~$0.03–0.05 |
| S3 + data transfer (1 upload + 1 poster) | < $0.001 |
| Fargate/RDS/ALB amortized per poster (at modest volume) | a few tenths of a cent |
| **Marginal cost / poster** | **~$0.04** |
| **Revenue / paid credit** ($1 ÷ 10) | **$0.10** |

So paid credits carry a healthy margin and the 5 free monthly posters are the customer
-acquisition cost — capped, predictable, and exactly the kind of line item Ch 29 tells you
to put a meter on before you ship. The DLQ + credit-refund-on-failure also means a Gemini
outage costs you retries, not angry customers.

## Repo map

```
wild-west-wanted-poster/
├── README.md                 ← this chapter
├── ARCHITECTURE.md           ← diagram, data flow, the decisions and why
├── RUNBOOK.md                ← deploy & operate, step by step
├── CLAUDE.md / AGENTS.md     ← repo legibility for the agent
├── .env.example              ← every env var (names only)
├── docs/                     ← per-topic deep dives + the agent-ready issues used
├── infra/terraform/          ← the entire AWS footprint (18 .tf files + README)
├── db/                       ← schema.sql + migrations + data-model notes
├── web/                      ← Next.js app (UI, API, admin, auth, Stripe)
└── worker/                   ← SQS consumer (Gemini, poster compositing, SES, cron)
```

## Takeaways

1. **A small product still has every part of a big one.** The value of a worked example is
   that it forces the boring, load-bearing pieces — DNS, IAM, idempotency, refunds — that
   tutorials skip and production punishes.
2. **The harness did the heavy lifting; the human owned the seams.** Agent-ready issues +
   a verify command + tight autonomy on money/secrets is the whole method.
3. **Event-source the thing people will argue about.** Credits are money-adjacent; an
   append-only ledger means every balance is explainable and every bug is recoverable.
4. **Meter the vendor before you ship.** Know your cost per AI call and put a credit system
   in front of it on day one, not after the first surprise invoice.

*Build it from [`RUNBOOK.md`](RUNBOOK.md). Read why it's shaped this way in
[`ARCHITECTURE.md`](ARCHITECTURE.md).*
