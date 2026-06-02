// lib/users.ts — User lookup/creation for magic-link auth + first-login free-credit grant.
// Ch 24 onboarding. Conventions: a user row is created when a magic link is requested; the first
// successful verify grants 5 free credits (idempotent via monthly_grants for the current period).
import type { PoolClient } from 'pg';
import { query, withTransaction } from './db';
import { isConfiguredAdmin } from './auth';
import { MONTHLY_FREE_CREDITS } from './credits';

export interface DbUser {
  id: string;
  email: string;
  is_admin: boolean;
}

/** Current period as 'YYYY-MM' for monthly_grants idempotency. */
export function currentPeriod(date = new Date()): string {
  const y = date.getUTCFullYear();
  const m = String(date.getUTCMonth() + 1).padStart(2, '0');
  return `${y}-${m}`;
}

/**
 * Find-or-create a user by email (called when a magic link is REQUESTED).
 * Does NOT grant credits — that happens on first successful verify.
 * Keeps is_admin in sync with ADMIN_EMAILS.
 */
export async function findOrCreateUser(email: string): Promise<DbUser> {
  const normalized = email.trim().toLowerCase();
  const admin = isConfiguredAdmin(normalized);

  const existing = await query<DbUser>(
    'SELECT id, email, is_admin FROM users WHERE email = $1',
    [normalized],
  );
  if (existing[0]) return existing[0];

  const created = await query<DbUser>(
    `INSERT INTO users (email, is_admin) VALUES ($1, $2)
       ON CONFLICT (email) DO UPDATE SET email = EXCLUDED.email
     RETURNING id, email, is_admin`,
    [normalized, admin],
  );
  return created[0]!;
}

/**
 * Called on a successful magic-link verify. Stamps last_login_at, syncs is_admin,
 * and grants the first 5 free credits if no grant exists for the current period.
 * Idempotent: monthly_grants PK (user_id, period) prevents double-granting.
 */
export async function completeLogin(userId: string): Promise<DbUser> {
  return withTransaction(async (client: PoolClient) => {
    const res = await client.query<DbUser>(
      'SELECT id, email, is_admin FROM users WHERE id = $1',
      [userId],
    );
    const user = res.rows[0];
    if (!user) throw new Error('User not found during login completion');

    const admin = isConfiguredAdmin(user.email);
    await client.query(
      'UPDATE users SET last_login_at = now(), is_admin = $2 WHERE id = $1',
      [user.id, admin],
    );

    const period = currentPeriod();
    const grant = await client.query(
      `INSERT INTO monthly_grants (user_id, period, granted_at)
       VALUES ($1, $2, now())
       ON CONFLICT (user_id, period) DO NOTHING`,
      [user.id, period],
    );
    // Only append the ledger entry if we actually inserted a fresh grant row.
    if (grant.rowCount && grant.rowCount > 0) {
      await client.query(
        "INSERT INTO credit_ledger (user_id, delta, reason, ref) VALUES ($1, $2, 'monthly_free', $3)",
        [user.id, MONTHLY_FREE_CREDITS, period],
      );
    }

    return { ...user, is_admin: admin };
  });
}
