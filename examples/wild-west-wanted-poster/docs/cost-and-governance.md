# Cost & governance

## Autonomy levels used (Ch 32)
| Area | Autonomy | Why |
|------|----------|-----|
| UI, route handlers, worker logic, docs | High (agent drafts, human reviews PR) | Bounded blast radius, covered by `verify` |
| Credit math, Stripe webhook, auth/session | Low (plan → review every line) | Money + identity; the Do-Not-Automate posture (Ch 33) |
| `terraform apply`, IAM, secrets | Human only | Irreversible / security-critical |

## Untrusted input (Ch 36)
Uploaded images and user names reach Gemini and the rendered poster. File type/size are
validated with zod before storage; user text is treated as poster *data*, never merged into
the model prompt; the Stripe webhook verifies signatures before trusting a body.

## Cost discipline (Ch 26, 29)
- Meter the vendor: 1 credit = 1 Gemini image. Marginal cost ≈ **$0.04/poster** [projection];
  revenue ≈ **$0.10/paid credit**. Free tier (5/mo) is capped CAC.
- Alarms: DLQ depth, oldest-message age, monthly Gemini spend, Fargate hours.
- Failure refunds credits, so vendor outages cost retries, not goodwill.

## Secrets (Ch 34)
All secrets in AWS Secrets Manager, injected as ECS task env. The repo carries names only
(`.env.example`). No secret ever lands in an image layer or git history.
