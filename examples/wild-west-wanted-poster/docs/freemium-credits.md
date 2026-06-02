# Freemium & credits (Phase 4)

Rules: 5 free credits/month, $1 = 10 credits, 1 poster = 1 credit. Implemented in
`web/lib/credits.ts` and `worker/src/monthly-reset.ts`.

## Balance
`getBalance(userId)` = `SUM(delta)` over `credit_ledger`. There is no cached balance.

## Spend (the careful part)
`spendOneCredit(userId, genId)` runs in one transaction:
```
BEGIN;
SELECT pg_advisory_xact_lock(hashtext(userId));     -- serialize this user's spends
balance := SUM(delta) WHERE user_id = userId;
IF balance < 1 THEN ROLLBACK → 402 insufficient_credits;
INSERT credit_ledger(userId, -1, 'generation', genId);
INSERT generations(genId, userId, 'queued', uploadKey);
COMMIT;
-- only now: putObject(upload) + sendSQS(job)   (side effects, post-commit)
```
The advisory lock prevents two concurrent uploads from both spending the last credit.

## Grants
- **Sign-up:** first successful magic-link verify grants `+5 'monthly_free'` for the
  current period (idempotent via `monthly_grants`).
- **Monthly cron:** grants `+5` to every user for the new period, skipping anyone who
  already has a `monthly_grants` row for it.
- **Purchase:** Stripe webhook appends `+10 'purchase'`.
- **Refund:** worker appends `+1 'refund'` keyed to the generation id when a job fails.
