# Characterization tests

> "You cannot safely change what you have not pinned." In a brownfield codebase with no
> behavioral test suite, the first move is to characterize the behavior you are about to
> stand next to — *before* you touch it. These tests fail loudly if the existing email-2FA
> contract drifts while we add TOTP. If a TOTP change makes one of these go red, that is a
> regression to explain, not a test to edit away (slop signature #2: deleted edge cases).

osTicket can't easily instantiate its auth classes in isolation (no framework, DB-coupled
bootstrap), so we characterize in two tiers — exactly how brownfield testing actually starts:

### Tier 1 — structural invariants (runs anywhere, no DB)
[`test.2fa-email.php`](test.2fa-email.php) asserts the source-level contract we depend on:
the backend abstraction, the registered email backend and its id, the required method
surface, the OTP length, and the strike/timeout machinery. It is intentionally in the same
idiom as osTicket's own `setup/test/` checks. Run via the harness `verify.sh`, or directly:

```bash
php test.2fa-email.php /path/to/osticket-src
```

It also records a **known baseline**: the base `_validate()` compares OTPs with `strcmp()`,
which is not constant-time. We pin it so the TOTP review is forced to make a *conscious*
decision about comparison timing rather than inheriting the email path by accident.

### Tier 2 — integration (runs in the Docker env)
Once `harness/docker-compose.yml` is up and osTicket is installed, the real characterization
is a browser/API flow: enable email 2FA for a staff user, log in, confirm the OTP email is
sent, that a wrong code is rejected, that `getMaxStrikes()` lockout triggers, and that a
correct code completes login. Script it with the `webapp-testing` skill (Playwright) and have
it return pass/fail + a screenshot/log path. This is the test the TOTP feature must not break.
