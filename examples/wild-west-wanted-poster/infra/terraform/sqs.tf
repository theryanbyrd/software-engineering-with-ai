# sqs.tf — Generation-jobs queue + dead-letter queue with redrive policy (Ch. "Async Work & Queues").

# Dead-letter queue: messages that fail processing maxReceiveCount times land here for inspection.
resource "aws_sqs_queue" "jobs_dlq" {
  name                      = "wwwp-generation-jobs-dlq"
  message_retention_seconds = 1209600 # 14 days

  tags = { Name = "wwwp-jobs-dlq" }
}

# Standard queue carrying {genId,userId,uploadKey} jobs to the worker.
resource "aws_sqs_queue" "jobs" {
  name                       = "wwwp-generation-jobs"
  visibility_timeout_seconds = 300 # > worker max processing time (Gemini + sharp composite)
  message_retention_seconds  = 345600 # 4 days
  receive_wait_time_seconds  = 20     # long polling

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.jobs_dlq.arn
    maxReceiveCount     = 5
  })

  tags = { Name = "wwwp-jobs" }
}

# Allow the DLQ to be a redrive target for the main queue.
resource "aws_sqs_queue_redrive_allow_policy" "dlq" {
  queue_url = aws_sqs_queue.jobs_dlq.id

  redrive_allow_policy = jsonencode({
    redrivePermission = "byQueue"
    sourceQueueArns   = [aws_sqs_queue.jobs.arn]
  })
}
