// app/api/admin/credits/route.ts — POST manual credit adjustment by an admin. Ch 31 admin tooling + Ch 30 ledger.
// Append-only: even admin corrections are ledger entries (reason 'refund'), never balance edits.
import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';
import { requireAdmin } from '@/lib/auth';
import { appendLedger, getBalance } from '@/lib/credits';
import { errorResponse } from '@/lib/http';

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';

const Body = z.object({
  userId: z.string().uuid(),
  delta: z.number().int().refine((n) => n !== 0, 'delta must be non-zero'),
  reason: z.enum(['monthly_free', 'purchase', 'generation', 'refund']).default('refund'),
});

export async function POST(req: NextRequest): Promise<NextResponse> {
  try {
    const admin = await requireAdmin();
    const { userId, delta, reason } = Body.parse(await req.json());

    // ref records who made the adjustment for auditability.
    await appendLedger(userId, delta, reason, `admin:${admin.email}`);
    const balance = await getBalance(userId);

    return NextResponse.json({ ok: true, userId, balance });
  } catch (err) {
    return errorResponse(err);
  }
}
