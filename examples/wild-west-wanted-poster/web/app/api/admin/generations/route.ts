// app/api/admin/generations/route.ts — GET recent generations with status, for ops monitoring. Ch 31.
import { NextResponse } from 'next/server';
import { requireAdmin } from '@/lib/auth';
import { query } from '@/lib/db';
import { errorResponse } from '@/lib/http';

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';

interface AdminGenRow {
  id: string;
  user_id: string;
  email: string;
  status: string;
  error: string | null;
  created_at: string;
  updated_at: string;
}

export async function GET(): Promise<NextResponse> {
  try {
    await requireAdmin();
    const rows = await query<AdminGenRow>(
      `SELECT g.id, g.user_id, u.email, g.status, g.error, g.created_at, g.updated_at
         FROM generations g
         JOIN users u ON u.id = g.user_id
        ORDER BY g.created_at DESC
        LIMIT 100`,
    );
    return NextResponse.json({ generations: rows });
  } catch (err) {
    return errorResponse(err);
  }
}
