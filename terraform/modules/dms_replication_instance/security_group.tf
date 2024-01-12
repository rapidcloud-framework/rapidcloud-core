resource "aws_security_group" "dms_security_group" {
  name        = "${var.replication_instance_id}-sg"
  description = "Security Group for ${var.replication_instance_id} Replication Instance"
  vpc_id      = var.vpc_id
  tags        = merge(var.tags, tomap({"Name" = "${var.replication_instance_id}-sg"}))
}

resource "aws_security_group_rule" "dms_self_ingress" {
  security_group_id = aws_security_group.dms_security_group.id
  type              = "ingress"
  from_port         = 0
  to_port           = 0
  protocol          = -1
  self              = true
}

resource "aws_security_group_rule" "cidr_ingress" {
  for_each          = var.cidr_ingress_rules
  security_group_id = aws_security_group.dms_security_group.id
  type              = "ingress"
  description       = each.key
  from_port         = element(split(",", each.value), 0)
  to_port           = element(split(",", each.value), 1)
  protocol          = element(split(",", each.value), 2)
  cidr_blocks       = [element(split(",", each.value), 3)]
}

resource "aws_security_group_rule" "cidr_egress" {
  for_each          = var.cidr_egress_rules
  security_group_id = aws_security_group.dms_security_group.id
  type              = "egress"
  description       = each.key
  from_port         = element(split(",", each.value), 0)
  to_port           = element(split(",", each.value), 1)
  protocol          = element(split(",", each.value), 2)
  cidr_blocks       = [element(split(",", each.value), 3)]
}

resource "aws_security_group_rule" "sg_ingress" {
  for_each                 = var.sg_ingress_rules
  security_group_id        = aws_security_group.dms_security_group.id
  type                     = "ingress"
  description              = each.key
  from_port                = element(split(",", each.value), 0)
  to_port                  = element(split(",", each.value), 1)
  protocol                 = element(split(",", each.value), 2)
  source_security_group_id = element(split(",", each.value), 3)
}

resource "aws_security_group_rule" "sg_egress" {
  for_each                 = var.sg_egress_rules
  security_group_id        = aws_security_group.dms_security_group.id
  type                     = "egress"
  description              = each.key
  from_port                = element(split(",", each.value), 0)
  to_port                  = element(split(",", each.value), 1)
  protocol                 = element(split(",", each.value), 2)
  source_security_group_id = element(split(",", each.value), 3)
}
