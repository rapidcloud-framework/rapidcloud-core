##################################################
# lambda
##################################################

resource "aws_iam_role" "ingestion_raw_lambda_role" {
  name = "${var.prefix}-ingestion-raw-lambda"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "ingestion_raw_lambda_attach" {
  role       = aws_iam_role.ingestion_raw_lambda_role.name
  policy_arn = aws_iam_policy.ingestion_raw_lambda_policy.arn
}

data "aws_iam_policy_document" "ingestion_raw_lambda_policy_json" {

  statement {
    sid = "AllowRWtoIngestionRawBucket"
    actions = [
      "s3:GetBucketAcl",
      "s3:ListBucket",
      "s3:GetObject",
      "s3:PutObject",
      "s3:DeleteObject",
    ]

    resources = [
      "${var.arn_prefix[var.region]}:s3:::${replace("${var.prefix}", "_", "-")}-raw",
      "${var.arn_prefix[var.region]}:s3:::${replace("${var.prefix}", "_", "-")}-raw/*",
      "${var.arn_prefix[var.region]}:s3:::${replace("${var.prefix}", "_", "-")}-query-results-bucket",
      "${var.arn_prefix[var.region]}:s3:::${replace("${var.prefix}", "_", "-")}-query-results-bucket/*",
    ]
  }

  statement {
    sid = "AllowROtoUtilsAndIngestionBucket"
    actions = [
      "s3:GetBucketAcl",
      "s3:ListBucket",
      "s3:GetObject",
    ]

    resources = [
      "${var.arn_prefix[var.region]}:s3:::${replace("${var.prefix}", "_", "-")}-utils",
      "${var.arn_prefix[var.region]}:s3:::${replace("${var.prefix}", "_", "-")}-utils/*",
      "${var.arn_prefix[var.region]}:s3:::${replace("${var.prefix}", "_", "-")}-ingestion",
      "${var.arn_prefix[var.region]}:s3:::${replace("${var.prefix}", "_", "-")}-ingestion/*",
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
      "${var.arn_prefix[var.region]}:secretsmanager:*:${var.account_id}:secret:trendmicro/api_key",
    ]

  }

  statement {
    sid = "AllowAthena"
    actions = [
      "athena:StartQueryExecution",
      "athena:GetQueryExecution",
    ]
    resources = [
      "${var.arn_prefix[var.region]}:athena:*:${var.account_id}:workgroup/*",
    ]
  }

  statement {
    sid = "AllowLambda"
    actions = [
      "lambda:GetFunction",
      "lambda:AddPermission",
    ]
    resources = [
      "${var.arn_prefix[var.region]}:athena:*:${var.account_id}:workgroup/*",
      "${var.arn_prefix[var.region]}:lambda:*:${var.account_id}:function:*"
    ]
  }

  statement {
    sid = "AllowTextract"
    actions = [
      "textract:StartDocumentTextDetection",
      "textract:StartDocumentAnalysis",
      "textract:GetDocumentTextDetection",
      "textract:GetDocumentAnalysis"
    ]
    resources = [
      "*"
    ]
  }

}

resource "aws_iam_policy" "ingestion_raw_lambda_policy" {
  name   = "${var.prefix}-ingestion-raw-lambda"
  policy = data.aws_iam_policy_document.ingestion_raw_lambda_policy_json.json
}

resource "aws_iam_role_policy_attachment" "ingestion_raw_attach_lambda_generic" {
  role       = aws_iam_role.ingestion_raw_lambda_role.name
  policy_arn = aws_iam_policy.lambda_generic_policy.arn
}

output "ingestion-raw_lambda_role_arn" {
  value = aws_iam_role.ingestion_raw_lambda_role.arn
}
