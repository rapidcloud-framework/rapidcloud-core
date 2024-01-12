resource "aws_iam_role" "firehose" {
  name               = var.name
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "firehose.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "firehose" {
  role       = aws_iam_role.firehose.name
  policy_arn = aws_iam_policy.firehose.arn
}

resource "aws_iam_policy" "firehose" {
  name   = var.name
  policy = data.aws_iam_policy_document.firehose.json
}

data "aws_iam_policy_document" "firehose" {
  statement {
    actions = [
      "glue:GetTable",
      "glue:GetTableVersion",
      "glue:GetTableVersions"
    ]
    resources = ["*"]
  }
  statement {
    actions = [
      "s3:AbortMultipartUpload",
      "s3:GetBucketLocation",
      "s3:GetObject",
      "s3:ListBucket",
      "s3:ListBucketMultipartUploads",
      "s3:PutObject"
    ]
    resources = [
      var.destination_bucket_arn,
      "${var.destination_bucket_arn}/*",
    ]
  }
  statement {
    actions = [
      "logs:PutLogEvents"
    ]
    resources = [
      "arn:aws:logs:${var.region}:${var.account_id}:log-group:/aws/kinesisfirehose/${var.name}:log-stream:*"
    ]
  }
  statement {
    actions = [
      "kinesis:DescribeStream",
      "kinesis:GetShardIterator",
      "kinesis:GetRecords",
      "kinesis:ListShards"
    ]
    resources = ["*"]
  }
  statement {
    actions = [
      "kms:Decrypt"
    ]
    resources = [
      "arn:aws:kms:${var.region}:${var.account_id}:alias/*",
      "arn:aws:kms:${var.region}:${var.account_id}:key/*",
    ]
  }
}
