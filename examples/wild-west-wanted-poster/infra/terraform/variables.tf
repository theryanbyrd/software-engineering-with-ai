# variables.tf — Input variables for the wwwp infrastructure (Ch. "Infrastructure as Code").

variable "aws_region" {
  description = "AWS region for all resources."
  type        = string
  default     = "us-west-2"
}

variable "environment" {
  description = "Deployment environment label (e.g. prod, staging)."
  type        = string
  default     = "prod"
}

variable "domain_name" {
  description = "Apex domain for the app."
  type        = string
  default     = "wildwestwanted.com"
}

variable "app_url" {
  description = "Public base URL the app serves from (APP_URL env var)."
  type        = string
  default     = "https://wildwestwanted.com"
}

# --- Networking -------------------------------------------------------------

variable "vpc_cidr" {
  description = "CIDR block for the VPC."
  type        = string
  default     = "10.20.0.0/16"
}

variable "az_count" {
  description = "Number of Availability Zones to span (public + private subnet per AZ)."
  type        = number
  default     = 2
}

# --- Database ---------------------------------------------------------------

variable "db_name" {
  description = "Initial PostgreSQL database name."
  type        = string
  default     = "wwwp"
}

variable "db_username" {
  description = "Master username for the RDS instance."
  type        = string
  default     = "wwwp_app"
}

variable "db_instance_class" {
  description = "RDS instance class. db.t4g.micro keeps the worked example cheap."
  type        = string
  default     = "db.t4g.micro"
}

variable "db_allocated_storage" {
  description = "Allocated storage (GiB) for RDS."
  type        = number
  default     = 20
}

variable "db_engine_version" {
  description = "PostgreSQL engine version."
  type        = string
  default     = "16.4"
}

# --- Container images -------------------------------------------------------

variable "web_image_tag" {
  description = "Image tag to deploy for the web service."
  type        = string
  default     = "latest"
}

variable "worker_image_tag" {
  description = "Image tag to deploy for the worker service."
  type        = string
  default     = "latest"
}

variable "web_desired_count" {
  description = "Baseline number of web tasks."
  type        = number
  default     = 1
}

variable "web_cpu" {
  description = "Fargate CPU units for the web task."
  type        = number
  default     = 512
}

variable "web_memory" {
  description = "Fargate memory (MiB) for the web task."
  type        = number
  default     = 1024
}

variable "worker_cpu" {
  description = "Fargate CPU units for the worker task."
  type        = number
  default     = 512
}

variable "worker_memory" {
  description = "Fargate memory (MiB) for the worker task."
  type        = number
  default     = 1024
}

variable "web_min_capacity" {
  description = "Minimum web task count for autoscaling."
  type        = number
  default     = 1
}

variable "web_max_capacity" {
  description = "Maximum web task count for autoscaling."
  type        = number
  default     = 4
}

# --- App configuration ------------------------------------------------------

variable "ses_from_email" {
  description = "From address for outbound mail (SES_FROM_EMAIL)."
  type        = string
  default     = "noreply@wildwestwanted.com"
}

variable "admin_emails" {
  description = "Comma-separated admin email list (ADMIN_EMAILS)."
  type        = string
  default     = ""
}

variable "stripe_price_credits" {
  description = "Stripe Price ID for the $1 / 10-credit pack (STRIPE_PRICE_CREDITS)."
  type        = string
  default     = ""
}

variable "alert_email" {
  description = "Email subscribed to the CloudWatch alarm / ops SNS topic."
  type        = string
  default     = "ops@wildwestwanted.com"
}

variable "log_retention_days" {
  description = "CloudWatch Logs retention in days."
  type        = number
  default     = 30
}
