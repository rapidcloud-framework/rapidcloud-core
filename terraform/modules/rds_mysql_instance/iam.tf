resource "aws_iam_role" "mysql" {
  name               = var.instance_name
  description        = "Allows RDS to write logs and monitoring data to cloudwatch"
  assume_role_policy = data.aws_iam_policy_document.mysql.json
}

data "aws_iam_policy_document" "mysql" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["monitoring.rds.amazonaws.com"]
    }
  }
}

resource "aws_iam_role_policy_attachment" "mysql" {
  role       = aws_iam_role.mysql.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonRDSEnhancedMonitoringRole"
}
