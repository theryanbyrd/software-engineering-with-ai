# Brownfield Worked Example — Adding TOTP 2FA to osTicket

Companion to *Software Engineering with AI: A Practical Handbook for the Claude Code Era* by Ryan Byrd. This is the **brownfield** counterpart to the greenfield [`wild-west-wanted-poster/`](../wild-west-wanted-poster/) example. Where that one builds a product from an empty directory, this one drops an agent into ~360k lines of legacy PHP it has never seen and adds a security-critical feature without making the codebase worse.

The subject is [osTicket](https://github.com/osTicket/osTicket) — a long-lived LAMP support-ticket system (classic procedural-plus-OO PHP on MySQL, a custom ORM, a custom forms engine, and almost no behavioral tests). It is representative of the systems most engineers actually inherit.

The feature is **TOTP two-factor authentication** (authenticator-app codes). It was chosen deliberately because it is *high-stakes*: it's an authentication factor, so the correctness bar is absolute, and it is exactly the kind of work the book's Do-Not-Automate catalog says the agent assists with but never owns. The lesson of this example is as much about **where you rein the agent in** as about what it can do.

## Why osTicket is a good brownfield subject

| Trait | What we found | Why it matters for the study |
|---|---|---|
| Size | ~1,500 PHP files, ~360k LOC (much vendored) | The agent cannot hold it in context; legibility (CLAUDE.md) is mandatory, not optional. |
| Style | Classic PHP, custom autoloader, custom ORM (`VerySimpleModel`) | The agent must learn local conventions instead of importing framework habits. |
| Tests | Only `setup/test/` — lint/structural checks, **no behavioral suite** | The single biggest brownfield hazard. We build the verification before we touch anything. |
| Seams | Signal bus (`class.signal.php`), plugin system (`class.plugin.php`), pluggable 2FA (`class.2fa.php`) | Real extension points let us add features without forking core. |
| Sensitivity | Tickets carry PII, file uploads, inbound email, auth/2FA | Security and resilience (Ch 36.5) are first-class, not afterthoughts. |

## The 2FA seam (and its trap)

osTicket already has a pluggable 2FA framework: an abstract `TwoFactorAuthenticationBackend` (`include/class.2fa.php`) with a `register()` mechanism — and currently exactly **one** backend, `Email2FABackend`, which emails a 6-digit code. Adding a `TOTP2FABackend` is the contained seam.

But the abstraction encodes an assumption that TOTP violates, and a naive agent will walk straight into it:

- The base class is built around **"generate a code, `send()` it, stash it in `$_SESSION`, compare on input."** TOTP sends nothing — the authenticator app generates the code from a **persistent per-user secret** enrolled once.
- The base `_validate()` compares with `!strcmp($store['otp'], $otp)` — a **non-constant-time** comparison. Fine-ish for an emailed nonce; a teaching point for a secret-derived code.
- `send($user)` is required by the interface but is meaningless for TOTP.

Surfacing that mismatch — and deciding the human owns the design while the agent drafts the mechanical parts — is the heart of this example.

## How the study is organized (read in order)

1. **[`CLAUDE.md`](CLAUDE.md)** — the legibility map the agent reads every session. Stack, the ORM/signal/2FA seams, build/test commands, gotchas, and the explicit "auth is high-stakes" guardrail.
2. **[`harness/`](harness/)** — the brownfield minimum viable harness: a Docker LAMP dev env (osTicket ships none), a single `verify` command, and **characterization tests** that pin the *existing* email-2FA behavior before we change anything.
3. **[`spec/`](spec/)** — the agent-ready issue for the TOTP backend (tiered T3), the Ch 36.5 security constraints, and the adversarial-review + verification plan for an auth change.
4. **[`reference/`](reference/)** — an annotated reference `TOTP2FABackend` and a NOTES file marking exactly which lines are agent-draftable and which are human-owned.

> The book chapter that narrates this example walks the same four steps as a story. This folder is the residue you can actually run.

## The one-paragraph version

You don't start by writing the feature. You start by making the codebase legible (CLAUDE.md), giving the agent a reproducible environment and a `verify` command, and pinning the behavior you're about to stand next to with characterization tests. Only then do you write a tight spec, let the agent draft the mechanical 80% (enrollment form, QR provisioning URI, Base32 plumbing), and reserve the security-critical 20% — constant-time comparison, replay/drift window, secret storage, recovery codes, strike limits — for a senior human and an adversarial reviewer. That sequence is the whole point.
