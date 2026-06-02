# iam.tf — ECS execution role + least-privilege task roles for web/worker (Ch. "Least-Privilege IAM").

data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

locals {
  account_id = data.aws_caller_identity.current.account_id

  # All secrets the tasks may need to resolve at startup.
  app_secret_arns = [
    aws_secretsmanager_secret.database_url.arn,
    aws_secretsmanager_secret.auth_secret.arn,
    aws_secretsmanager_secret.stripe_secret_key.arn,
    aws_secretsmanager_secret.stripe_webhook_secret.arn,
    aws_secretsmanager_secret.gemini_api_key.arn,
  ]
}

# --- Trust policy shared by all ECS task roles ------------------------------

data "aws_iam_policy_document" "ecs_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

# --- Task EXECUTION role (pull image, write logs, resolve secrets at launch) -

resource "aws_iam_role" "ecs_execution" {
  name               = "wwwp-ecs-execution"
  assume_role_policy = data.aws_iam_policy_document.ecs_assume.json
  tags               = { Name = "wwwp-ecs-execution" }
}

resource "aws_iam_role_policy_attachment" "ecs_execution_managed" {
  role       = aws_iam_role.ecs_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# Execution role also needs to read the secret values referenced in task-def `secrets`.
data "aws_iam_policy_document" "execution_secrets" {
  statement {
    sid       = "ReadAppSecrets"
    actions   = ["secretsmanager:GetSecretValue"]
    resources = local.app_secret_arns
  }
}

resource "aws_iam_role_policy" "execution_secrets" {
  name   = "wwwp-execution-secrets"
  role   = aws_iam_role.ecs_execution.id
  policy = data.aws_iam_policy_document.execution_secrets.json
}

# --- WEB task role ----------------------------------------------------------
# Web handles uploads (put to uploads bucket), reads posters (presign), enqueues jobs,
# sends auth/notification mail, and reads its runtime secrets.

resource "aws_iam_role" "web_task" {
  name               = "wwwp-web-task"
  assume_role_policy = data.aws_iam_policy_document.ecs_assume.json
  tags               = { Name = "wwwp-web-task" }
}

data "aws_iam_policy_document" "web_task" {
  statement {
    sid     = "UploadsReadWrite"
    actions = ["s3:PutObject", "s3:GetObject", "s3:DeleteObject"]
    resources = ["${aws_s3_bucket.uploads.arn}/*"]
  }

  statement {
    sid       = "PostersRead"
    actions   = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.posters.arn}/*"]
  }

  statement {
    sid       = "ListAppBuckets"
    actions   = ["s3:ListBucket"]
    resources = [aws_s3_bucket.uploads.arn, aws_s3_bucket.posters.arn]
  }

  statement {
    sid       = "EnqueueJobs"
    actions   = ["sqs:SendMessage", "sqs:GetQueueAttributes", "sqs:GetQueueUrl"]
    resources = [aws_sqs_queue.jobs.arn]
  }

  statement {
    sid       = "SendEmail"
    actions   = ["ses:SendEmail", "ses:SendRawEmail"]
    resources = [aws_ses_domain_identity.main.arn]
    condition {
      test     = "StringEquals"
      variable = "ses:FromAddress"
      values   = [var.ses_from_email]
    }
  }

  statement {
    sid       = "ReadSecrets"
    actions   = ["secretsmanager:GetSecretValue"]
    resources = local.app_secret_arns
  }
}

resource "aws_iam_role_policy" "web_task" {
  name   = "wwwp-web-task-policy"
  role   = aws_iam_role.web_task.id
  policy = data.aws_iam_policy_document.web_task.json
}

# --- WORKER task role -------------------------------------------------------
# Worker reads the raw upload, writes the finished poster, consumes/deletes jobs,
# sends "poster ready" mail, and may run the monthly reset task.

resource "aws_iam_role" "worker_task" {
  name               = "wwwp-worker-task"
  assume_role_policy = data.aws_iam_policy_document.ecs_assume.json
  tags               = { Name = "wwwp-worker-task" }
}

data "aws_iam_policy_document" "worker_task" {
  statement {
    sid       = "ReadUploads"
    actions   = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.uploads.arn}/*"]
  }

  statement {
    sid     = "WritePosters"
    actions = ["s3:PutObject", "s3:GetObject"]
    resources = ["${aws_s3_bucket.posters.arn}/*"]
  }

  statement {
    sid       = "ListAppBuckets"
    actions   = ["s3:ListBucket"]
    resources = [aws_s3_bucket.uploads.arn, aws_s3_bucket.posters.arn]
  }

  statement {
    sid     = "ConsumeJobs"
    actions = [
      "sqs:ReceiveMessage",
      "sqs:DeleteMessage",
      "sqs:GetQueueAttributes",
      "sqs:GetQueueUrl",
      "sqs:ChangeMessageVisibility",
    ]
    resources = [aws_sqs_queue.jobs.arn]
  }

  statement {
    sid       = "SendEmail"
    actions   = ["ses:SendEmail", "ses:SendRawEmail"]
    resources = [aws_ses_domain_identity.main.arn]
    condition {
      test     = "StringEquals"
      variable = "ses:FromAddress"
      values   = [var.ses_from_email]
    }
  }

  statement {
    sid       = "ReadSecrets"
    actions   = ["secretsmanager:GetSecretValue"]
    resources = local.app_secret_arns
  }
}

resource "aws_iam_role_policy" "worker_task" {
  name   = "wwwp-worker-task-policy"
  role   = aws_iam_role.worker_task.id
  policy = data.aws_iam_policy_document.worker_task.json
}

# --- EventBridge Scheduler role (run the monthly-reset ECS task) ------------

data "aws_iam_policy_document" "scheduler_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["scheduler.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "scheduler" {
  name               = "wwwp-scheduler"
  assume_role_policy = data.aws_iam_policy_document.scheduler_assume.json
  tags               = { Name = "wwwp-scheduler" }
}

data "aws_iam_policy_document" "scheduler" {
  statement {
    sid       = "RunResetTask"
    actions   = ["ecs:RunTask"]
    # Match every revision of the worker-reset task-definition family.
    resources = ["arn:aws:ecs:${data.aws_region.current.name}:${local.account_id}:task-definition/${aws_ecs_task_definition.worker_reset.family}:*"]
    condition {
      test     = "ArnLike"
      variable = "ecs:cluster"
      values   = [aws_ecs_cluster.main.arn]
    }
  }

  # Scheduler must pass the execution + task roles to the one-off task.
  statement {
    sid       = "PassRoles"
    actions   = ["iam:PassRole"]
    resources = [aws_iam_role.ecs_execution.arn, aws_iam_role.worker_task.arn]
    condition {
      test     = "StringEquals"
      variable = "iam:PassedToService"
      values   = ["ecs-tasks.amazonaws.com"]
    }
  }
}

resource "aws_iam_role_policy" "scheduler" {
  name   = "wwwp-scheduler-policy"
  role   = aws_iam_role.scheduler.id
  policy = data.aws_iam_policy_document.scheduler.json
}
