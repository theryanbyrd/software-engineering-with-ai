# backend.tf — Remote state config (S3 + DynamoDB lock). Commented example (Ch. "Cost Discipline & State").

# Remote state keeps the wwwp state file off your laptop and lets the lock table prevent
# two `terraform apply` runs from racing. Create the bucket + table ONCE (out of band, or
# in a tiny bootstrap module) before uncommenting this block, then run `terraform init`.
#
# Bootstrap (run once, manually):
#   aws s3api create-bucket --bucket wwwp-tfstate-<your-account-id> \
#     --region us-west-2 --create-bucket-configuration LocationConstraint=us-west-2
#   aws s3api put-bucket-versioning --bucket wwwp-tfstate-<your-account-id> \
#     --versioning-configuration Status=Enabled
#   aws dynamodb create-table --table-name wwwp-tfstate-lock \
#     --attribute-definitions AttributeName=LockID,AttributeType=S \
#     --key-schema AttributeName=LockID,KeyType=HASH \
#     --billing-mode PAY_PER_REQUEST --region us-west-2

# terraform {
#   backend "s3" {
#     bucket         = "wwwp-tfstate-<your-account-id>"
#     key            = "wild-west-wanted-poster/terraform.tfstate"
#     region         = "us-west-2"
#     dynamodb_table = "wwwp-tfstate-lock"
#     encrypt        = true
#   }
# }
