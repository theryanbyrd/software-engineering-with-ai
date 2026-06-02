# s3.tf — Private uploads + posters buckets (block public access, SSE, raw-upload lifecycle) (Ch. "Object Storage").

resource "random_id" "bucket_suffix" {
  byte_length = 4
}

locals {
  uploads_bucket_name = "wwwp-uploads-${random_id.bucket_suffix.hex}"
  posters_bucket_name = "wwwp-posters-${random_id.bucket_suffix.hex}"
}

# --- Uploads bucket (raw photos) -------------------------------------------

resource "aws_s3_bucket" "uploads" {
  bucket = local.uploads_bucket_name
  tags   = { Name = "wwwp-uploads" }
}

resource "aws_s3_bucket_public_access_block" "uploads" {
  bucket                  = aws_s3_bucket.uploads.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "uploads" {
  bucket = aws_s3_bucket.uploads.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Raw uploads are only needed until the poster is generated; expire after 30 days.
resource "aws_s3_bucket_lifecycle_configuration" "uploads" {
  bucket = aws_s3_bucket.uploads.id

  rule {
    id     = "expire-raw-uploads"
    status = "Enabled"

    filter {
      prefix = "uploads/"
    }

    expiration {
      days = 30
    }

    abort_incomplete_multipart_upload {
      days_after_initiation = 7
    }
  }
}

# --- Posters bucket (generated, served via presigned URLs) ------------------

resource "aws_s3_bucket" "posters" {
  bucket = local.posters_bucket_name
  tags   = { Name = "wwwp-posters" }
}

resource "aws_s3_bucket_public_access_block" "posters" {
  bucket                  = aws_s3_bucket.posters.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "posters" {
  bucket = aws_s3_bucket.posters.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Posters are durable assets; CORS lets the browser fetch them via presigned URLs.
resource "aws_s3_bucket_cors_configuration" "posters" {
  bucket = aws_s3_bucket.posters.id

  cors_rule {
    allowed_methods = ["GET"]
    allowed_origins = [var.app_url]
    allowed_headers = ["*"]
    max_age_seconds = 3600
  }
}
