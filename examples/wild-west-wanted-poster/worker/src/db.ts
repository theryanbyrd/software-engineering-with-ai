// db.ts — Postgres access helper (node-postgres pool) for the worker.
// Book chapter concept: "One connection pool per process" — share a pg.Pool, expose tiny
// query/tx helpers, and centralize the event-sourced credit-ledger reads/writes.

import { Pool, type PoolClient, type QueryResultRow } from 'pg';

const connectionString = process.env.DATABASE_URL;
if (!connectionString) {
  throw new Error('DATABASE_URL is required');
}

/** Shared connection pool for the worker process. */
export const pool = new Pool({
  connectionString,
  max: 5,
  idleTimeoutMillis: 30_000,
  // RDS requires TLS; allow self-signed chain in non-prod. Tighten via PGSSLMODE in prod.
  ssl: process.env.PGSSLMODE === 'disable' ? false : { rejectUnauthorized: false },
});

pool.on('error', (err) => {
  // Surface background client errors instead of crashing silently.
  console.error('[db] idle client error', err);
});

/** Run a parameterized query and return typed rows. */
export async function query<T extends QueryResultRow = QueryResultRow>(
  text: string,
  params: unknown[] = [],
): Promise<T[]> {
  const res = await pool.query<T>(text, params as never[]);
  return res.rows;
}

/** Run `fn` inside a transaction, committing on success and rolling back on throw. */
export async function withTransaction<T>(fn: (client: PoolClient) => Promise<T>): Promise<T> {
  const client = await pool.connect();
  try {
    await client.query('BEGIN');
    const result = await fn(client);
    await client.query('COMMIT');
    return result;
  } catch (err) {
    try {
      await client.query('ROLLBACK');
    } catch (rollbackErr) {
      console.error('[db] rollback failed', rollbackErr);
    }
    throw err;
  } finally {
    client.release();
  }
}

/** Current credit balance for a user = SUM(delta) over the append-only ledger. */
export async function getBalance(userId: string): Promise<number> {
  const rows = await query<{ balance: string }>(
    'SELECT COALESCE(SUM(delta), 0)::int AS balance FROM credit_ledger WHERE user_id = $1',
    [userId],
  );
  return Number(rows[0]?.balance ?? 0);
}

/** Append a credit-ledger event. The ledger is append-only — never UPDATE/DELETE it. */
export async function appendLedger(
  client: PoolClient,
  userId: string,
  delta: number,
  reason: 'monthly_free' | 'purchase' | 'generation' | 'refund',
  ref?: string,
): Promise<void> {
  await client.query(
    'INSERT INTO credit_ledger (user_id, delta, reason, ref) VALUES ($1, $2, $3, $4)',
    [userId, delta, reason, ref ?? null],
  );
}

/** Close the pool during graceful shutdown. */
export async function closePool(): Promise<void> {
  await pool.end();
}
