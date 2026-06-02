-- schema.sql — Full Postgres 16 schema for Wild West Wanted Poster (wwwp).
-- Book chapter concept: "Modeling state with an event-sourced credit ledger" — credits are
-- derived by summing an append-only ledger rather than stored as a mutable balance column.
-- This file is the canonical, idempotent definition of the schema. Migrations in db/migrations
-- build up to this state; this file is the reference/target a fresh DB can also be bootstrapped from.

-- citext gives us case-insensitive email comparisons without LOWER() everywhere.
CREATE EXTENSION IF NOT EXISTS citext;
-- pgcrypto provides gen_random_uuid() for UUID primary keys.
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- ---------------------------------------------------------------------------
-- users — one row per account. Identity is the (case-insensitive) email.
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
  id            uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
  email         citext      NOT NULL UNIQUE,
  is_admin      boolean     NOT NULL DEFAULT false,
  created_at    timestamptz NOT NULL DEFAULT now(),
  last_login_at timestamptz
);
COMMENT ON TABLE  users IS 'Accounts. Email is case-insensitive (citext) and unique.';
COMMENT ON COLUMN users.is_admin IS 'Set true for emails in ADMIN_EMAILS (see 0002_seed_admin.sql).';

-- ---------------------------------------------------------------------------
-- auth_tokens — single-use magic-link tokens for passwordless login.
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS auth_tokens (
  token       text        PRIMARY KEY,
  user_id     uuid        NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  expires_at  timestamptz NOT NULL,
  consumed_at timestamptz
);
COMMENT ON TABLE  auth_tokens IS 'Magic-link tokens. Single use: set consumed_at on verify.';
COMMENT ON COLUMN auth_tokens.consumed_at IS 'Non-null once redeemed; reject already-consumed tokens.';
CREATE INDEX IF NOT EXISTS auth_tokens_user_id_idx ON auth_tokens (user_id);

-- ---------------------------------------------------------------------------
-- credit_ledger — APPEND-ONLY event log of credit movements.
-- balance(user) = SUM(delta). Never UPDATE or DELETE rows here.
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS credit_ledger (
  id         bigserial   PRIMARY KEY,
  user_id    uuid        NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  delta      integer     NOT NULL,
  reason     text        NOT NULL,
  ref        text,
  created_at timestamptz NOT NULL DEFAULT now(),
  -- Guard the vocabulary of reasons so a typo never silently mis-prices an account.
  CONSTRAINT credit_ledger_reason_chk
    CHECK (reason IN ('monthly_free', 'purchase', 'generation', 'refund'))
);
COMMENT ON TABLE  credit_ledger IS 'Append-only credit events. balance = SUM(delta). Never mutate.';
COMMENT ON COLUMN credit_ledger.delta IS 'Signed change: +5 monthly_free, +10 purchase, -1 generation, +1 refund.';
COMMENT ON COLUMN credit_ledger.ref   IS 'Optional correlation id (generation id, stripe session id, period).';
-- Hot path: computing a user balance scans only that user''s events.
CREATE INDEX IF NOT EXISTS credit_ledger_user_id_idx ON credit_ledger (user_id);

-- ---------------------------------------------------------------------------
-- monthly_grants — idempotency guard for the 5 free credits per calendar month.
-- One row per (user, 'YYYY-MM'); presence means "already granted this period".
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS monthly_grants (
  user_id    uuid        NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  period     char(7)     NOT NULL,
  granted_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (user_id, period)
);
COMMENT ON TABLE  monthly_grants IS 'Idempotency for monthly free credits. period is ''YYYY-MM''.';

-- ---------------------------------------------------------------------------
-- generations — one row per poster job. Drives the SQS worker state machine.
-- status: queued -> processing -> done | failed
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS generations (
  id         uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id    uuid        NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  status     text        NOT NULL DEFAULT 'queued',
  upload_key text,
  poster_key text,
  error      text,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT generations_status_chk
    CHECK (status IN ('queued', 'processing', 'done', 'failed'))
);
COMMENT ON TABLE  generations IS 'Poster jobs. State machine: queued -> processing -> done|failed.';
COMMENT ON COLUMN generations.upload_key IS 'S3 key in S3_UPLOAD_BUCKET: uploads/{userId}/{genId}.';
COMMENT ON COLUMN generations.poster_key IS 'S3 key in S3_POSTER_BUCKET once done; served via presigned URL.';
-- Powers the user dashboard ("my recent generations") and admin filters by status.
CREATE INDEX IF NOT EXISTS generations_user_id_status_idx ON generations (user_id, status);

-- ---------------------------------------------------------------------------
-- payments — record of Stripe Checkout purchases ($1 = 10 credits).
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS payments (
  id                uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id           uuid        NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  stripe_session_id text        NOT NULL UNIQUE,
  amount_cents      integer     NOT NULL,
  credits           integer     NOT NULL,
  status            text        NOT NULL,
  created_at        timestamptz NOT NULL DEFAULT now()
);
COMMENT ON TABLE  payments IS 'Stripe Checkout purchases. stripe_session_id unique for idempotency.';

-- ---------------------------------------------------------------------------
-- webhook_events — Stripe webhook idempotency. id is the Stripe event id.
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS webhook_events (
  id          text        PRIMARY KEY,
  type        text        NOT NULL,
  received_at timestamptz NOT NULL DEFAULT now()
);
COMMENT ON TABLE webhook_events IS 'Seen Stripe event ids; insert-then-process to dedupe webhooks.';
