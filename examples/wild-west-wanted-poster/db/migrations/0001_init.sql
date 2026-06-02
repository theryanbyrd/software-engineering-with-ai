-- 0001_init.sql — Initial schema migration for wwwp.
-- Book chapter concept: "Schema migrations as ordered, replayable steps" — each file is a
-- forward-only step applied in filename order. This first step creates the full baseline schema.
-- Apply with: psql "$DATABASE_URL" -f db/migrations/0001_init.sql  (see db/README.md).

BEGIN;

CREATE EXTENSION IF NOT EXISTS citext;
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS users (
  id            uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
  email         citext      NOT NULL UNIQUE,
  is_admin      boolean     NOT NULL DEFAULT false,
  created_at    timestamptz NOT NULL DEFAULT now(),
  last_login_at timestamptz
);

CREATE TABLE IF NOT EXISTS auth_tokens (
  token       text        PRIMARY KEY,
  user_id     uuid        NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  expires_at  timestamptz NOT NULL,
  consumed_at timestamptz
);
CREATE INDEX IF NOT EXISTS auth_tokens_user_id_idx ON auth_tokens (user_id);

CREATE TABLE IF NOT EXISTS credit_ledger (
  id         bigserial   PRIMARY KEY,
  user_id    uuid        NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  delta      integer     NOT NULL,
  reason     text        NOT NULL,
  ref        text,
  created_at timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT credit_ledger_reason_chk
    CHECK (reason IN ('monthly_free', 'purchase', 'generation', 'refund'))
);
CREATE INDEX IF NOT EXISTS credit_ledger_user_id_idx ON credit_ledger (user_id);

CREATE TABLE IF NOT EXISTS monthly_grants (
  user_id    uuid        NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  period     char(7)     NOT NULL,
  granted_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (user_id, period)
);

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
CREATE INDEX IF NOT EXISTS generations_user_id_status_idx ON generations (user_id, status);

CREATE TABLE IF NOT EXISTS payments (
  id                uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id           uuid        NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  stripe_session_id text        NOT NULL UNIQUE,
  amount_cents      integer     NOT NULL,
  credits           integer     NOT NULL,
  status            text        NOT NULL,
  created_at        timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS webhook_events (
  id          text        PRIMARY KEY,
  type        text        NOT NULL,
  received_at timestamptz NOT NULL DEFAULT now()
);

COMMIT;
