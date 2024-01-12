##################################################
# lambda
##################################################

resource "aws_iam_role" "scan_ingestion_lambda_role" {
  name = "${var.prefix}-scan-ingestion-lambda"

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

resource "aws_iam_role_policy_attachment" "scan_ingestion_lambda_attach" {
  role       = aws_iam_role.scan_ingestion_lambda_role.name
  policy_arn = aws_iam_policy.scan_ingestion_lambda_policy.arn
}

data "aws_iam_policy_document" "scan_ingestion_lambda_policy_json" {

  statement {
    sid = "AllowLambdaResources"
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:DescribeLogGroups",
      "logs:DescribeLogStreams",
      "logs:PutLogEvents",
      "logs:PutLogEvents",
    ]
    resources = ["*"]
  }
  
  statement {
    sid = "AllowPromoteAndQuarantine"
    actions = [
      "s3:GetBucketAcl",
      "s3:ListBucket",
      "s3:GetObject",
      "s3:PutObject",
      "s3:PutObjectTagging"
    ]
    resources = [
      "${var.arn_prefix[var.region]}:s3:::*-ingestion",
      "${var.arn_prefix[var.region]}:s3:::*-ingestion/*",
      "${var.arn_prefix[var.region]}:s3:::${replace("${var.prefix}", "_", "-")}-quarantine",
      "${var.arn_prefix[var.region]}:s3:::${replace("${var.prefix}", "_", "-")}-quarantine/*"
    ]
  }

}

resource "aws_iam_policy" "scan_ingestion_lambda_policy" {
  name   = "${var.prefix}-scan-ingestion-lambda"
  policy = data.aws_iam_policy_document.scan_ingestion_lambda_policy_json.json
  lifecycle {
    # scan-ingestion policy will be changed every time new TM-FSS storage stack is added or removed, therefore we are instructing terraform to never propose changes for this policy
    ignore_changes = all
  }
}

resource "aws_iam_role_policy_attachment" "scan_ingestion_attach_lambda_generic" {
  role       = aws_iam_role.scan_ingestion_lambda_role.name
  policy_arn = aws_iam_policy.lambda_generic_policy.arn
}

output "scan-ingestion_lambda_role_arn" {
  value = aws_iam_role.scan_ingestion_lambda_role.arn
}
