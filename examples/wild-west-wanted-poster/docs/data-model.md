# Data model (Phase 2)

Defined in `db/schema.sql`, migrated via `db/migrations/`. The design decision that matters:
**credits are event-sourced.**

## Tables
- `users` — identity (`email` is `citext` unique), `is_admin`, timestamps.
- `auth_tokens` — magic-link tokens (`token` pk, `user_id`, `expires_at`, `consumed_at`).
- `credit_ledger` — **append-only.** `(id, user_id, delta, reason, ref, created_at)`.
  `reason ∈ {monthly_free, purchase, generation, refund, admin_adjust}`. Balance is
  `SELECT COALESCE(SUM(delta),0) FROM credit_ledger WHERE user_id=$1`.
- `monthly_grants` — `(user_id, period 'YYYY-MM')` PK; the idempotency guard for the
  monthly free 5.
- `generations` — `(id, user_id, status, upload_key, poster_key, error, timestamps)`;
  `status ∈ {queued, processing, done, failed}`.
- `payments` — Stripe purchases (`stripe_session_id` unique).
- `webhook_events` — `(id, type, received_at)`; Stripe idempotency.

## Why a ledger and not a balance column
Money-adjacent state is exactly where you want history. A mutable `credits` integer drifts
under concurrency, hides bugs, and can't answer "how did this user get to 3?" The ledger
answers it, makes refunds an append (not a risky decrement), and lets the admin tool record
manual adjustments as first-class, attributable events.

## Indexes
`credit_ledger(user_id)` (balance sums), `generations(user_id, status)` (admin dashboards
and per-user lists), `auth_tokens(user_id)`.
