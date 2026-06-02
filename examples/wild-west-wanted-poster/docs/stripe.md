# Payments — Stripe (Phase 8)

"Buy 10 credits for $1." Test mode first; the same code works in live mode with live keys.

## Checkout
`POST /api/checkout` (`web/app/api/checkout/route.ts`) creates a Checkout Session:
`mode=payment`, one line item = `STRIPE_PRICE_CREDITS` (qty 1), `client_reference_id =
userId`, success/cancel URLs back to `APP_URL`. Returns the hosted `url`; the client
redirects.

## Webhook (where the credits are actually granted)
`POST /api/stripe/webhook` (`web/app/api/stripe/webhook/route.ts`):
1. Read the **raw** body (Next.js: do not let the framework parse it) and verify the
   `Stripe-Signature` with `STRIPE_WEBHOOK_SECRET`. An unverified body is untrusted input.
2. Idempotency: `INSERT INTO webhook_events(id) … ON CONFLICT DO NOTHING`; if the event was
   already seen, return 200 and stop.
3. On `checkout.session.completed`: insert a `payments` row and append `+10 'purchase'` to
   the ledger, keyed to the session id.

## Why grant on the webhook, not on the success redirect
The success URL is a client navigation and can be spoofed or simply never reached. The
webhook is the authoritative, signed signal that money moved. Never grant credits from the
browser's success page.

## Local testing
`stripe listen --forward-to localhost:3000/api/stripe/webhook` and use test cards.
