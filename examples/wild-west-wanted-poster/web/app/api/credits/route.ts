// app/api/credits/route.ts — GET the current user's credit balance (event-sourced sum). Ch 30.
import { NextResponse } from 'next/server';
import { requireUser } from '@/lib/auth';
import { getBalance } from '@/lib/credits';
import { errorResponse } from '@/lib/http';

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';

export async function GET(): Promise<NextResponse> {
  try {
    const user = await requireUser();
    const balance = await getBalance(user.id);
    return NextResponse.json({ balance });
  } catch (err) {
    return errorResponse(err);
  }
}
