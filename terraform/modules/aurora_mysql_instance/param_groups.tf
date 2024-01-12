resource "aws_rds_cluster_parameter_group" "rds_cluster" {
  name        = var.cluster_identifier
  description = "RDS cluster parameter group for ${var.cluster_identifier}"
  family      = var.param_group_family

  dynamic "parameter" {
    for_each = var.parameters
    content {
      name         = parameter.value.name
      value        = parameter.value.value
      apply_method = lookup(parameter.value, "apply_method", null)
    }
  }
}

resource "aws_db_parameter_group" "rds_db" {
  description = "RDS DB parameter group for ${var.cluster_identifier}"
  name        = var.cluster_identifier
  family      = var.param_group_family
}

