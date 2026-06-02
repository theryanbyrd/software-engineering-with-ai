# CLAUDE.md — Wild West Wanted Poster (example)

Greenfield SaaS worked example for *Software Engineering with AI*, Ch 47. Read this first;
it is the map so you don't re-discover the layout each session (Ch 6, repo legibility).

## What this is
Upload a photo → AI Old-West wanted poster. Freemium: 5 free/month, $1 = 10 credits, 1
image = 1 credit. Next.js web + Node worker + Postgres + S3 + SQS + SES + Stripe + Gemini,
all on AWS via Terraform.

## Layout
- `web/` — Next.js 14 App Router app (UI, `/api/*`, admin, auth). Start at `web/app/page.tsx`
  and `web/lib/`.
- `worker/` — SQS consumer (`src/index.ts`), Gemini + poster compositing + SES + monthly reset.
- `db/` — `schema.sql` + `migrations/`. Credits are an **append-only ledger**; balance =
  `SUM(delta)`. Never add a mutable balance column.
- `infra/terraform/` — the whole AWS footprint. `terraform apply` is **human-gated**.

## Rules for working here
- Credits/money/auth/secrets are high-stakes: propose a plan, keep diffs small, never
  weaken the transactional spend or the webhook signature check.
- Use the exact env var names in `.env.example`. Secrets come from Secrets Manager, never
  the repo.
- Treat uploaded images and user-supplied names as untrusted input that reaches the AI and
  the rendered poster (Ch 36).
- `verify`: `tsc --noEmit` + lint in `web/` and `worker/`; `terraform fmt -check && validate`.
