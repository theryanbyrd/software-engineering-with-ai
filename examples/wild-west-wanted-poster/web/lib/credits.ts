// lib/credits.ts — Event-sourced credit ledger: balance = SUM(delta). Append-only, never UPDATE/DELETE.
// Ch 30 event sourcing. The transactional spend is the heart of the freemium/credits rules.
import { randomUUID } from 'crypto';
import type { PoolClient } from 'pg';
import { query, withTransaction } from './db';

export type LedgerReason = 'monthly_free' | 'purchase' | 'generation' | 'refund';

export const PURCHASE_CREDITS = 10; // $1 = 10 credits
export const MONTHLY_FREE_CREDITS = 5; // 5 free generations/month

/** balance(user) = COALESCE(SUM(delta),0) FROM credit_ledger WHERE user_id=$1 */
export async function getBalance(userId: string): Promise<number> {
  const rows = await query<{ balance: string }>(
    'SELECT COALESCE(SUM(delta), 0)::int AS balance FROM credit_ledger WHERE user_id = $1',
    [userId],
  );
  return Number(rows[0]?.balance ?? 0);
}

/** Same as getBalance but runs on an existing transaction client with a row lock intent. */
async function getBalanceTx(client: PoolClient, userId: string): Promise<number> {
  const res = await client.query<{ balance: string }>(
    'SELECT COALESCE(SUM(delta), 0)::int AS balance FROM credit_ledger WHERE user_id = $1',
    [userId],
  );
  return Number(res.rows[0]?.balance ?? 0);
}

/** Append a ledger entry (any delta/reason). Used for purchases, grants, refunds, admin adjusts. */
export async function appendLedger(
  userId: string,
  delta: number,
  reason: LedgerReason,
  ref: string | null = null,
): Promise<void> {
  await query(
    'INSERT INTO credit_ledger (user_id, delta, reason, ref) VALUES ($1, $2, $3, $4)',
    [userId, delta, reason, ref],
  );
}

/** Grant credits (positive delta). Convenience wrapper over appendLedger. */
export async function grantCredits(
  userId: string,
  amount: number,
  reason: LedgerReason,
  ref: string | null = null,
): Promise<void> {
  if (amount <= 0) throw new Error('grantCredits requires a positive amount');
  await appendLedger(userId, amount, reason, ref);
}

export class InsufficientCreditsError extends Error {
  constructor() {
    super('Insufficient credits');
    this.name = 'InsufficientCreditsError';
  }
}

/**
 * Transactional spend of exactly one credit, tied to a generation.
 * Per conventions: BEGIN; check balance>=1; INSERT credit_ledger(-1,'generation',genId); <work>; COMMIT.
 * The caller's `work` runs inside the same transaction (e.g. INSERT generations row) — if it throws,
 * the spend is rolled back. SQS enqueue should happen AFTER commit (side effect) by the caller.
 *
 * Returns the generated genId so the caller can use it consistently as the ledger ref.
 */
export async function spendOneCredit(
  userId: string,
  work: (client: PoolClient, genId: string) => Promise<void>,
): Promise<string> {
  const genId = randomUUID();
  await withTransaction(async (client) => {
    // Serialize concurrent spends for this user to avoid races on the running balance.
    await client.query('SELECT pg_advisory_xact_lock(hashtext($1))', [userId]);

    const balance = await getBalanceTx(client, userId);
    if (balance < 1) throw new InsufficientCreditsError();

    await client.query(
      "INSERT INTO credit_ledger (user_id, delta, reason, ref) VALUES ($1, -1, 'generation', $2)",
      [userId, genId],
    );

    await work(client, genId);
  });
  return genId;
}

/** Refund a previously spent generation credit (e.g. worker reported failure). */
export async function refundGeneration(userId: string, genId: string): Promise<void> {
  await appendLedger(userId, 1, 'refund', genId);
}
