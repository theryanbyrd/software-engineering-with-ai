# Wild West Wanted Poster — Infrastructure (Terraform / AWS)

This module provisions the full **from-scratch** AWS footprint for the `wild-west-wanted-poster`
(wwwp) worked example: upload a photo, get an AI-generated Old-West "WANTED" poster. It is the
companion infra to the book's chapters on IaC, networking, containers, queues, secrets, and
**cost discipline**.

Region: `us-west-2` · Domain: `wildwestwanted.com` · Everything tagged `project=wild-west-wanted-poster`.

## What this provisions

| File | Resources |
|------|-----------|
| `providers.tf` | AWS provider (region var), version pins, `terraform >= 1.6`, default tags |
| `backend.tf` | Commented S3 + DynamoDB remote-state example (bootstrap once, then uncomment) |
| `variables.tf` / `terraform.tfvars.example` | All inputs (domain, db, image tags, sizing, emails) |
| `network.tf` | VPC, 2× public + 2× private subnets across 2 AZs, IGW, single NAT, route tables |
| `dns.tf` | Route53 hosted zone, DNS-validated ACM cert (apex + www), A/alias records to the ALB |
| `alb.tf` | ALB, HTTPS listener (ACM), HTTP→HTTPS redirect, web target group, ALB/web/worker SGs |
| `ecr.tf` | ECR repos for `wwwp/web` and `wwwp/worker` (scan-on-push, keep-last-10 lifecycle) |
| `ecs.tf` | Fargate cluster, web (behind ALB, :3000) + worker services, log groups, web autoscaling, one-off reset task def |
| `rds.tf` | RDS PostgreSQL 16 (private subnets), subnet group, parameter group, RDS SG |
| `s3.tf` | Private uploads + posters buckets (block public access, SSE, 30-day raw-upload expiry) |
| `sqs.tf` | Standard generation-jobs queue + DLQ + redrive policy |
| `ses.tf` | SES domain identity, DKIM, custom MAIL FROM, verification records |
| `iam.tf` | Task execution role + least-privilege web/worker task roles + scheduler role |
| `secrets.tf` | Secrets Manager: `DATABASE_URL`, `AUTH_SECRET` (generated), `STRIPE_*`, `GEMINI_API_KEY` (empty) |
| `eventbridge-cron.tf` | EventBridge Scheduler (monthly, 1st 00:00 UTC) running the worker-reset task |
| `outputs.tf` | ALB DNS, NS records, ECR URLs, bucket names, queue URL, secret ARNs, etc. |

## Prerequisites

1. An AWS account + credentials (`aws configure` / SSO) with permission to create the above.
2. Terraform >= 1.6.
3. The domain `wildwestwanted.com` either registered in Route53, **or** registered elsewhere
   with its NS records delegated to this hosted zone. After the first apply, read
   `terraform output route53_name_servers` and set those at your registrar. ACM and SES
   validation will not complete until delegation is live.

## Apply order

Terraform resolves the dependency graph automatically, but conceptually the order is:

1. `terraform init` (configure the backend first if you uncommented `backend.tf`).
2. `terraform plan -out tfplan` and review.
3. `terraform apply tfplan`.
4. Set the registrar NS records to the `route53_name_servers` output, then wait for ACM cert
   validation and SES domain verification to flip to issued/verified (re-run apply if needed).
5. Populate the placeholder secrets (they are created with `CHANGE-ME`):
   ```sh
   aws secretsmanager put-secret-value --secret-id wwwp/stripe-secret-key     --secret-string 'sk_live_...'
   aws secretsmanager put-secret-value --secret-id wwwp/stripe-webhook-secret --secret-string 'whsec_...'
   aws secretsmanager put-secret-value --secret-id wwwp/gemini-api-key        --secret-string 'AIza...'
   ```
6. Build and push images to the ECR repos (`ecr_web_repository_url`, `ecr_worker_repository_url`),
   then bump `web_image_tag` / `worker_image_tag` and re-apply (or force a new ECS deployment).

> `DATABASE_URL` and `AUTH_SECRET` are generated and populated by Terraform; the DB master
> password lives in `wwwp/db-password`. The ECS task defs inject all of these as env via the
> task-definition `secrets` block.

## Teardown

```sh
terraform destroy
```

Notes:
- S3 buckets must be empty to delete. Empty them first (e.g. `aws s3 rm s3://<bucket> --recursive`)
  or the destroy will fail on the bucket resources.
- `rds.tf` sets `skip_final_snapshot = true` and `deletion_protection = false` for the worked
  example so teardown is clean. **Flip both for real production.**
- Secrets Manager secrets have a recovery window; add `--force-delete-without-recovery` if you
  need them gone immediately.

## Cost note (ties to the cost-discipline chapter)

This stack is intentionally lean but is **not** free. The standing-cost drivers, roughly:

- **NAT Gateway** — the biggest fixed line item (hourly + per-GB). We deliberately run **one**
  NAT instead of one-per-AZ, trading AZ-failure resilience for cost. For a hobby/demo you can
  drop NAT entirely by putting tasks in public subnets with tight SGs (covered in the chapter).
- **ALB** — hourly + LCU charges.
- **RDS** — `db.t4g.micro`, single-AZ, gp3, 7-day backups. Single-AZ halves the DB cost vs Multi-AZ.
- **Fargate** — web (1–4 tasks via autoscaling) + 1 worker; you pay per vCPU/GB-second.
- **Mostly usage-priced / near-zero at low volume**: S3, SQS, SES, Secrets Manager, ECR (10-image
  cap), Route53 (per-zone + queries), EventBridge Scheduler.

Cost-discipline levers already baked in: single NAT, small Fargate sizes with CPU-target
autoscaling, RDS storage autoscaling capped at 100 GiB, ECR keep-last-10 lifecycle, 30-day
expiry on raw uploads, and 30-day log retention. Set a budget alarm and run `terraform destroy`
when you're done experimenting.
