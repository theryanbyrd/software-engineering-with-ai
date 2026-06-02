# eventbridge-cron.tf — Monthly EventBridge Scheduler that runs the one-off worker-reset ECS task (Ch. "Scheduled Jobs").

# Fires at 00:00 UTC on the 1st of every month. The reset task grants 5 free credits to
# active users, idempotently per (user, YYYY-MM) via the monthly_grants table.
resource "aws_scheduler_schedule" "monthly_credit_reset" {
  name        = "wwwp-monthly-credit-reset"
  group_name  = "default"
  description = "Grant 5 free monthly credits to active users (idempotent per period)."

  schedule_expression          = "cron(0 0 1 * ? *)"
  schedule_expression_timezone = "UTC"

  flexible_time_window {
    mode = "OFF"
  }

  target {
    arn      = aws_ecs_cluster.main.arn
    role_arn = aws_iam_role.scheduler.arn

    ecs_parameters {
      task_definition_arn = aws_ecs_task_definition.worker_reset.arn
      launch_type         = "FARGATE"
      task_count          = 1

      network_configuration {
        subnets          = aws_subnet.private[*].id
        security_groups  = [aws_security_group.worker.id]
        assign_public_ip = false
      }
    }

    retry_policy {
      maximum_retry_attempts       = 2
      maximum_event_age_in_seconds = 3600
    }
  }
}
