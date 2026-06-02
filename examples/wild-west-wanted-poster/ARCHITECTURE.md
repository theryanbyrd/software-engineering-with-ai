# Architecture — Wild West Wanted Poster

> Why the system is shaped this way. Pairs with [README.md](README.md) (the narrative) and
> [RUNBOOK.md](RUNBOOK.md) (how to stand it up).

## Request/data flow

1. **Sign in.** User submits email → `POST /api/auth/request` creates an `auth_tokens` row
   and SES sends a magic link → `GET /auth/verify?token=…` consumes it, sets a signed-JWT
   session cookie, and on first login grants 5 free credits.
2. **Generate.** `POST /api/upload` (auth required) validates the image, then in **one DB
   transaction**: checks balance ≥ 1, appends `-1 'generation'` to `credit_ledger`, inserts
   a `generations` row (`queued`), and — only after commit — uploads the original to the
   uploads bucket and sends an SQS message `{genId,userId,uploadKey}`.
3. **Process.** The worker long-polls SQS → `processing` → Gemini restyle → `sharp`
   composite → upload poster → `done`; SES emails the user. On failure: `failed` + `+1
   'refund'`.
4. **Poll.** The browser polls `GET /api/generations/[id]`; when `done`, the API returns a
   short-lived presigned URL to the poster.
5. **Buy credits.** `POST /api/checkout` → Stripe Checkout → on success Stripe calls
   `POST /api/stripe/webhook` → verify signature, dedupe on `webhook_events`, append `+10
   'purchase'`.
6. **Monthly reset.** EventBridge → one-off ECS task → grant 5 to each user for `YYYY-MM`
   (idempotent via `monthly_grants`).

## Key decisions

- **Event-sourced credits.** `credit_ledger` is append-only; balance = `SUM(delta)`.
  Mutable balance columns drift and lose history; a ledger is auditable and lets us refund
  by appending, never by editing. (Reasons: `monthly_free`, `purchase`, `generation`,
  `refund`, plus admin adjustments.)
- **Transactional spend with an advisory lock.** The check-and-debit is one transaction
  keyed by `pg_advisory_xact_lock(userId)` so concurrent uploads can't both spend the last
  credit. The SQS send is a post-commit side effect (never inside the txn).
- **Two private buckets, presigned reads.** Nothing is public. Uploads expire in 30 days;
  posters are served via presigned GET URLs minted per request.
- **Web vs worker split.** Image generation is slow and bursty; isolating it behind a queue
  keeps the web tier responsive and lets the worker scale (and fail, and retry via DLQ)
  independently.
- **Idempotency everywhere money or grants are involved.** Stripe events dedupe on
  `webhook_events.id`; monthly grants dedupe on `(user_id, period)`; refunds key on the
  generation id.
- **Secrets via Secrets Manager → ECS env.** No secrets in images or the repo.

## Failure modes & responses

| Failure | Response |
|---------|----------|
| Gemini error / timeout | generation → `failed`, credit refunded, message returns to queue → DLQ after N tries |
| Duplicate Stripe webhook | dropped via `webhook_events` idempotency |
| Concurrent uploads at balance=1 | advisory lock serializes; the second gets `402 insufficient credits` |
| Worker crash mid-job | SQS visibility timeout returns the message; generation re-processed (idempotent writes keyed by genId) |
| SES in sandbox | sign-in/notifications fail closed; RUNBOOK covers requesting production access |

## Scaling notes

Web autoscales on CPU behind the ALB. The worker scales on queue depth (add a target-
tracking policy on `ApproximateNumberOfMessagesVisible`). RDS starts small (gp3, single
-AZ) and moves to Multi-AZ + a read replica only when metrics justify it (Ch 31).
