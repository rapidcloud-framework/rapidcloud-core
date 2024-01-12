resource "aws_redshift_parameter_group" "redshift" {
  name        = "${var.cluster_name}-parameter-group"
  description = "Paramter group for cluster var.cluster"
  family      = "redshift-1.0"

  dynamic "parameter" {
    for_each = var.parameters
    content {
      name  = parameter.key
      value = parameter.value
    }
  }

  tags = var.tags

}
