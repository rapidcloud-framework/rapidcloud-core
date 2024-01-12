##################################################
# lambda
##################################################

resource "aws_iam_role" "ingestion_lambda_role" {
  name = "${var.prefix}-ingestion-lambda"

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

resource "aws_iam_role_policy_attachment" "ingestion_lambda_attach" {
  role       = aws_iam_role.ingestion_lambda_role.name
  policy_arn = aws_iam_policy.ingestion_lambda_policy.arn
}

data "aws_iam_policy_document" "ingestion_lambda_policy_json" {
  statement {
    sid = "AllowRWtoIngestionBucket"
    actions = [
      "s3:GetBucketAcl",
      "s3:ListBucket",
      "s3:GetObject",
      "s3:PutObject",
      "s3:DeleteObject",
    ]

    resources = [
      "${var.arn_prefix[var.region]}:s3:::${replace("${var.prefix}", "_", "-")}-ingestion",
      "${var.arn_prefix[var.region]}:s3:::${replace("${var.prefix}", "_", "-")}-ingestion/*"
    ]
  }

  statement {
    sid = "AllowROtoUtilsBucket"
    actions = [
      "s3:GetBucketAcl",
      "s3:ListBucket",
      "s3:GetObject",
    ]

    resources = [
      "${var.arn_prefix[var.region]}:s3:::${replace("${var.prefix}", "_", "-")}-utils/*",
      "${var.arn_prefix[var.region]}:s3:::${replace("${var.prefix}", "_", "-")}-utils"
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

}

resource "aws_iam_policy" "ingestion_lambda_policy" {
  name   = "${var.prefix}-ingestion-lambda"
  policy = data.aws_iam_policy_document.ingestion_lambda_policy_json.json
}

resource "aws_iam_role_policy_attachment" "ingestion_attach_lambda_generic" {
  role       = aws_iam_role.ingestion_lambda_role.name
  policy_arn = aws_iam_policy.lambda_generic_policy.arn
}

output "ingestion_lambda_role_arn" {
  value = aws_iam_role.ingestion_lambda_role.arn
}
