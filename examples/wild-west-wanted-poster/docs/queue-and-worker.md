# Queue, worker & AI vendor (Phase 6)

The generation pipeline is asynchronous: the web tier enqueues, the worker does the slow
AI work. Code in `worker/`.

## Message shapes
- Generation: `{ genId, userId, uploadKey }`.
- Cron: `{ command: 'reset-monthly' }` (sent by the EventBridge one-off task; see below).

## The worker loop (`worker/src/index.ts`)
Long-poll SQS (20s). For a generation job, call `processGeneration`; for the reset command,
call `runMonthlyReset`. Delete the message on success; on failure, leave it so SQS redelivers
and, after the redrive limit, parks it in the DLQ. A visibility-timeout heartbeat covers
slow Gemini calls so a long job isn't redelivered mid-flight. SIGTERM/SIGINT drain and exit.

## Processing a generation (`worker/src/process-generation.ts`)
`processing` → download upload from S3 → `gemini.ts` restyle → `poster.ts` composite →
upload poster → `done` → SES "ready" email. On any error: `failed` + error text + `+1
'refund'` ledger event (idempotent on genId). Writes are keyed by genId so a redelivery is
safe.

## Gemini (`worker/src/gemini.ts`)
`gemini-2.5-flash-image` via `@google/genai`. The prompt restyles the uploaded portrait as a
sepia, weathered Old-West wanted-poster mugshot. User-supplied text (their name) is passed
as poster data to `sharp`, **not** concatenated into the model prompt, so it can't steer the
model (Ch 36).

## Poster compositing (`worker/src/poster.ts`)
`sharp` lays the Gemini portrait into a parchment frame with "WANTED", "DEAD OR ALIVE", a
randomized reward, and the user's name → PNG.

## Cron
`worker/src/monthly-reset.ts` is the same image invoked with the reset command by
EventBridge Scheduler on the 1st of each month (`infra/terraform/eventbridge-cron.tf`).
