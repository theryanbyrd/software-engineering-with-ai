# providers.tf — AWS provider config + version pins for the wwwp deployment (Ch. "Infrastructure as Code").

terraform {
  required_version = ">= 1.6"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.40"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      project     = "wild-west-wanted-poster"
      environment = var.environment
      managed_by  = "terraform"
    }
  }
}

# ACM certificates consumed by CloudFront would need us-east-1; the ALB cert lives in
# the app region, so the default provider is sufficient here. Aliased provider kept for
# clarity / future edge work.
provider "aws" {
  alias  = "us_east_1"
  region = "us-east-1"

  default_tags {
    tags = {
      project     = "wild-west-wanted-poster"
      environment = var.environment
      managed_by  = "terraform"
    }
  }
}
