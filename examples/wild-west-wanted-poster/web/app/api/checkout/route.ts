// app/api/checkout/route.ts — POST: create a Stripe Checkout Session for the $1/10-credit pack.
// Ch 25 payments. Returns {url} for the client to redirect to.
import { NextResponse } from 'next/server';
import { requireUser } from '@/lib/auth';
import { createCheckoutSession } from '@/lib/stripe';
import { errorResponse } from '@/lib/http';

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';

export async function POST(): Promise<NextResponse> {
  try {
    const user = await requireUser();
    const url = await createCheckoutSession(user.id, user.email);
    return NextResponse.json({ url });
  } catch (err) {
    return errorResponse(err);
  }
}
