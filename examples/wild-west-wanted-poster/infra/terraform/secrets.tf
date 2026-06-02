# secrets.tf — Secrets Manager entries; ECS injects these as env via task-def `secrets` (Ch. "Secrets Management").

# IMPORTANT: Terraform creates the secret *containers* here. Real values must be populated
# out-of-band so they never touch state or git, e.g.:
#   aws secretsmanager put-secret-value --secret-id wwwp/stripe-secret-key \
#     --secret-string 'sk_live_...'
# The exceptions are DATABASE_URL (assembled from the RDS endpoint + generated password)
# and the auto-generated DB password / AUTH_SECRET, which we can manage safely.

# --- Generated DB master password ------------------------------------------

resource "random_password" "db" {
  length  = 32
  special = false # avoid URL-encoding headaches in DATABASE_URL
}

resource "aws_secretsmanager_secret" "db_password" {
  name        = "wwwp/db-password"
  description = "RDS master password for wwwp."
  tags        = { Name = "wwwp-db-password" }
}

resource "aws_secretsmanager_secret_version" "db_password" {
  secret_id     = aws_secretsmanager_secret.db_password.id
  secret_string = random_password.db.result
}

# --- DATABASE_URL (assembled) ----------------------------------------------

resource "aws_secretsmanager_secret" "database_url" {
  name        = "wwwp/database-url"
  description = "Postgres connection string (DATABASE_URL)."
  tags        = { Name = "wwwp-database-url" }
}

resource "aws_secretsmanager_secret_version" "database_url" {
  secret_id = aws_secretsmanager_secret.database_url.id
  secret_string = format(
    "postgresql://%s:%s@%s:%d/%s?sslmode=require",
    var.db_username,
    random_password.db.result,
    aws_db_instance.main.address,
    aws_db_instance.main.port,
    var.db_name,
  )
}

# --- AUTH_SECRET (generated; used to sign session JWTs) --------------------

resource "random_password" "auth_secret" {
  length  = 48
  special = false
}

resource "aws_secretsmanager_secret" "auth_secret" {
  name        = "wwwp/auth-secret"
  description = "JWT signing secret (AUTH_SECRET)."
  tags        = { Name = "wwwp-auth-secret" }
}

resource "aws_secretsmanager_secret_version" "auth_secret" {
  secret_id     = aws_secretsmanager_secret.auth_secret.id
  secret_string = random_password.auth_secret.result
}

# --- Externally-supplied secrets (create empty; populate via CLI) ----------

resource "aws_secretsmanager_secret" "stripe_secret_key" {
  name        = "wwwp/stripe-secret-key"
  description = "STRIPE_SECRET_KEY. Populate with `aws secretsmanager put-secret-value`."
  tags        = { Name = "wwwp-stripe-secret-key" }
}

resource "aws_secretsmanager_secret" "stripe_webhook_secret" {
  name        = "wwwp/stripe-webhook-secret"
  description = "STRIPE_WEBHOOK_SECRET. Populate after creating the Stripe webhook endpoint."
  tags        = { Name = "wwwp-stripe-webhook-secret" }
}

resource "aws_secretsmanager_secret" "gemini_api_key" {
  name        = "wwwp/gemini-api-key"
  description = "GEMINI_API_KEY for @google/genai. Populate out-of-band."
  tags        = { Name = "wwwp-gemini-api-key" }
}

# Placeholder versions so ECS can resolve the ARN on first deploy. Replace the value
# immediately — these CHANGE-ME strings will not work against the real APIs.
resource "aws_secretsmanager_secret_version" "stripe_secret_key" {
  secret_id     = aws_secretsmanager_secret.stripe_secret_key.id
  secret_string = "CHANGE-ME"

  lifecycle {
    ignore_changes = [secret_string] # so manual rotation isn't reverted by apply
  }
}

resource "aws_secretsmanager_secret_version" "stripe_webhook_secret" {
  secret_id     = aws_secretsmanager_secret.stripe_webhook_secret.id
  secret_string = "CHANGE-ME"

  lifecycle {
    ignore_changes = [secret_string]
  }
}

resource "aws_secretsmanager_secret_version" "gemini_api_key" {
  secret_id     = aws_secretsmanager_secret.gemini_api_key.id
  secret_string = "CHANGE-ME"

  lifecycle {
    ignore_changes = [secret_string]
  }
}
