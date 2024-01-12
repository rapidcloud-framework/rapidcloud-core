data "aws_caller_identity" "current" {}


resource "aws_iam_role" "dms_endpoint" {
  name = var.endpoint_id

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "dms.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF

  tags = var.tags
}

resource "aws_iam_role_policy_attachment" "dms_endpoint" {
  role       = aws_iam_role.dms_endpoint.name
  policy_arn = aws_iam_policy.dms_endpoint.arn
}

resource "aws_iam_policy" "dms_endpoint" {
  name        = var.endpoint_id
  description = "policy for ${var.endpoint_id} s3 target endpoint"
  policy      = data.aws_iam_policy_document.dms_endpoint.json
}

data "aws_iam_policy_document" "dms_endpoint" {
  statement {
    sid = "AllowS3"

    actions = [
      "s3:ListBucket",
      "s3:PutObject",
      "s3:PutObjectTagging",
      "s3:GetObjectVersion",
      "s3:DeleteObject",
    ]

    resources = [
      var.s3_bucket_arn,
      "${var.s3_bucket_arn}/*"
    ]

  }
}
