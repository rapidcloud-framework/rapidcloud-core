data "aws_region" "current" {}

resource "aws_iam_role" "psql" {
  name               = "${var.instance_name}-psql-monitoring"
  description        = "Allows RDS to write logs and monitoring data to cloudwatch"
  assume_role_policy = data.aws_iam_policy_document.psql.json
}

data "aws_iam_policy_document" "psql" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["monitoring.rds.amazonaws.com"]
    }
  }
}

resource "aws_iam_role_policy_attachment" "psql" {
  role       = aws_iam_role.psql.name
  policy_arn = "${var.arn_prefix[data.aws_region.current.name]}:iam::aws:policy/service-role/AmazonRDSEnhancedMonitoringRole"
}
