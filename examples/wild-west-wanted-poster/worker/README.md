# Worker — Wild West Wanted Poster (wwwp)

A Node 20 + TypeScript **long-poll SQS consumer**. It turns an uploaded portrait into an
Old-West "WANTED" poster and handles the monthly free-credit reset. It runs as its own ECS
Fargate service, separate from the web app.

## What it does

The worker pulls messages off the SQS generation queue (`SQS_QUEUE_URL`) and dispatches by kind:

1. **Generation job** — `{ "genId": "...", "userId": "...", "uploadKey": "..." }`
   - mark `generations.status = 'processing'`
   - download the original portrait from `S3_UPLOAD_BUCKET`
   - call Gemini (`gemini-2.5-flash-image`) to render a sepia Old-West portrait
   - composite the WANTED frame with `sharp` (parchment, "WANTED", "DEAD OR ALIVE", random reward, name)
   - upload the poster PNG to `S3_POSTER_BUCKET`
   - mark `status = 'done'` and send a "poster ready" email via SES
   - **on any failure**: mark `status = 'failed'` with the error AND append a `+1 'refund'`
     credit-ledger event so the user isn't charged for our mistake. The message is left on the
     queue, so SQS redelivers and eventually routes it to the DLQ after `maxReceiveCount`.

2. **Monthly reset** — `{ "command": "reset-monthly" }` (sent by EventBridge Scheduler)
   - grant 5 free credits to every user for the current `'YYYY-MM'`, idempotently via
     `monthly_grants` + a `+5 'monthly_free'` ledger event.

## Files

| File                      | Responsibility                                                      |
|---------------------------|---------------------------------------------------------------------|
| `src/index.ts`            | SQS poll loop, message dispatch, visibility heartbeat, shutdown.    |
| `src/process-generation.ts` | One job end-to-end (the saga) + refund-on-failure.                |
| `src/monthly-reset.ts`    | Idempotent monthly free-credit grant; also runs as a one-shot task. |
| `src/gemini.ts`           | Portrait -> sepia wanted-poster portrait via `@google/genai`.       |
| `src/poster.ts`           | `sharp` compositing of the final poster PNG.                        |
| `src/db.ts`               | `pg` pool + transaction + event-sourced ledger helpers.             |
| `src/s3.ts`               | Download uploads / upload posters.                                  |
| `src/ses.ts`              | Transactional email (poster-ready).                                 |

## Run locally

```bash
cp .env.example .env   # fill in real values (DATABASE_URL, AWS_*, GEMINI_API_KEY, ...)
npm install
npm run dev            # tsx watch src/index.ts — long-polls SQS

# One-shot monthly reset (what EventBridge triggers, runnable by hand):
npm run reset-monthly
```

Typecheck / build:

```bash
npm run typecheck      # tsc --noEmit
npm run build          # emits dist/
```

Container:

```bash
docker build -t wwwp-worker .
docker run --env-file .env wwwp-worker
```

The Dockerfile is multi-stage on `node:20-alpine` and installs `vips` so `sharp` works at runtime.

## Required environment

See `.env.example`. Names match the shared conventions exactly: `DATABASE_URL`, `APP_URL`,
`AWS_REGION`, `S3_UPLOAD_BUCKET`, `S3_POSTER_BUCKET`, `SQS_QUEUE_URL`, `SES_FROM_EMAIL`,
`GEMINI_API_KEY`, `AUTH_SECRET`, `ADMIN_EMAILS`. Stripe vars are not used by the worker.

## How it maps to the book

- **Queue / worker chapter** — `index.ts` is the canonical long-poll consumer: receive, dispatch,
  delete-on-success, redeliver/DLQ-on-failure, graceful shutdown, and visibility extension for
  slow third-party calls.
- **Cost discipline chapter** — the expensive Gemini call lives behind the queue (never in a user
  request), 1 image = 1 credit, free tier is metered by `monthly_grants`, and failed jobs **refund**
  the credit. The event-sourced `credit_ledger` makes every cent auditable.
- **Event sourcing chapter** — balances are derived from `credit_ledger`; spends, grants, purchases,
  and refunds are all append-only events.
