resource "aws_iam_policy" "lambda_generic_policy" {
  name        = "${var.prefix}-lambda-generic"
  description = "This policy allows ${var.prefix}-lambda access to DMS, Cloudwatch, SNS and Lambda"
  policy      = data.aws_iam_policy_document.lambda_generic_policy.json
}

data "aws_iam_policy_document" "lambda_generic_policy" {
  statement {
    sid = "AllowLambdaResources"

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
    sid = "AllowKMS"
    actions = [
      "kms:Decrypt",
      "kms:Encrypt",
    ]

    resources = [
      "${var.arn_prefix[var.region]}:kms:${var.region}:${var.account_id}:*",
      "${var.arn_prefix[var.region]}:kms:${var.region}:${var.account_id}:alias/*",
      "${var.arn_prefix[var.region]}:kms:${var.region}:${var.account_id}:key/*",
    ]
  }

  statement {
    sid = "AllowSNS"
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
    sid = "DenyRedshiftClusterActions"
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
    sid = "AllowDynamoActions"
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
    sid = "AllowGlueJobs"
    actions = [
      "glue:StartTrigger",
      "glue:StartJobRun",
      "glue:StartCrawler",
      "glue:GetCrawler",
      "glue:BatchCreatePartition",
      "glue:GetTable",
      "glue:GetTables",
      "glue:GetDatabase",
      "glue:GetDataBases",
      "glue:GetJob"
    ]
    resources = [
      "${var.arn_prefix[var.region]}:glue:${var.region}:${var.account_id}:*"
    ]
  }

  statement {
    sid = "AllowCloudformation"
    actions = [
      "cloudformation:DescribeStacks"
    ]
    resources = ["*"]
  }

  statement {
    sid = "AllowSecrets"
    actions = [
      "secretsmanager:Describe*",
      "secretsmanager:Get*",
      "secretsmanager:List*"
    ]

    resources = [
      "${var.arn_prefix[var.region]}:secretsmanager:*:${var.account_id}:secret:${replace("${var.prefix}", "-", "_")}/*/*",
      "${var.arn_prefix[var.region]}:secretsmanager:*:${var.account_id}:secret:trendmicro/*"
    ]

  }

}

