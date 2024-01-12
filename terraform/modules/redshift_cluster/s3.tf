data "aws_redshift_service_account" "acct" {}


resource "aws_s3_bucket" "redshift" {
  count         = var.enable_logging ? 1 : 0
  bucket        = "${var.cluster_name}-logging"
  force_destroy = true

}

resource "aws_s3_bucket_policy" "name" {
  bucket = aws_s3_bucket.redshift[count.index].id
  count  = var.enable_logging ? 1 : 0

  policy = <<EOF
{
    "Version": "2008-10-17",
    "Statement": [
        {
                    "Sid": "Put bucket policy needed for audit logging",
                    "Effect": "Allow",
                    "Principal": {
                        "AWS": "${data.aws_redshift_service_account.acct.arn}"
                    },
                    "Action": "s3:PutObject",
                    "Resource": "arn:aws:s3:::${var.cluster_name}-logging/*"
                },
                {
                    "Sid": "Get bucket policy needed for audit logging ",
                    "Effect": "Allow",
                    "Principal": {
                        "AWS": "${data.aws_redshift_service_account.acct.arn}"
                    },
                    "Action": "s3:GetBucketAcl",
                    "Resource": "arn:aws:s3:::${var.cluster_name}-logging"
                }
    ]
}
EOF
  
}

output "service_account_arn" {
  value = "${data.aws_redshift_service_account.acct.arn}"
}

output "service_account_id" {
  value = "${data.aws_redshift_service_account.acct.id}"
}
