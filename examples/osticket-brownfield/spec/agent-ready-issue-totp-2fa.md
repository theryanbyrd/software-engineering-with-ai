# Agent-ready issue — Add a TOTP (authenticator-app) 2FA backend to osTicket

> This is the spec the agent works from. It follows the book's agent-ready-issue pattern:
> context, the seam, an explicit tier, hard constraints, the split of what the agent drafts
> vs. what the human owns, and acceptance criteria a deterministic `verify` can check.

## Context
osTicket has a pluggable 2FA framework (`include/class.2fa.php`) with exactly one backend,
`Email2FABackend`. We are adding a second backend, **`TOTP2FABackend`**, so staff can use an
authenticator app (Google Authenticator, Authy, 1Password, etc.) instead of emailed codes.

## Tier: **T3 — high-stakes, senior-owned.**
This is an authentication factor. Per the Do-Not-Automate catalog it is delegable *to the
author* but never *from review*. The agent assists; a senior engineer owns the design and the
security-critical logic; a separate reviewer agent runs adversarially; nothing merges on a
green check alone.

## The seam (and the trap — read `../CLAUDE.md` first)
Implement `class TOTP2FABackend extends TwoFactorAuthenticationBackend` and register it. The
base abstraction assumes "generate a code → `send()` it → stash in `$_SESSION` → `strcmp()` on
input." **TOTP violates every clause of that:**
- Nothing is sent. The code is derived on the client from a persistent per-user secret enrolled once.
- The secret is durable per-user state, not a per-login session nonce — do **not** persist it via `store()`.
- `send()` is meaningless → make it a safe no-op.
- `_validate()`'s `strcmp()` is **not constant-time** → the secret-derived comparison must be constant-time.

## Hard constraints (do not violate; these are gates, not suggestions)
Security (cross-references Ch 36.5):
1. **RFC 6238 TOTP / RFC 4226 HOTP.** SHA-1, 6 digits, 30s step (the authenticator-app default).
2. **Constant-time comparison** of the submitted code against computed candidates. Never `==`, never `strcmp`.
3. **Replay protection.** A code valid for a step may be used **once**; record the last-consumed step per user and reject re-use within the window.
4. **Bounded clock drift.** Accept ±1 step (±30s) only. Do not widen the window to "make it work."
5. **Secret generation** uses a CSPRNG (`random_bytes`), ≥160 bits, Base32-encoded via the existing `Base32` class (`include/class.base32.php`).
6. **Secret at rest** is encrypted with osTicket's existing crypto (`class.crypto.php`), not stored plaintext. Never logged, never returned to the client after enrollment, never placed in a URL/query string.
7. **Enrollment is confirm-before-enable:** the secret is only activated after the user proves possession by entering one valid code.
8. **Recovery codes:** issue a set of one-time recovery codes at enrollment (hashed at rest) so a lost device can't lock a user out — and so support can't be socially engineered into disabling 2FA.
9. **Preserve existing protections:** keep the strike limiting (`getMaxStrikes()`) and lockout. Do not weaken or remove any existing auth check (slop signature #5).
10. **Rate limit** verification attempts on the login route (Ch 36.5) in addition to strikes.

Engineering:
11. New persistent fields go through an **upgrade-stream migration** (`include/upgrader/streams/`), not a raw schema edit.
12. User-facing strings through `__()` with `/* @trans */` markers.
13. Follow the custom autoloader naming: the class lives in `include/class.totp2fa.php`.
14. Keep the diff small and within the seam. No "while I'm here" refactors of auth (slop signature #7).

## Split of ownership
**Agent drafts (mechanical 80%):**
- The enrollment setup form (`getSetupForm`) showing the Base32 secret + an `otpauth://` provisioning URI for the QR code.
- The Base32/HOTP/TOTP plumbing wired to the existing `Base32` class.
- The `send()` no-op, registration call, i18n wiring, and the migration skeleton.
- Tests: unit tests against RFC 6238 test vectors; an integration enrollment+login flow test.

**Human owns (security-critical 20%) — do not accept agent output here unreviewed:**
- The constant-time comparison and the replay/last-step bookkeeping.
- Secret-at-rest encryption and recovery-code hashing decisions.
- The drift window and strike/rate-limit interaction.
- The final security review and the merge decision.

## Acceptance criteria (deterministic where possible)
- [ ] `harness/verify.sh` passes, including the **unchanged** characterization tests (email 2FA contract intact).
- [ ] Unit tests reproduce the **RFC 6238 published test vectors** exactly (SHA-1 column).
- [ ] A code from a real authenticator app enrolled against the displayed secret logs a staff user in.
- [ ] A **reused** code (same step) is rejected (replay test).
- [ ] A code ±2 steps away is rejected; ±1 step is accepted (drift test).
- [ ] After `getMaxStrikes()` bad codes, the account is locked out (strike test).
- [ ] The secret never appears in logs, the rendered page after enrollment, or any URL (grep the trace).
- [ ] Comparison is constant-time (reviewed by a human; no `==`/`strcmp` on the code path).
- [ ] Recovery codes work once and are hashed at rest.
