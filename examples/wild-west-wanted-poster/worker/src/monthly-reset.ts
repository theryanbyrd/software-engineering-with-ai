// monthly-reset.ts — Grant 5 free credits to every user for the current 'YYYY-MM', idempotently.
// Book chapter concept: "Idempotent scheduled jobs" — driven by EventBridge Scheduler (a
// {command:'reset-monthly'} SQS message or a one-shot ECS task). monthly_grants is the dedupe key:
// (user_id, period). Re-running in the same month is a no-op.

import { PoolClient } from 'pg';
import { withTransaction, query, appendLedger } from './db.js';

const MONTHLY_FREE_CREDITS = 5;

/** Current period as 'YYYY-MM' in UTC. */
export function currentPeriod(date = new Date()): string {
  const y = date.getUTCFullYear();
  const m = String(date.getUTCMonth() + 1).padStart(2, '0');
  return `${y}-${m}`;
}

interface UserIdRow {
  id: string;
}

/**
 * Grant the monthly free credits for one user/period if not already granted.
 * Returns true if a grant was inserted, false if it was a no-op (already granted).
 * The grant + ledger insert happen in a single transaction so they can't drift apart.
 */
export async function grantUserMonthly(userId: string, period: string): Promise<boolean> {
  return withTransaction(async (client: PoolClient) => {
    // INSERT ... ON CONFLICT DO NOTHING is the idempotency guard. rowCount tells us if we won.
    const res = await client.query(
      `INSERT INTO monthly_grants (user_id, period)
       VALUES ($1, $2)
       ON CONFLICT (user_id, period) DO NOTHING`,
      [userId, period],
    );
    const inserted = (res.rowCount ?? 0) > 0;
    if (inserted) {
      await appendLedger(client, userId, +MONTHLY_FREE_CREDITS, 'monthly_free', period);
    }
    return inserted;
  });
}

export interface MonthlyResetSummary {
  period: string;
  usersConsidered: number;
  granted: number;
  skipped: number;
}

/**
 * Iterate all users and grant the current month's free credits idempotently.
 * Safe to run multiple times per month; only the first run per user actually grants.
 */
export async function runMonthlyReset(date = new Date()): Promise<MonthlyResetSummary> {
  const period = currentPeriod(date);
  const users = await query<UserIdRow>('SELECT id FROM users');

  let granted = 0;
  let skipped = 0;
  for (const u of users) {
    try {
      const did = await grantUserMonthly(u.id, period);
      if (did) granted += 1;
      else skipped += 1;
    } catch (err) {
      // Log and continue: one bad user shouldn't abort the whole monthly run.
      console.error(`[monthly-reset] failed for user ${u.id} period ${period}`, err);
      skipped += 1;
    }
  }

  const summary: MonthlyResetSummary = {
    period,
    usersConsidered: users.length,
    granted,
    skipped,
  };
  console.log(`[monthly-reset] ${JSON.stringify(summary)}`);
  return summary;
}

// Allow running as a standalone one-shot task: `tsx src/monthly-reset.ts` (npm run reset-monthly).
// Compares the resolved module path against the invoked script so it only auto-runs when executed
// directly, not when imported by the SQS consumer.
const invokedDirectly =
  process.argv[1] !== undefined && import.meta.url === `file://${process.argv[1]}`;
if (invokedDirectly) {
  runMonthlyReset()
    .then(() => process.exit(0))
    .catch((err) => {
      console.error('[monthly-reset] fatal', err);
      process.exit(1);
    });
}
