// app/api/admin/users/route.ts — GET admin user list with balances + generation counts. Ch 31 admin/ops.
import { NextResponse } from 'next/server';
import { requireAdmin } from '@/lib/auth';
import { query } from '@/lib/db';
import { errorResponse } from '@/lib/http';

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';

interface AdminUserRow {
  id: string;
  email: string;
  is_admin: boolean;
  created_at: string;
  last_login_at: string | null;
  balance: number;
  generations: number;
}

export async function GET(): Promise<NextResponse> {
  try {
    await requireAdmin();
    const rows = await query<AdminUserRow>(
      `SELECT u.id,
              u.email,
              u.is_admin,
              u.created_at,
              u.last_login_at,
              COALESCE((SELECT SUM(delta) FROM credit_ledger l WHERE l.user_id = u.id), 0)::int AS balance,
              (SELECT COUNT(*) FROM generations g WHERE g.user_id = u.id)::int AS generations
         FROM users u
        ORDER BY u.created_at DESC
        LIMIT 200`,
    );
    return NextResponse.json({ users: rows });
  } catch (err) {
    return errorResponse(err);
  }
}
