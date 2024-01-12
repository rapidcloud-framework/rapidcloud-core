resource "aws_db_parameter_group" "mysql" {
  name   = var.instance_name
  family = var.param_group_family
  dynamic "parameter" {
    for_each = var.parameters
    content {
      name         = parameter.value.name
      value        = parameter.value.value
      apply_method = lookup(parameter.value, "apply_method", null)
    }
  }
}

