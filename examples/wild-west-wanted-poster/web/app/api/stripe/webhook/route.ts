// app/api/stripe/webhook/route.ts — POST Stripe webhook: verify signature on the RAW body,
// idempotently record the event, then credit purchases (+10) via the ledger. Ch 25 payments + Ch 30 idempotency.
import { NextRequest, NextResponse } from 'next/server';
import type Stripe from 'stripe';
import { stripe } from '@/lib/stripe';
import { env } from '@/lib/env';
import { withTransaction } from '@/lib/db';
import { PURCHASE_CREDITS } from '@/lib/credits';

// Must run on Node and read the raw body (no body parsing) for signature verification.
export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';

export async function POST(req: NextRequest): Promise<NextResponse> {
  const sig = req.headers.get('stripe-signature');
  if (!sig) return NextResponse.json({ error: 'Missing signature' }, { status: 400 });

  const rawBody = await req.text(); // raw string is required for verify

  let event: Stripe.Event;
  try {
    event = stripe().webhooks.constructEvent(rawBody, sig, env().STRIPE_WEBHOOK_SECRET);
  } catch (err) {
    console.error('Stripe signature verification failed:', err);
    return NextResponse.json({ error: 'Invalid signature' }, { status: 400 });
  }

  try {
    await withTransaction(async (client) => {
      // Idempotency: webhook_events.id is the Stripe event id (PK). Second delivery is a no-op.
      const inserted = await client.query(
        `INSERT INTO webhook_events (id, type, received_at)
         VALUES ($1, $2, now())
         ON CONFLICT (id) DO NOTHING`,
        [event.id, event.type],
      );
      if (inserted.rowCount === 0) return; // already processed

      if (event.type === 'checkout.session.completed') {
        const session = event.data.object as Stripe.Checkout.Session;
        const userId = session.client_reference_id ?? session.metadata?.userId;
        if (!userId) {
          console.error('checkout.session.completed without userId', session.id);
          return;
        }

        // Record the payment (unique on stripe_session_id) ...
        await client.query(
          `INSERT INTO payments (id, user_id, stripe_session_id, amount_cents, credits, status, created_at)
           VALUES (gen_random_uuid(), $1, $2, $3, $4, 'completed', now())
           ON CONFLICT (stripe_session_id) DO NOTHING`,
          [userId, session.id, session.amount_total ?? 100, PURCHASE_CREDITS],
        );

        // ... and append +10 credits to the event-sourced ledger.
        await client.query(
          "INSERT INTO credit_ledger (user_id, delta, reason, ref) VALUES ($1, $2, 'purchase', $3)",
          [userId, PURCHASE_CREDITS, session.id],
        );
      }
    });

    return NextResponse.json({ received: true });
  } catch (err) {
    console.error('Webhook processing error:', err);
    return NextResponse.json({ error: 'Processing error' }, { status: 500 });
  }
}
