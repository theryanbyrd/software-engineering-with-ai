-- 0002_seed_admin.sql — Seed/flag admin accounts from ADMIN_EMAILS.
-- Book chapter concept: "Bootstrapping operators safely" — admins are data, not code branches.
--
-- NOTE on ADMIN_EMAILS: the app reads a comma-separated ADMIN_EMAILS env var to know who is an
-- operator. SQL migrations cannot read env vars directly, so this step does two things:
--   1. Ensures any listed admin email exists as a user row.
--   2. Marks that user is_admin = true (idempotent; safe to re-run).
-- Replace the example address below with the value(s) from your ADMIN_EMAILS before applying,
-- OR apply via the templated form shown in db/README.md (psql --set) to inject ADMIN_EMAILS.
--
-- Default example matches the project owner used throughout the book example.

BEGIN;

-- Upsert the admin user, then flag as admin. Using citext means casing in ADMIN_EMAILS is moot.
INSERT INTO users (email, is_admin)
VALUES ('ryanbyrd@gmail.com', true)
ON CONFLICT (email) DO UPDATE SET is_admin = true;

COMMIT;

-- --- Templated alternative (run instead of the literal INSERT above) -------------------------
-- For each address in ADMIN_EMAILS, run:
--   psql "$DATABASE_URL" \
--     -v admin_email="$ADMIN_EMAIL" \
--     -c "INSERT INTO users (email, is_admin) VALUES (:'admin_email', true) \
--         ON CONFLICT (email) DO UPDATE SET is_admin = true;"
