# Database — Wild West Wanted Poster (wwwp)

PostgreSQL 16 (RDS in production). All access from the app and worker goes through `pg`
(node-postgres) using the `DATABASE_URL` connection string.

This directory is the source of truth for the schema:

- **`schema.sql`** — the canonical, idempotent definition of every table, index, and comment.
  Useful for spinning up a fresh database or diffing against a live one.
- **`migrations/`** — ordered, forward-only steps. Filenames are zero-padded and applied in order.
  - `0001_init.sql` — creates the baseline schema.
  - `0002_seed_admin.sql` — flags admin accounts from `ADMIN_EMAILS`.

## Data model at a glance

| Table            | Purpose                                                            |
|------------------|-------------------------------------------------------------------|
| `users`          | Accounts (case-insensitive email via `citext`).                   |
| `auth_tokens`    | Single-use magic-link login tokens.                               |
| `credit_ledger`  | **Append-only** credit events. `balance = SUM(delta)`.            |
| `monthly_grants` | Idempotency for the 5 free credits/month, keyed by `(user, 'YYYY-MM')`. |
| `generations`    | Poster jobs: `queued -> processing -> done \| failed`.            |
| `payments`       | Stripe Checkout purchases ($1 = 10 credits).                      |
| `webhook_events` | Seen Stripe event ids (webhook idempotency).                      |

Credits are **event-sourced**: there is no `balance` column. To read a balance:

```sql
SELECT COALESCE(SUM(delta), 0) AS balance FROM credit_ledger WHERE user_id = $1;
```

Never `UPDATE` or `DELETE` in `credit_ledger` — corrections are new rows (e.g. a `+1`/`refund`).

## Applying migrations

### Option A — plain `psql` (no extra tooling)

```bash
export DATABASE_URL='postgres://user:pass@host:5432/wwwp'

# Apply in order. Each file is wrapped in a transaction.
for f in db/migrations/*.sql; do
  echo "Applying $f"
  psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f "$f"
done
```

To seed admins from `ADMIN_EMAILS` without editing SQL, use the templated form:

```bash
IFS=',' read -ra EMAILS <<< "$ADMIN_EMAILS"
for email in "${EMAILS[@]}"; do
  psql "$DATABASE_URL" -v ON_ERROR_STOP=1 \
    -v admin_email="$email" \
    -c "INSERT INTO users (email, is_admin) VALUES (:'admin_email', true) \
        ON CONFLICT (email) DO UPDATE SET is_admin = true;"
done
```

### Option B — `node-pg-migrate`

If you prefer a migration runner with an applied-migrations table and `up`/`down`:

```bash
npm i -D node-pg-migrate pg
# point it at this directory's SQL steps (or convert them to node-pg-migrate JS files)
DATABASE_URL="$DATABASE_URL" npx node-pg-migrate up -m db/migrations
```

`node-pg-migrate` records applied steps in a `pgmigrations` table so re-running is safe.
The plain-`psql` loop above is intentionally simple and works for the book example; the
`CREATE ... IF NOT EXISTS` / `ON CONFLICT` guards keep both approaches idempotent.

## Fresh database from scratch

```bash
createdb wwwp
psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f db/schema.sql
```

## Book chapter mapping

- **Event sourcing** — `credit_ledger` is the worked example for "derive state from an event log".
- **Idempotency** — `monthly_grants` and `webhook_events` show two flavors of "exactly-once-ish".
- **Migrations** — `migrations/` demonstrates ordered, replayable schema evolution.
