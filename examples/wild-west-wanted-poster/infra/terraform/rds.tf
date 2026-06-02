# rds.tf — RDS PostgreSQL 16 in private subnets, SG, subnet/parameter groups, generated password (Ch. "Relational Data").

resource "aws_db_subnet_group" "main" {
  name       = "wwwp-db-subnets"
  subnet_ids = aws_subnet.private[*].id
  tags       = { Name = "wwwp-db-subnets" }
}

# Postgres reachable only from the web + worker task SGs.
resource "aws_security_group" "rds" {
  name        = "wwwp-rds-sg"
  description = "Postgres access from app tasks only."
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "Postgres from web"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.web.id]
  }

  ingress {
    description     = "Postgres from worker"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.worker.id]
  }

  egress {
    description = "All outbound"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = { Name = "wwwp-rds-sg" }
}

resource "aws_db_parameter_group" "main" {
  name   = "wwwp-pg16"
  family = "postgres16"

  # citext is used for users.email (case-insensitive unique); ensure logging of slow queries.
  parameter {
    name  = "log_min_duration_statement"
    value = "500"
  }

  tags = { Name = "wwwp-pg16" }
}

resource "aws_db_instance" "main" {
  identifier     = "wwwp-postgres"
  engine         = "postgres"
  engine_version = var.db_engine_version
  instance_class = var.db_instance_class

  allocated_storage     = var.db_allocated_storage
  max_allocated_storage = 100 # storage autoscaling cap
  storage_type          = "gp3"
  storage_encrypted     = true

  db_name  = var.db_name
  username = var.db_username
  # Password sourced from the generated Secrets Manager secret (see secrets.tf).
  password = random_password.db.result

  db_subnet_group_name   = aws_db_subnet_group.main.name
  parameter_group_name   = aws_db_parameter_group.main.name
  vpc_security_group_ids = [aws_security_group.rds.id]

  multi_az            = false # single-AZ for the worked example; flip to true for prod HA
  publicly_accessible = false

  backup_retention_period   = 7
  skip_final_snapshot       = true
  final_snapshot_identifier = null
  deletion_protection       = false # set true for real production
  apply_immediately         = true

  performance_insights_enabled = true

  tags = { Name = "wwwp-postgres" }
}
