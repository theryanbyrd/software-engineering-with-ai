# Reference notes — what's agent-draftable vs. human-owned

This folder is an **illustration of the change**, not a merge-ready patch. Its job is to make
the ownership boundary concrete. The `[AGENT]` / `[HUMAN]` / `[INTEGRATION]` tags in
[`class.totp2fa.php`](class.totp2fa.php) are the point of the whole example.

## Agent-draftable (mechanical 80%)
- The enrollment form fields and the `otpauth://` provisioning URI.
- The HOTP/TOTP pure functions (`hotp`, `totpAt`). They're verifiable against RFC vectors, so
  the agent can draft them and the test ([`test.totp-vectors.php`](test.totp-vectors.php)) proves them.
- The `send()` no-op, the i18n wiring, and the registration call.

## Human-owned (security-critical 20%) — never accept unreviewed
- **Constant-time comparison.** We use `hash_equals()` and evaluate the entire drift window
  before deciding, so timing can't leak which step matched. The base class's `strcmp()` is
  forbidden on this path (the characterization test pins that as a known baseline).
- **Replay protection.** A matched step must be consumed once; `loadLastStepFor`/`storeLastStepFor`
  are integration points the human wires to a per-user column with an atomic update.
- **Drift window = ±1 step.** Widening it is a weakened-validation slop signature; it stays fixed.
- **Secret at rest.** Generated with `random_bytes`, Base32-encoded, encrypted via osTicket's
  `Crypto` before persistence, never logged, never re-rendered after enrollment.
- **Recovery codes.** One-time, hashed at rest. (Not shown here; specified in the spec.)

## What's deliberately NOT here
- The upgrade-stream migration that adds the per-user `secret` and `last_step` columns.
- The `Crypto::encrypt/decrypt` wiring and `$user->get2FAConfig()` persistence.
- The confirm-before-enable enrollment handshake and recovery-code issuance.

These are left to the human precisely because they are the decisions that determine whether the
second factor is real or theater. That is the lesson: the agent gets you the legible 80% fast;
the 20% that must be exactly right is where you stay the engineer.

## Running the vector test
```bash
php test.totp-vectors.php   # standalone (uses the Base32 shim); expect "5 passed, 0 failed"
```
In a real osTicket checkout, the class autoloads `Base32` and `TwoFactorAuthenticationBackend`;
standalone, the shim covers Base32 and you stub the base class to exercise just the math.
