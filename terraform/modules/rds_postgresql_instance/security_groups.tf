#------------------------------------------------------------------------------
# RDS Security group
#------------------------------------------------------------------------------
resource "aws_security_group" "psql" {
  name        = "${var.instance_name}-psql"
  description = "Security group for ${var.instance_name} psql"
  vpc_id      = var.vpc_id

  tags = merge(
    var.tags,
    {
      "Name" = var.instance_name
    },
  )
}

resource "aws_security_group_rule" "psql_egress" {
  security_group_id = aws_security_group.psql.id
  type              = "egress"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  cidr_blocks       = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "psql_ingress_self" {
  count             = var.sg_enable_self ? 1 : 0
  security_group_id = aws_security_group.psql.id
  type              = "ingress"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  self              = true
}

resource "aws_security_group_rule" "psql_from_ips" {
  security_group_id = aws_security_group.psql.id
  type              = "ingress"
  from_port         = var.port
  to_port           = var.port
  protocol          = "tcp"
  count             = length(var.allowed_ips)
  cidr_blocks       = [element(var.allowed_ips, count.index)]
}

resource "aws_security_group_rule" "psql_from_sgs" {
  security_group_id        = aws_security_group.psql.id
  type                     = "ingress"
  from_port                = var.port
  to_port                  = var.port
  protocol                 = "tcp"
  count                    = length(var.allowed_sgs)
  source_security_group_id = element(var.allowed_sgs, count.index)
}

output "sg_id" {
  value = aws_security_group.psql.id
}

