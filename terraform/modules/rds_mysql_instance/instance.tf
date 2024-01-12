#------------------------------------------------------------------------------
# Data Section
#------------------------------------------------------------------------------
# Define and associate subnets to db subnets group
resource "aws_db_subnet_group" "mysql" {
  name        = var.instance_name
  description = "Allowed subnets for Aurora DB cluster instances"
  subnet_ids  = var.db_subnets

  tags = merge(
    var.tags,
    {
      "Name" = var.instance_name
    },
  )
}

resource "aws_db_instance" "mysql" {
  # engine options
  engine         = "mysql"
  engine_version = var.engine_version

  # settings
  identifier = var.instance_name
  username   = var.database_username
  password   = var.database_password
  db_name       = var.database_name

  instance_class                  = var.instance_class
  storage_type                    = var.storage_type
  allocated_storage               = var.allocated_storage
  max_allocated_storage           = var.max_allocated_storage != "" ? var.max_allocated_storage : var.allocated_storage + 1
  backup_retention_period         = var.backup_retention_period
  enabled_cloudwatch_logs_exports = var.enabled_cloudwatch_logs_exports
  monitoring_interval             = var.monitoring_interval
  monitoring_role_arn             = aws_iam_role.mysql.arn
  skip_final_snapshot             = true


  publicly_accessible    = false
  multi_az               = var.multi_az
  db_subnet_group_name   = aws_db_subnet_group.mysql.name
  parameter_group_name   = aws_db_parameter_group.mysql.name
  vpc_security_group_ids = [aws_security_group.mysql.id]

  tags = merge(
    var.tags,
    {
      "Name" = var.instance_name
    },
  )

  lifecycle {
    create_before_destroy = true
  }

  timeouts {
    create = "60m"
  }
}

#------------------------------------------------------------------------------
# Outputs
#------------------------------------------------------------------------------
output "endpoint" {
  value = aws_db_instance.mysql.endpoint
}

output "id" {
  value = aws_db_instance.mysql.id
}

output "port" {
  value = aws_db_instance.mysql.port
}

