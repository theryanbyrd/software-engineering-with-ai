# CLAUDE.md — osTicket (brownfield harness)

> This file makes osTicket legible to an agent. It is the map so the agent does not
> re-derive the layout every session (Ch 6, repo legibility). It is written for a
> checkout of https://github.com/osTicket/osTicket. Paths are relative to the osTicket
> repo root, not to this example folder.

## What this is
osTicket — a legacy LAMP support-ticket system. Classic PHP (PHP 7.x/8.x), MySQL/MariaDB,
Apache. ~1,500 PHP files / ~360k LOC, much of it vendored under `include/` (laminas-mail,
mpdf, etc.). No framework: there is a **custom autoloader** (`include/UniversalClassLoader.php`)
and a **custom ORM** (`include/class.orm.php`, `VerySimpleModel`).

## Where things live
- **Front controllers (client):** `index.php`, `open.php` (new ticket), `tickets.php`,
  `login.php`, `account.php` — bootstrapped by `client.inc.php`.
- **Staff control panel:** `scp/` — bootstrapped by `scp/staff.inc.php` → `secure.inc.php`.
- **API:** `api/http.php` (REST dispatcher), `api/pipe.php` (inbound email→ticket),
  `api/cron.php`. Backends register routes via `Signal::send('api', $dispatcher)`.
- **Core classes:** `include/class.*.php` (~94). Key ones for this task:
  - `class.2fa.php` — the 2FA framework (see below). **This is the seam we extend.**
  - `class.auth.php` — authentication, login flow, where 2FA is invoked.
  - `class.base32.php` — Base32 encode/decode (needed for TOTP secrets).
  - `class.orm.php` — the ORM. Models extend `VerySimpleModel`.
  - `class.signal.php` — the publish/subscribe hook bus.
  - `class.plugin.php` — the plugin system.
  - `class.dynamic_forms.php` / `SimpleForm` — the forms engine the 2FA UI uses.
- **DB:** schema in `setup/inc/sql/`; migrations as upgrade streams in
  `include/upgrader/streams/`. Models map to tables via the ORM, not raw SQL.
- **Tests:** `setup/test/run-tests.php` — lint/structural only (short-open-tags, var_dump,
  signals, validation). **There is no behavioral test suite.** We add one (see `harness/`).

## The 2FA seam (`include/class.2fa.php`)
- `abstract class TwoFactorAuthenticationBackend` defines `send($user)`, `validate($form,$user)`,
  `getSetupForm()`, `getInputForm()`, and registration via `register($class)` /
  `allRegistered()` / `getBackend($id)`.
- Helpers on the base class: `store($otp)` stashes an OTP in `$_SESSION['_2fa']`;
  `_validate($otp)` checks strikes (`getMaxStrikes()`) and timeout (`getTimeout()`) and then
  compares with `!strcmp($store['otp'], $otp)`.
- The only existing backend is `Email2FABackend` (id `2fa-email`): generates a 6-digit code,
  `send()`s it by email, validates against the session copy.

### Read this before writing any TOTP code
The base abstraction assumes "generate a code → send it → stash in session → compare." **TOTP
breaks that assumption.** With TOTP nothing is sent; the code is derived on the client from a
**persistent per-user secret** enrolled once. So:
- Do **not** reuse `store()/_validate()` as-is for the secret. The secret is durable state, not a
  per-login session nonce.
- `send()` has no meaning for TOTP — make it a no-op; enrollment happens in the setup form.
- `!strcmp()` is **not constant-time**. A secret-derived comparison must be constant-time.
These are design decisions, not mechanical ones. See `spec/` — the human owns them.

## Build / run / verify
- Dev environment: `harness/docker-compose.yml` (PHP-Apache + MySQL). osTicket ships none.
- One command to check the repo: `harness/verify.sh` (PHP lint + `setup/test` + characterization
  tests). Treat a green `verify` as necessary-but-not-sufficient — read the diff and pull the trace.

## Conventions / gotchas
- Use the ORM (`VerySimpleModel`), not hand-written SQL, for model changes.
- New persistent fields require an **upgrade stream migration**, not just a schema edit.
- i18n: user-facing strings go through `__()`; keep the `/* @trans */` markers.
- The custom autoloader resolves `class.<name>.php` — follow the existing file-naming exactly.
- Security-sensitive areas (auth, 2FA, sessions, file upload, email parsing) are **high-stakes**:
  propose a plan, keep diffs small, never weaken or remove an existing check to make something pass.

## Autonomy guardrail for THIS task
Auth/2FA is Tier-3 (Do-Not-Automate-without-senior). The agent drafts the mechanical parts
(enrollment UI, Base32/otpauth URI plumbing, tests). A senior human owns the security-critical
logic and the final review. A separate reviewer agent (different prompt/model) runs adversarially.
Never merge an auth change on a green checkmark alone.
