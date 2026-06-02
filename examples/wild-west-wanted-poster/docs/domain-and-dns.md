# Domain & DNS (Phase 0)

Goal: `https://wildwestwanted.com` and `https://www.wildwestwanted.com` resolve to the ALB
with a valid TLS cert, fully managed by Terraform.

1. **Register the domain.** Either register directly in Route53 (zone is created for you),
   or register at any registrar and delegate to the Route53 hosted zone Terraform creates.
2. **Hosted zone** — `infra/terraform/dns.tf` creates the zone and outputs `name_servers`.
   If the domain is external, paste those NS records at your registrar and wait for
   propagation (minutes to a few hours).
3. **ACM certificate** — a DNS-validated cert for the apex + `www`. Terraform creates the
   `_acme`/validation CNAMEs in the zone automatically, so validation completes without
   manual steps once delegation is live.
4. **Alias records** — A/AAAA alias records for apex and `www` point at the ALB.
5. **HTTPS** — the ALB listener uses the validated cert; HTTP :80 issues a 301 to :443
   (`alb.tf`).

Gotcha: ACM validation can't complete until NS delegation is in place, so `terraform apply`
may sit on the cert resource until your registrar change propagates. That's expected.
