// lib/db.ts — Single shared pg Pool built from DATABASE_URL. Ch 22 data access / connection pooling.
// All persistence flows through here so we keep one pool per container (ECS task).
import { Pool, type PoolClient, type QueryResultRow } from 'pg';
import { env } from './env';

declare global {
  // Reuse the pool across hot reloads in dev to avoid exhausting connections.
  // eslint-disable-next-line no-var
  var __wwwpPool: Pool | undefined;
}

function makePool(): Pool {
  return new Pool({
    connectionString: env().DATABASE_URL,
    max: 10,
    idleTimeoutMillis: 30_000,
    connectionTimeoutMillis: 5_000,
  });
}

export const pool: Pool = global.__wwwpPool ?? makePool();
if (process.env.NODE_ENV !== 'production') global.__wwwpPool = pool;

/** Run a parameterized query and return rows. */
export async function query<T extends QueryResultRow = QueryResultRow>(
  text: string,
  params: ReadonlyArray<unknown> = [],
): Promise<T[]> {
  const res = await pool.query<T>(text, params as unknown[]);
  return res.rows;
}

/** Run a function inside a transaction; commits on success, rolls back on throw. */
export async function withTransaction<T>(fn: (client: PoolClient) => Promise<T>): Promise<T> {
  const client = await pool.connect();
  try {
    await client.query('BEGIN');
    const result = await fn(client);
    await client.query('COMMIT');
    return result;
  } catch (err) {
    await client.query('ROLLBACK');
    throw err;
  } finally {
    client.release();
  }
}
