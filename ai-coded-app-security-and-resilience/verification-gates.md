# Verification Gates

Each gate converts a defect class an agent reliably produces into a gate it cannot pass. None require the agent to "be more careful." Wire them into the verification skill (the `.claude/skills/<flow>/scripts/` pattern) and into CI.

## Gate 1 — Bundle secret scan (build-time)

Grep the built client bundle for known secret shapes and fail the build if any match. Same hook pattern as Ch 35, applied to your own output instead of the agent's.

```bash
# fail the build if a server-secret shape made it into the client bundle
grep -rEn \
  -e 'sk-[A-Za-z0-9]{20,}' \
  -e 'sk_live_[A-Za-z0-9]{20,}' \
  -e 'service_role' \
  -e 'SUPABASE_SERVICE_ROLE' \
  dist/ build/ .next/static 2>/dev/null \
  && { echo "SECRET in client bundle"; exit 1; } || echo "bundle clean"
```

## Gate 2 — Cross-user RLS access test

The only thing that *proves* a policy. Provision two test users; assert the boundary holds.

```
1. As user A: create a row the policy says only A may see.
2. As user B (separate session, public anon key): SELECT it → expect 0 rows.
3. As user B: UPDATE / DELETE it → expect rejected (RLS violation).
4. Repeat per table that holds user data.
```

This is exactly the test an agent will not write unless it's in the spec. Put it there.

## Gate 3 — Auth-route burst test

```
Fire a burst (e.g. 100 requests in 5s) at the login/reset route.
Assert: the route returns 429 before the burst completes.
```

## Gate 4 — Fault injection

Prove the app degrades instead of hanging.

```
In a test environment, kill or 503 each external dependency in turn
(payment provider, AI vendor, DB under contention).
Assert: bounded wait, user-visible failure state, error in logs/traces — no hang, no silent null.
```

The book's chaos-and-fault-injection note exists precisely because agents mishandle retries and idempotency.

## Gate 5 — Throttled / offline walkthrough

Not fully automatable; make it a required manual step in the PR checklist.

```
[ ] Walked core flows on slow-3G profile (dev tools).
[ ] Walked core flows offline — honest message, no frozen screen.
[ ] Optimistic-update path tested with reconcile failing.
```

---

**The rule:** a hope is a prompt the next session forgets; a constraint is a gate that runs every time. Move each item above from hope to gate.
