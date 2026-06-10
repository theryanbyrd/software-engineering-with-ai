# Security & Resilience Checklist for AI-Coded Apps

> Print this. Run it against anything an agent built before it ships. Every item is a defect class agents produce *reliably*, and every one is invisible on the happy path you tested.

## 1. Secrets that ride to the client

The most common and most expensive mistake: a secret compiled into the frontend bundle.

- [ ] **No server secret referenced from client code.** An agent wiring up OpenAI, Supabase, or Stripe will read the key it needs from wherever it's writing code. If that code runs in the browser, the key is now in downloadable JavaScript.
- [ ] **Treat every `NEXT_PUBLIC_` / `VITE_` value as published — because it is.** Nothing with a public prefix may grant write or admin access.
- [ ] **Service-role / secret keys never appear in client code.** Supabase `service_role`, Stripe secret keys, any admin-scoped token → server-side only, behind an API route or edge function the browser calls without ever seeing the key.
- [ ] **A leaked key is leaked everywhere.** Remediation is rotate **plus** audit usage during the exposure window — the key is in every cached bundle and every user's history.

*Why the agent does it:* locally there's no observable difference between a key read on the server and one read in the browser — both make the call succeed.

## 2. Row-Level Security and the "it works in dev" trap

BaaS platforms (Supabase, Firebase) moved authorization into database policy. The policy is now the only thing between an authenticated user and everyone else's rows.

- [ ] **RLS enabled on every table that holds user data.** Supabase ships with RLS *off* until you enable it; an agent scaffolding a schema frequently leaves it off.
- [ ] **No `using (true)` / `allow read, write: if true`.** That technically "turns the feature on" while granting universal read/write. It's the tutorial default an agent copies and never tightens.
- [ ] **Deny-by-default, proven by a cross-user test** (see verification gates): user A creates a row; from user B's session the read returns nothing and the write is rejected.

*Why it survives to prod:* nothing in development exercises the boundary. You're logged in as yourself, you see your own data, the app is correct from where you sit. The hole only opens when a second user — or anyone with the public anon key — queries the table directly through the same client library your frontend uses.

## 3. Missing rate limits

Login, signup, password-reset, and any route that triggers a paid downstream call are the routes that most need a limit and are least likely to get one.

- [ ] **Rate limit on auth, signup, reset.** Open login pages invite credential-stuffing.
- [ ] **Rate limit on every route that costs money per call** (LLM calls, email sends). An open unauthenticated endpoint that calls a model invites a five-figure overnight bill or a drained connection pool.
- [ ] **Defined behavior at the limit:** token-bucket keyed on IP *and* user ID, stricter bucket on auth and paid calls, hard ceiling that returns `429` rather than melting.

*Why the agent skips it:* legitimate traffic never hits the limit you forgot to set, so no normal test surfaces the omission. This is the consumer-facing twin of the LLM-gateway chokepoint in the cost-discipline runbook.

## 4. Failing silently (resilience)

Ch 2's slop catalog names *deleted edge cases* and *silent error swallowing* as review smells. Seen from the running product, those smells become outages.

- [ ] **Every external boundary answers "what happens when this fails?"** — every network call, DB write, queue op.
- [ ] **Timeout with a sensible ceiling** on every call. No unbounded `fetch`.
- [ ] **Bounded retry with backoff and an idempotency key** so a retry can't double-charge or double-send.
- [ ] **User-visible failure state that is not a frozen spinner.**
- [ ] **No empty `catch`.** Errors surface to logs and traces, not a quiet `null` a downstream function dereferences into a second, more confusing crash.

*The counter-pattern, done deliberately (Ch 47.6):* a failed job marks the work failed and refunds the credit, a dead-letter queue catches poison messages, failures are absorbed on the operator's side rather than dumped on the customer. That behavior appeared because the spec demanded it — not because the agent is wise about failure.

## 5. The network you didn't test: offline & throttled

Agents develop on a fast, reliable, always-on network and ship code that assumes it's the only one that exists.

- [ ] **Core flows walked once on a throttled (slow-3G) profile** in browser dev tools.
- [ ] **Core flows walked once offline** — the app says something honest instead of hanging.
- [ ] **Optimistic-update paths tested with the reconcile actually failing** — that's the case that corrupts local state.

*Why it matters:* real users are on a train, in a garage, on hotel wifi that drops every ninety seconds. An app that never considered the throttled case doesn't fail gracefully — it hangs, the fetch has no timeout, the UI has no "still waiting" state, and the user decides your product is broken. On their network, it is.

---

## The paste-ready version (drop into a PR template or skill)

```
[ ] No secrets in the client bundle; no PUBLIC/VITE_ prefix on anything granting write/admin.
[ ] RLS (or equivalent) enabled and proven by a cross-user access test, not visual inspection.
[ ] Rate limits on auth/signup/reset and every route that costs money per call, with defined behavior at the limit.
[ ] Every external call wrapped in a timeout + bounded idempotent retry + user-visible failure state. No empty catch, no infinite spinner.
[ ] Core flows walked once on a throttled network and once offline.
```
