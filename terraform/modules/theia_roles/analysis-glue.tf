resource "aws_iam_role" "analysis_glue_role" {
  name = "${var.prefix}-analysis-glue"

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
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "analysis_glue_attach" {
  role       = aws_iam_role.analysis_glue_role.name
  policy_arn = aws_iam_policy.analysis_glue_policy.arn
}

data "aws_iam_policy_document" "analysis_glue_policy_json" {
  statement {
    sid = "AllowLambdaResources"

    actions = [
      "lambda:ListFunctions",
      "lambda:InvokeFunction",
    ]

    resources = ["*"]
  }

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
      "${var.arn_prefix[var.region]}:s3:::${replace("${var.prefix}", "_", "-")}-query-results-bucket",
      "${var.arn_prefix[var.region]}:s3:::${replace("${var.prefix}", "_", "-")}-query-results-bucket/*",
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
      "${var.arn_prefix[var.region]}:s3:::${replace("${var.prefix}", "_", "-")}-glue-scripts",
      "${var.arn_prefix[var.region]}:s3:::${replace("${var.prefix}", "_", "-")}-glue-scripts/*",
      "${var.arn_prefix[var.region]}:s3:::${replace("${var.prefix}", "_", "-")}-utils",
      "${var.arn_prefix[var.region]}:s3:::${replace("${var.prefix}", "_", "-")}-utils/*",
      "${var.arn_prefix[var.region]}:s3:::${replace("${var.prefix}", "_", "-")}-raw",
      "${var.arn_prefix[var.region]}:s3:::${replace("${var.prefix}", "_", "-")}-raw/*",
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
    sid = "AllowROtoKMS"
    actions = [
      "kms:Decrypt",
      "kms:Encrypt",
      "kms:GenerateDataKey",
      "ssm:GetParameters",
      "ssm:GetParameter",
    ]

    resources = [
      "${var.arn_prefix[var.region]}:kms:*:${var.account_id}:alias/*",
      "${var.arn_prefix[var.region]}:kms:*:${var.account_id}:key/*",
      "${var.arn_prefix[var.region]}:ssm:*:${var.account_id}:parameter/*",
    ]
  }

  statement {
    sid = "AllowKMSKeyGeneration"
    actions = [
      "kms:GenerateDataKey",
    ]

    resources = [
      "${var.arn_prefix[var.region]}:kms:*:${var.account_id}:alias/*",
      "${var.arn_prefix[var.region]}:kms:*:${var.account_id}:key/*",
      "${var.arn_prefix[var.region]}:ssm:*:${var.account_id}:parameter/*",
    ]
  }

  statement {
    sid = "AllowAthena"
    actions = [
      "athena:StartQueryExecution",
      "athena:GetQueryExecution",
      "athena:GetQueryResults",
    ]
    resources = [
      "${var.arn_prefix[var.region]}:athena:*:${var.account_id}:workgroup/*",
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

  statement {
    sid = "AllowDynamo"
    actions = [
      "dynamodb:UpdateItem",
      "dynamodb:Scan",
      "dynamodb:Query",
      "dynamodb:PutItem",
      "dynamodb:ListTables",
      "dynamodb:GetItem",
      "dynamodb:DescribeTable",
      "dynamodb:DeleteItem",
      "dynamodb:BatchGetItem"
    ]
    resources = [
      "${var.arn_prefix[var.region]}:dynamodb:*:${var.account_id}:table/*",
    ]
  }
}

resource "aws_iam_policy" "analysis_glue_policy" {
  name   = "${var.prefix}-analysis-glue"
  policy = data.aws_iam_policy_document.analysis_glue_policy_json.json
}

resource "aws_iam_role_policy_attachment" "analysis_attach_glue_service_role" {
  role       = aws_iam_role.analysis_glue_role.name
  policy_arn = "${var.arn_prefix[var.region]}:iam::aws:policy/service-role/AWSGlueServiceRole"
}

output "analysis_glue_role_arn" {
  value = aws_iam_role.analysis_glue_role.arn
}

