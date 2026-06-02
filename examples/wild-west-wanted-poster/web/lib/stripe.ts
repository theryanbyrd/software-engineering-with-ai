// lib/stripe.ts — Stripe client + one-time Checkout Session for the $1/10-credit pack.
// Ch 25 payments. Webhook verification + crediting lives in app/api/stripe/webhook.
import Stripe from 'stripe';
import { env } from './env';

let client: Stripe | null = null;

/** Lazily-constructed Stripe client (pinned API version). */
export function stripe(): Stripe {
  if (!client) {
    client = new Stripe(env().STRIPE_SECRET_KEY, { apiVersion: '2024-06-20' });
  }
  return client;
}

/**
 * Create a one-time Checkout Session for STRIPE_PRICE_CREDITS (qty 1 = 10 credits).
 * client_reference_id carries our userId so the webhook can credit the right user.
 */
export async function createCheckoutSession(userId: string, email: string): Promise<string> {
  const { APP_URL, STRIPE_PRICE_CREDITS } = env();
  const session = await stripe().checkout.sessions.create({
    mode: 'payment',
    customer_email: email,
    client_reference_id: userId,
    line_items: [{ price: STRIPE_PRICE_CREDITS, quantity: 1 }],
    success_url: `${APP_URL}/?purchase=success`,
    cancel_url: `${APP_URL}/?purchase=cancel`,
    metadata: { userId },
  });
  if (!session.url) throw new Error('Stripe did not return a checkout URL');
  return session.url;
}
