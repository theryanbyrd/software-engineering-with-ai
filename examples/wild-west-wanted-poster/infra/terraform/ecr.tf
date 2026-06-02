# ecr.tf — ECR repos for the web and worker images, with scan-on-push + lifecycle pruning (Ch. "Build & Registry").

resource "aws_ecr_repository" "web" {
  name                 = "wwwp/web"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = { Name = "wwwp-ecr-web" }
}

resource "aws_ecr_repository" "worker" {
  name                 = "wwwp/worker"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = { Name = "wwwp-ecr-worker" }
}

# Keep only the most recent 10 images per repo so the registry bill stays flat.
locals {
  ecr_lifecycle_policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Keep last 10 images"
        selection = {
          tagStatus   = "any"
          countType   = "imageCountMoreThan"
          countNumber = 10
        }
        action = { type = "expire" }
      }
    ]
  })
}

resource "aws_ecr_lifecycle_policy" "web" {
  repository = aws_ecr_repository.web.name
  policy     = local.ecr_lifecycle_policy
}

resource "aws_ecr_lifecycle_policy" "worker" {
  repository = aws_ecr_repository.worker.name
  policy     = local.ecr_lifecycle_policy
}
