resource "aws_security_group" "msk" {
  name   = var.cluster_name
  vpc_id = var.vpc_id
  tags   = merge(var.tags, tomap({"Name" = "${var.cluster_name}-msk-cluster"}))
}

resource "aws_security_group_rule" "kafka" {
  from_port         = 9092
  to_port           = 9092
  protocol          = "tcp"
  security_group_id = aws_security_group.msk.id
  type              = "ingress"
  self              = true
}

resource "aws_security_group_rule" "kafka_cidr_ingress" {
  security_group_id = aws_security_group.msk.id
  count             = length(var.allowed_cidrs) > 0 ? 1 : 0
  type              = "ingress"
  from_port         = 9092
  to_port           = 9092
  protocol          = "tcp"
  cidr_blocks       = var.allowed_cidrs
}

resource "aws_security_group_rule" "kafka_sg_ingress" {
  security_group_id        = aws_security_group.msk.id
  count                    = length(var.allowed_sgs)
  type                     = "ingress"
  from_port                = 9092
  to_port                  = 9092
  protocol                 = "tcp"
  source_security_group_id = element(var.allowed_sgs, count.index)
}

resource "aws_security_group_rule" "kafka_tls" {
  from_port         = 9094
  to_port           = 9094
  protocol          = "tcp"
  security_group_id = aws_security_group.msk.id
  type              = "ingress"
  self              = true
}

resource "aws_security_group_rule" "kafka_tls_cidr_ingress" {
  security_group_id = aws_security_group.msk.id
  count             = length(var.allowed_cidrs) > 0 ? 1 : 0
  type              = "ingress"
  from_port         = 9094
  to_port           = 9094
  protocol          = "tcp"
  cidr_blocks       = var.allowed_cidrs
}

resource "aws_security_group_rule" "kafka_tls_sg_ingress" {
  security_group_id        = aws_security_group.msk.id
  count                    = length(var.allowed_sgs)
  type                     = "ingress"
  from_port                = 9094
  to_port                  = 9094
  protocol                 = "tcp"
  source_security_group_id = element(var.allowed_sgs, count.index)
}

resource "aws_security_group_rule" "zookeeper" {
  from_port         = 2181
  to_port           = 2181
  protocol          = "tcp"
  security_group_id = aws_security_group.msk.id
  type              = "ingress"
  self              = true
}

# resource "aws_security_group_rule" "kafka_zookeeper_cidr_ingress" {
#   security_group_id = aws_security_group.msk.id
#   count             = length(var.allowed_cidrs) > 0 ? 1 : 0
#   type              = "ingress"
#   from_port         = 2181
#   to_port           = 2181
#   protocol          = "tcp"
#   cidr_blocks       = var.allowed_cidrs
# }

# resource "aws_security_group_rule" "kafka_zookeeper_sg_ingress" {
#   security_group_id        = aws_security_group.msk.id
#   count                    = length(var.allowed_sgs)
#   type                     = "ingress"
#   from_port                = 2181
#   to_port                  = 2181
#   protocol                 = "tcp"
#   source_security_group_id = element(var.allowed_sgs, count.index)
# }

# resource "aws_security_group_rule" "jmx-exporter" {
#   count = var.jmx_exporter ? 1 : 0

#   from_port         = 11001
#   to_port           = 11001
#   protocol          = "tcp"
#   security_group_id = aws_security_group.msk.id
#   type              = "ingress"
#   self              = true
# }

# resource "aws_security_group_rule" "node_exporter" {
#   count = var.node_exporter ? 1 : 0

#   from_port         = 11002
#   to_port           = 11002
#   protocol          = "tcp"
#   security_group_id = aws_security_group.msk.id
#   type              = "ingress"
#   self              = true
# }

