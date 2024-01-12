resource "aws_iam_role" "role" {
  name = "${var.prefix}-glue-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "glue.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    },
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "redshift.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "attach" {
  role       = aws_iam_role.role.name
  policy_arn = aws_iam_policy.policy.arn
}

data "aws_iam_policy_document" "policy_json" {
  statement {
    actions = [
      "redshift:CreateCluster",
      "redshift:DeleteCluster",
      "redshift:ModifyCluster",
      "redshift:RebootCluster"
    ]

    resources = ["*"]
    effect    = "Deny"

  }
  statement {
    actions = [
      "dynamodb:PutItem",
      "dynamodb:UpdateItem",
      "dynamodb:DeleteItem",
      "dynamodb:DescribeTable",
      "dynamodb:Query",
      "dynamodb:Scan",
      "dynamodb:GetItem",
      "dynamodb:BatchGetItem"
    ]

    resources = ["*"]
  }

  statement {
    actions = [
      "cloudwatch:PutMetricData"
    ]

    resources = ["*"]
  }

  statement {
    actions = [
      "iam:ListRolePolicies",
      "iam:GetRole",
      "iam:GetRolePolicy",
    ]

    resources = ["*"]
  }

  statement {
    actions = [
      "ec2:DescribeVpcEndpoints",
      "ec2:DescribeRouteTables",
      "ec2:CreateNetworkInterface",
      "ec2:DeleteNetworkInterface",
      "ec2:DescribeNetworkInterfaces",
      "ec2:DescribeSecurityGroups",
      "ec2:DescribeSubnets",
      "ec2:DescribeVpcAttribute",
      "ec2:CreateTags",
      "ec2:DeleteTags",
    ]

    resources = ["*"]
  }

  statement {
    actions = [
      "s3:GetBucketLocation",
      "s3:ListAllMyBuckets",
    ]

    resources = ["*"]
  }

  statement {
    actions = [
      "s3:GetBucketAcl",
      "s3:ListBucket",
      "s3:GetObject",
      "s3:PutObject",
      "s3:DeleteObject",
    ]

    resources = concat([
      aws_s3_bucket.glue_scripts.arn,
      "${aws_s3_bucket.glue_scripts.arn}/*",
      aws_s3_bucket.glue_temporary.arn,
      "${aws_s3_bucket.glue_temporary.arn}/*",
    ], var.additional_buckets)
  }


  statement {
    actions = [
      "glue:*",
    ]

    resources = ["*"]
  }


  statement {
    actions = [
      "sns:CreateTopic",
      "sns:ListTopics",
      "sns:SetTopicAttributes",
      "sns:DeleteTopic",
      "sns:Publish",
    ]

    resources = ["${var.arn_prefix[var.region]}:sns:*:${var.account_id}:*"]
  }

  statement {
    actions = [
      "secretsmanager:Describe*",
      "secretsmanager:Get*",
      "secretsmanager:List*"
    ]
    resources = ["${var.arn_prefix[var.region]}:secretsmanager:*:${var.account_id}:secret:${replace("${var.prefix}", "-", "_")}/*"]

  }

  statement {
    actions = [
      "kms:Decrypt",
      "ssm:GetParameters",
      "ssm:GetParameter",
    ]

    resources = [
      "${var.arn_prefix[var.region]}:kms:*:${var.account_id}:alias/*",
      "${var.arn_prefix[var.region]}:kms:*:${var.account_id}:key/*",
      "${var.arn_prefix[var.region]}:ssm:*:${var.account_id}:parameter/*",
    ]
  }
}

resource "aws_iam_policy" "policy" {
  name   = "${var.prefix}-glue-s3-policy"
  policy = data.aws_iam_policy_document.policy_json.json
}

resource "aws_iam_role_policy_attachment" "attach_glue" {
  role       = aws_iam_role.role.name
  policy_arn = "${var.arn_prefix[var.region]}:iam::aws:policy/service-role/AWSGlueServiceRole"
}
