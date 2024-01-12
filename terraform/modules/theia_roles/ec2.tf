##################################################
# ec2
##################################################
resource "aws_iam_role" "ec2_role" {
  name = "${var.prefix}-ec2"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

data "aws_iam_policy_document" "ec2_policy_json" {
  statement {
    sid = "AllowRWtoAnalysisBucket"
    actions = [
      "s3:GetBucketAcl",
      "s3:ListBucket",
      "s3:GetObject",
      "s3:PutObject",
      "s3:DeleteObject",
    ]

    resources = [
      "${var.arn_prefix[var.region]}:s3:::${replace("${var.prefix}", "_", "-")}-analysis",
      "${var.arn_prefix[var.region]}:s3:::${replace("${var.prefix}", "_", "-")}-analysis/*",
    ]
  }

  statement {
    sid = "AllowROtoUtilsAndRawBucket"
    actions = [
      "s3:GetBucketAcl",
      "s3:ListBucket",
      "s3:GetObject",
    ]

    resources = [
      "${var.arn_prefix[var.region]}:s3:::${replace("${var.prefix}", "_", "-")}-utils",
      "${var.arn_prefix[var.region]}:s3:::${replace("${var.prefix}", "_", "-")}-utils/*",
      "${var.arn_prefix[var.region]}:s3:::${replace("${var.prefix}", "_", "-")}-raw",
      "${var.arn_prefix[var.region]}:s3:::${replace("${var.prefix}", "_", "-")}-raw/*"
    ]
  }

  statement {
    sid = "AllowROtoRDSSecrets"
    actions = [
      "secretsmanager:Describe*",
      "secretsmanager:Get*",
      "secretsmanager:List*"
    ]

    resources = [
      "${var.arn_prefix[var.region]}:secretsmanager:*:${var.account_id}:secret:${replace("${var.prefix}", "-", "_")}/rds_*/*",
      "${var.arn_prefix[var.region]}:secretsmanager:*:${var.account_id}:secret:${replace("${var.prefix}", "-", "_")}/aurora_*/*",
    ]

  }

  statement {
    sid = "AllowSns"
    actions = [
      "sns:Publish",
      "sns:ListTopics",
    ]
    resources = [
      "${var.arn_prefix[var.region]}:sns:*:${var.account_id}:*",
    ]
  }
}

data "aws_iam_policy" "AmazonSSMManagedInstanceCore" {
  arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

resource "aws_iam_policy" "ec2_policy" {
  name   = "${var.prefix}-ec2"
  policy = data.aws_iam_policy_document.ec2_policy_json.json
}

resource "aws_iam_role_policy_attachment" "ec2_attach" {
  role       = aws_iam_role.ec2_role.name
  policy_arn = aws_iam_policy.ec2_policy.arn
}

resource "aws_iam_role_policy_attachment" "AmazonSSMManagedInstanceCore" {
  role       = aws_iam_role.ec2_role.name
  policy_arn = data.aws_iam_policy.AmazonSSMManagedInstanceCore.arn
}

output "ec2_role_arn" {
  value = aws_iam_role.ec2_role.arn
}
