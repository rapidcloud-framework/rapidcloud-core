resource "aws_security_group" "emr_master" {
  name                   = "${var.cluster_name}-master"
  vpc_id                 = var.vpc_id
  revoke_rules_on_delete = "true"

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group_rule" "emr_master_to_master" {
  type                     = "ingress"
  from_port                = 0
  to_port                  = 65535
  protocol                 = "-1"
  source_security_group_id = aws_security_group.emr_master.id
  security_group_id        = aws_security_group.emr_master.id
}

resource "aws_security_group_rule" "emr_master_to_core" {
  type                     = "ingress"
  from_port                = 0
  to_port                  = 65535
  protocol                 = "-1"
  source_security_group_id = aws_security_group.emr_master.id
  security_group_id        = aws_security_group.emr_core.id
}

resource "aws_security_group" "emr_core" {
  name                   = "${var.cluster_name}-core"
  vpc_id                 = var.vpc_id
  revoke_rules_on_delete = "true"

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group_rule" "emr_core_to_core" {
  type                     = "ingress"
  from_port                = 0
  to_port                  = 65535
  protocol                 = "-1"
  source_security_group_id = aws_security_group.emr_core.id
  security_group_id        = aws_security_group.emr_core.id
}

resource "aws_security_group_rule" "emr_core_to_master" {
  type                     = "ingress"
  from_port                = 0
  to_port                  = 65535
  protocol                 = "-1"
  source_security_group_id = aws_security_group.emr_core.id
  security_group_id        = aws_security_group.emr_master.id
}

resource "aws_security_group" "emr_service_access" {
  count                  = var.access_type == "private" ? 1 : 0
  name                   = "${var.cluster_name}-service-access"
  vpc_id                 = var.vpc_id
  revoke_rules_on_delete = "true"

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  lifecycle {
    ignore_changes = [egress]
  }
}

resource "aws_security_group_rule" "emr_master_to_service" {
  count                    = var.access_type == "private" ? 1 : 0
  type                     = "ingress"
  from_port                = 9443
  to_port                  = 9443
  protocol                 = "tcp"
  source_security_group_id = aws_security_group.emr_master.id
  security_group_id        = aws_security_group.emr_service_access.0.id
}

resource "aws_security_group_rule" "emr_master_cidr_ingress" {
  security_group_id = aws_security_group.emr_master.id
  count             = length(var.master_cidr_ingress_rules)
  type              = "ingress"
  from_port         = element(split(":", element(var.master_cidr_ingress_rules, count.index)), 0)
  to_port           = element(split(":", element(var.master_cidr_ingress_rules, count.index)), 1)
  protocol          = element(split(":", element(var.master_cidr_ingress_rules, count.index)), 2)
  cidr_blocks       = [element(split(":", element(var.master_cidr_ingress_rules, count.index)), 3)]
}

resource "aws_security_group_rule" "emr_master_sg_ingress" {
  security_group_id        = aws_security_group.emr_master.id
  count                    = length(var.master_sg_ingress_rules)
  type                     = "ingress"
  from_port                = element(split(":", element(var.master_sg_ingress_rules, count.index)), 0)
  to_port                  = element(split(":", element(var.master_sg_ingress_rules, count.index)), 1)
  protocol                 = element(split(":", element(var.master_sg_ingress_rules, count.index)), 2)
  source_security_group_id = element(split(":", element(var.master_sg_ingress_rules, count.index)), 3)
}

resource "aws_security_group_rule" "emr_core_cidr_ingress" {
  security_group_id = aws_security_group.emr_core.id
  count             = length(var.core_cidr_ingress_rules)
  type              = "ingress"
  from_port         = element(split(":", element(var.core_cidr_ingress_rules, count.index)), 0)
  to_port           = element(split(":", element(var.core_cidr_ingress_rules, count.index)), 1)
  protocol          = element(split(":", element(var.core_cidr_ingress_rules, count.index)), 2)
  cidr_blocks       = [element(split(":", element(var.core_cidr_ingress_rules, count.index)), 3)]
}

resource "aws_security_group_rule" "emr_core_sg_ingress" {
  security_group_id        = aws_security_group.emr_core.id
  count                    = length(var.core_sg_ingress_rules)
  type                     = "ingress"
  from_port                = element(split(":", element(var.core_sg_ingress_rules, count.index)), 0)
  to_port                  = element(split(":", element(var.core_sg_ingress_rules, count.index)), 1)
  protocol                 = element(split(":", element(var.core_sg_ingress_rules, count.index)), 2)
  source_security_group_id = element(split(":", element(var.core_sg_ingress_rules, count.index)), 3)
}
