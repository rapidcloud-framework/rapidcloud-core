resource "aws_iam_role" "role" {
  name               = "${var.prefix}-lambda"
  description        = "This role allows ${var.prefix}-lambda access to DMS, Cloudwatch, Lambda, SNS, KMS and Dyanmo"
  assume_role_policy = data.aws_iam_policy_document.sts.json
}

data "aws_iam_policy_document" "sts" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role_policy_attachment" "policy" {
  role       = aws_iam_role.role.name
  policy_arn = aws_iam_policy.policy.arn
}

resource "aws_iam_policy" "policy" {
  name        = "${var.prefix}-lambda"
  description = "This policy allows ${var.prefix}-lambda access to DMS, Cloudwatch, SNS and Lambda"
  policy      = data.aws_iam_policy_document.policy.json
}

data "aws_iam_policy_document" "policy" {
  statement {
    sid = "AllowLambda"

    actions = [
      "ec2:CreateNetworkInterface",    # needed for running in vpc
      "ec2:DescribeNetworkInterfaces", # needed for running in vpc
      "ec2:DeleteNetworkInterface",    # needed for running in vpc
      "ec2:AttachNetworkInterface",    # needed for running in vpc

      "lambda:ListFunctions",
      "lambda:InvokeFunction",

      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:DescribeLogGroups",
      "logs:DescribeLogStreams",
      "logs:PutLogEvents",
      "logs:PutLogEvents",

      "dms:ListTagsForResource",
      "dms:RemoveTagsFromResource",
      "dms:DescribeReplicationTasks",
      "dms:AddTagsToResource",
      "dms:ModifyReplicationTask",
      "dms:StartReplicationTask",
      "s3:ListAllMyBuckets",
      "s3:GetBucketLocation",
    ]

    resources = ["*"]
  }

  statement {
    sid = "ssm"

    actions = [
      "kms:Decrypt",
      "ssm:GetParameters",
      "ssm:GetParameter",
    ]

    resources = [
      "${var.arn_prefix[var.region]}:kms:${var.region}:${var.account}:*",
      "${var.arn_prefix[var.region]}:kms:${var.region}:${var.account}:alias/*",
      "${var.arn_prefix[var.region]}:kms:${var.region}:${var.account}:key/*",
    ]
  }

  statement {
    actions = [
      "sns:CreateTopic",
      "sns:ListTopics",
      "sns:SetTopicAttributes",
      "sns:DeleteTopic",
      "sns:Publish",
    ]

    resources = ["${var.arn_prefix[var.region]}:sns:*:${var.account}:*"]
  }

  statement {
    actions = [
      "secretsmanager:Describe*",
      "secretsmanager:Get*",
      "secretsmanager:List*"
    ]
    resources = ["${var.arn_prefix[var.region]}:secretsmanager:*:${var.account}:secret:${replace("${var.prefix}", "-", "_")}/*"]

  }

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
      "dynamodb:BatchGetItem",
      "dynamodb:ListTables"
    ]

    resources = ["*"]
  }
  statement {
    actions = [
      "s3:PutObject",
      "s3:ListBucket",
      "s3:GetObject",
      "s3:GetBucketAcl",
      "s3:DeleteObject"
    ]
    resources = [
      "${var.arn_prefix[var.region]}:s3:::${replace("${var.prefix}", "_", "-")}*/*",
      "${var.arn_prefix[var.region]}:s3:::${replace("${var.prefix}", "_", "-")}*",
      "${var.arn_prefix[var.region]}:s3:::_data_*/*",
      "${var.arn_prefix[var.region]}:s3:::_data_*",
      "${var.arn_prefix[var.region]}:s3:::-data-*/*",
      "${var.arn_prefix[var.region]}:s3:::-data-*"
    ]
  }
  statement {
    actions = [
      "glue:GetTable",
      "glue:GetTables",
      "glue:GetDatabase",
      "glue:GetDataBases",
      "glue:StartTrigger",
      "glue:StartJobRun",
    ]
    resources = [
      "${var.arn_prefix[var.region]}:glue:${var.region}:${var.account}:*"
    ]
  }
}
