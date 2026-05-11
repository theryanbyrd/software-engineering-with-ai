---
name: db-migration
description: Plans and writes a database migration with rollback, including the forward and backward SQL, the application code changes, and a staging-replay plan. Use when the user asks for a schema change, column add/drop, index change, or data backfill. Always plan before writing SQL.
allowed_tools: Read, Edit, Write, Bash, Grep
---

# Database migration

## When to use this skill

The user has asked for a schema change. Always run this skill even if the change seems trivial. "Add a column" is not trivial in production.

## Procedure

1. **Read `docs/db.md`** (or your team's database conventions doc) and the target table's most recent migration to understand naming and idempotency conventions.
2. **Confirm the change is backward-compatible.** If not, explicitly flag this and stop for human approval. Non-backward-compatible migrations require a multi-step deploy and cannot be done in a single PR.
3. **Write a forward migration AND a backward migration.** Backward migrations are required, no exceptions. If you cannot write a backward migration (e.g., dropping a column with data), the migration is destructive — flag for human approval.
4. **Plan the deploy order:**
   - Schema change (additive)
   - App deploy (handles both old and new schema)
   - Backfill (if needed)
   - App deploy (uses new schema only)
   - Cleanup (drop unused columns/indexes)
   Document each step.
5. **Generate a staging-replay command** using `scripts/replay-migration.sh` (or your team's equivalent). The replay should run the migration against a copy of staging data and verify no errors.
6. **Output the plan to the user. Wait for approval before writing files.**

## Output

```
## Migration plan

**Change:** <one-line description>
**Backward-compatible:** yes / no (if no, requires multi-step deploy)
**Estimated lock impact:** <none / brief / extended — use ACCESS EXCLUSIVE warnings>

**Forward migration:** path/to/NNN_change.up.sql
**Backward migration:** path/to/NNN_change.down.sql

**Deploy order:**
1. ...
2. ...

**Staging replay:** `bash scripts/replay-migration.sh NNN`

**App code changes required:** <list>

Awaiting approval before writing files.
```

## Forbidden

- Do not run `DROP TABLE`, `DROP COLUMN`, or `TRUNCATE` without explicit human approval at execution time.
- Do not modify migrations that have already been applied (check `schema_migrations` or your team's equivalent).
- Do not generate destructive backfills without a `--dry-run` mode first.
- Do not skip the backward migration. "It's hard to write" is not an exception.
- Do not skip the staging-replay step.

## References

- `references/migration-conventions.md` — naming, transaction wrapping, lock-timeout patterns (TBD; create if absent)
- Chapter 13 §13.4 — the canonical sample of this skill in the handbook
