# The agent-ready issues used to build this (Ch 19)

Each phase was delegated as a scoped issue with acceptance criteria and a test plan, in the
shape from Chapter 19 / Appendix C. Abridged versions:

## #1 — Postgres data model
**Context:** Need the schema for users, event-sourced credits, generations, payments.
**Acceptance:** `db/schema.sql` creates all 7 tables; `credit_ledger` append-only; balance
= SUM(delta); indexes on `credit_ledger(user_id)` and `generations(user_id,status)`;
migrations apply cleanly against postgres:16. **Out of scope:** app code.

## #2 — Auth via SES magic link
**Acceptance:** `POST /api/auth/request` issues a token + sends SES email; `/auth/verify`
consumes it, sets a signed-JWT cookie, first login grants 5 credits (idempotent).
**Tier:** T2 (inspection — touches identity).

## #3 — Upload + transactional credit spend + enqueue
**Acceptance:** `POST /api/upload` validates file (zod), spends 1 credit in a txn with an
advisory lock, creates a `generations` row, stores to S3, enqueues SQS; returns `{id}`. A
user at balance 0 gets 402. **Tier:** T2.

## #4 — Worker: Gemini → poster → SES
**Acceptance:** consumes SQS, marks processing, Gemini restyle, sharp composite, upload,
mark done, email; failure → failed + refund; redelivery-safe. DLQ wired.

## #5 — Stripe checkout + webhook
**Acceptance:** checkout session for $1/10 credits; webhook verifies signature, dedupes on
`webhook_events`, appends `+10`. Credits granted **only** on the webhook. **Tier:** T1
(do-not-automate from review — money).

## #6 — Terraform foundation
**Acceptance:** VPC, ALB+ACM+Route53, ECS web+worker, RDS, S3×2, SQS+DLQ, SES, IAM least
-privilege, Secrets Manager, EventBridge monthly cron; `fmt -check` + `validate` pass.
**Tier:** human-gated apply.

## #7 — Admin backend
**Acceptance:** `requireAdmin` allow-list; dashboard totals; manual credit adjust recorded
as a ledger event with a reason.

## #8 — Monthly free reset
**Acceptance:** EventBridge → one-off ECS task → grant 5/user for `YYYY-MM`, idempotent via
`monthly_grants`.

Each issue's "definition of done" included: `verify` green, the author can explain every
line, and — for #2/#3/#5 — a human read the diff before merge.
