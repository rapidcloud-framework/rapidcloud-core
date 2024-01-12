resource "aws_iam_role" "rds" {
  name               = "${var.cluster_identifier}-rds-monitoring"
  description        = "Allows RDS to write logs and monitoring data to cloudwatch"
  assume_role_policy = data.aws_iam_policy_document.rds.json
}

data "aws_iam_policy_document" "rds" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["monitoring.rds.amazonaws.com"]
    }
  }
}

resource "aws_iam_role_policy_attachment" "rds" {
  role       = aws_iam_role.rds.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonRDSEnhancedMonitoringRole"
}

output "rds_monitoring_arn" {
  value = aws_iam_role.rds.arn
}

