# ecs.tf — ECS Fargate cluster, web (behind ALB) + worker services, logs, web autoscaling (Ch. "Running Containers").

resource "aws_ecs_cluster" "main" {
  name = "wwwp"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }

  tags = { Name = "wwwp-cluster" }
}

# --- CloudWatch log groups --------------------------------------------------

resource "aws_cloudwatch_log_group" "web" {
  name              = "/ecs/wwwp/web"
  retention_in_days = var.log_retention_days
  tags              = { Name = "wwwp-web-logs" }
}

resource "aws_cloudwatch_log_group" "worker" {
  name              = "/ecs/wwwp/worker"
  retention_in_days = var.log_retention_days
  tags              = { Name = "wwwp-worker-logs" }
}

# --- Shared env + secrets injected into both services ----------------------

locals {
  common_environment = [
    { name = "APP_URL", value = var.app_url },
    { name = "AWS_REGION", value = var.aws_region },
    { name = "S3_UPLOAD_BUCKET", value = aws_s3_bucket.uploads.bucket },
    { name = "S3_POSTER_BUCKET", value = aws_s3_bucket.posters.bucket },
    { name = "SQS_QUEUE_URL", value = aws_sqs_queue.jobs.url },
    { name = "SES_FROM_EMAIL", value = var.ses_from_email },
    { name = "ADMIN_EMAILS", value = var.admin_emails },
    { name = "STRIPE_PRICE_CREDITS", value = var.stripe_price_credits },
  ]

  # Secrets Manager ARNs surfaced as env vars by ECS at container start.
  common_secrets = [
    { name = "DATABASE_URL", valueFrom = aws_secretsmanager_secret.database_url.arn },
    { name = "AUTH_SECRET", valueFrom = aws_secretsmanager_secret.auth_secret.arn },
    { name = "STRIPE_SECRET_KEY", valueFrom = aws_secretsmanager_secret.stripe_secret_key.arn },
    { name = "STRIPE_WEBHOOK_SECRET", valueFrom = aws_secretsmanager_secret.stripe_webhook_secret.arn },
    { name = "GEMINI_API_KEY", valueFrom = aws_secretsmanager_secret.gemini_api_key.arn },
  ]
}

# --- WEB task definition + service -----------------------------------------

resource "aws_ecs_task_definition" "web" {
  family                   = "wwwp-web"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = var.web_cpu
  memory                   = var.web_memory
  execution_role_arn       = aws_iam_role.ecs_execution.arn
  task_role_arn            = aws_iam_role.web_task.arn

  container_definitions = jsonencode([
    {
      name      = "web"
      image     = "${aws_ecr_repository.web.repository_url}:${var.web_image_tag}"
      essential = true
      portMappings = [
        { containerPort = 3000, protocol = "tcp" }
      ]
      environment = local.common_environment
      secrets     = local.common_secrets
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.web.name
          "awslogs-region"        = var.aws_region
          "awslogs-stream-prefix" = "web"
        }
      }
    }
  ])

  tags = { Name = "wwwp-web-taskdef" }
}

resource "aws_ecs_service" "web" {
  name            = "wwwp-web"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.web.arn
  desired_count   = var.web_desired_count
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = aws_subnet.private[*].id
    security_groups  = [aws_security_group.web.id]
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.web.arn
    container_name   = "web"
    container_port   = 3000
  }

  # Let autoscaling own desired_count after the first deploy.
  lifecycle {
    ignore_changes = [desired_count]
  }

  depends_on = [aws_lb_listener.https]

  tags = { Name = "wwwp-web-svc" }
}

# --- WORKER task definition + service --------------------------------------

resource "aws_ecs_task_definition" "worker" {
  family                   = "wwwp-worker"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = var.worker_cpu
  memory                   = var.worker_memory
  execution_role_arn       = aws_iam_role.ecs_execution.arn
  task_role_arn            = aws_iam_role.worker_task.arn

  container_definitions = jsonencode([
    {
      name        = "worker"
      image       = "${aws_ecr_repository.worker.repository_url}:${var.worker_image_tag}"
      essential   = true
      command     = ["node", "dist/index.js"]
      environment = local.common_environment
      secrets     = local.common_secrets
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.worker.name
          "awslogs-region"        = var.aws_region
          "awslogs-stream-prefix" = "worker"
        }
      }
    }
  ])

  tags = { Name = "wwwp-worker-taskdef" }
}

resource "aws_ecs_service" "worker" {
  name            = "wwwp-worker"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.worker.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = aws_subnet.private[*].id
    security_groups  = [aws_security_group.worker.id]
    assign_public_ip = false
  }

  tags = { Name = "wwwp-worker-svc" }
}

# --- One-off "monthly reset" task definition (run by EventBridge Scheduler) -
# Reuses the worker image but runs the reset entrypoint; not a long-running service.

resource "aws_ecs_task_definition" "worker_reset" {
  family                   = "wwwp-worker-reset"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = var.worker_cpu
  memory                   = var.worker_memory
  execution_role_arn       = aws_iam_role.ecs_execution.arn
  task_role_arn            = aws_iam_role.worker_task.arn

  container_definitions = jsonencode([
    {
      name      = "worker-reset"
      image     = "${aws_ecr_repository.worker.repository_url}:${var.worker_image_tag}"
      essential = true
      command   = ["node", "dist/index.js"]
      environment = concat(local.common_environment, [
        { name = "WORKER_MODE", value = "reset" } # worker branches on WORKER_MODE=reset
      ])
      secrets = local.common_secrets
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.worker.name
          "awslogs-region"        = var.aws_region
          "awslogs-stream-prefix" = "worker-reset"
        }
      }
    }
  ])

  tags = { Name = "wwwp-worker-reset-taskdef" }
}

# --- Web service autoscaling (target tracking on CPU) ----------------------

resource "aws_appautoscaling_target" "web" {
  max_capacity       = var.web_max_capacity
  min_capacity       = var.web_min_capacity
  resource_id        = "service/${aws_ecs_cluster.main.name}/${aws_ecs_service.web.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}

resource "aws_appautoscaling_policy" "web_cpu" {
  name               = "wwwp-web-cpu-target"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.web.resource_id
  scalable_dimension = aws_appautoscaling_target.web.scalable_dimension
  service_namespace  = aws_appautoscaling_target.web.service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }
    target_value       = 60
    scale_in_cooldown  = 120
    scale_out_cooldown = 60
  }
}
