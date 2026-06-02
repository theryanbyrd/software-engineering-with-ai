# outputs.tf — Useful values after apply (Ch. "Infrastructure as Code").

output "alb_dns_name" {
  description = "Public DNS name of the ALB (apex/www alias to this)."
  value       = aws_lb.main.dns_name
}

output "app_url" {
  description = "Public app URL."
  value       = var.app_url
}

output "route53_name_servers" {
  description = "Delegate the registrar's NS records to these to activate the hosted zone."
  value       = aws_route53_zone.main.name_servers
}

output "ses_verified_domain" {
  description = "SES domain identity (verify status visible in the SES console)."
  value       = aws_ses_domain_identity.main.domain
}

output "ecr_web_repository_url" {
  description = "Push the web image here."
  value       = aws_ecr_repository.web.repository_url
}

output "ecr_worker_repository_url" {
  description = "Push the worker image here."
  value       = aws_ecr_repository.worker.repository_url
}

output "uploads_bucket" {
  description = "S3_UPLOAD_BUCKET value."
  value       = aws_s3_bucket.uploads.bucket
}

output "posters_bucket" {
  description = "S3_POSTER_BUCKET value."
  value       = aws_s3_bucket.posters.bucket
}

output "sqs_queue_url" {
  description = "SQS_QUEUE_URL value."
  value       = aws_sqs_queue.jobs.url
}

output "rds_endpoint" {
  description = "RDS endpoint host:port (assembled into DATABASE_URL secret)."
  value       = aws_db_instance.main.endpoint
}

output "ecs_cluster_name" {
  description = "ECS cluster name."
  value       = aws_ecs_cluster.main.name
}

output "secret_arns" {
  description = "Secrets Manager ARNs the app reads (populate the CHANGE-ME ones out-of-band)."
  value = {
    database_url          = aws_secretsmanager_secret.database_url.arn
    auth_secret           = aws_secretsmanager_secret.auth_secret.arn
    stripe_secret_key     = aws_secretsmanager_secret.stripe_secret_key.arn
    stripe_webhook_secret = aws_secretsmanager_secret.stripe_webhook_secret.arn
    gemini_api_key        = aws_secretsmanager_secret.gemini_api_key.arn
  }
}
