resource "aws_rds_cluster_parameter_group" "psql" {
  name        = var.cluster_identifier
  family      = var.param_group_family
  description = "Paramter group for ${var.cluster_identifier}"
  dynamic "parameter" {
    for_each = var.parameters
    content {
      name         = parameter.value.name
      value        = parameter.value.value
      apply_method = lookup(parameter.value, "apply_method", null)
    }
  }
}
