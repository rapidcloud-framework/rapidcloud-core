resource "aws_iam_role" "role" {
  count = var.enable_bucket_policy ? 1 : 0
  name  = "${var.bucket_name}-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "dms.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "attach" {
  count      = var.enable_bucket_policy ? 1 : 0
  role       = aws_iam_role.role.0.name
  policy_arn = aws_iam_policy.policy.0.arn
}

data "aws_iam_policy_document" "policy_json" {
  statement {
    actions = [
      "s3:ListBucket",
      "s3:PutObject",
      "s3:DeleteObject",
    ]

    resources = [
      aws_s3_bucket.s3.arn,
      "${aws_s3_bucket.s3.arn}/*",
    ]
  }
}

resource "aws_iam_policy" "policy" {
  count  = var.enable_bucket_policy ? 1 : 0
  name   = "dms-datalake-s3-${var.bucket_name}-policy"
  policy = data.aws_iam_policy_document.policy_json.json
}
