#------------------------------------------------------------------------------
# RDS Security group
#------------------------------------------------------------------------------
resource "aws_security_group" "mysql" {
  name        = var.cluster_identifier
  description = "Allow 3306"
  vpc_id      = var.vpc_id

  tags = merge(
    var.tags,
    {
      "Name" = var.cluster_identifier
    },
  )
}

resource "aws_security_group_rule" "mysql_egress" {
  security_group_id = aws_security_group.mysql.id
  type              = "egress"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  cidr_blocks       = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "mysql_from_ips" {
  security_group_id = aws_security_group.mysql.id
  type              = "ingress"
  from_port         = var.port
  to_port           = var.port
  protocol          = "tcp"
  count             = length(var.allowed_ips)
  cidr_blocks       = [element(var.allowed_ips, count.index)]
}

resource "aws_security_group_rule" "mysql_from_sgs" {
  security_group_id        = aws_security_group.mysql.id
  type                     = "ingress"
  from_port                = var.port
  to_port                  = var.port
  protocol                 = "tcp"
  count                    = length(var.allowed_sgs)
  source_security_group_id = element(var.allowed_sgs, count.index)
}

