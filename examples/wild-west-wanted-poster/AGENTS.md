# AGENTS.md

Cross-vendor agent guidance for the Wild West Wanted Poster example. See
[CLAUDE.md](CLAUDE.md) for the full map; this file exists so non-Claude CLIs get the same
context (Ch 6, Appendix B).

- Build/verify: in `web/` and `worker/`, run `npm run typecheck` (`tsc --noEmit`) and lint.
  Terraform: `terraform fmt -check -recursive && terraform validate` in `infra/terraform/`.
- Do not commit secrets; `.env.example` documents names only.
- Money, auth, secrets, and `terraform apply` are human-gated (Ch 32).
- Credits are event-sourced (append-only `credit_ledger`); never mutate balances.
