##################################################
# workload lambda
##################################################

resource "aws_iam_role" "workload_lambda_role" {
  name = "${var.prefix}-workload-lambda"
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

resource "aws_iam_role_policy_attachment" "workload_lambda_attach" {
  role       = aws_iam_role.workload_lambda_role.name
  policy_arn = aws_iam_policy.workload_lambda_policy.arn
}

data "aws_iam_policy_document" "workload_lambda_policy_json" {

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
    sid = "AllowTFState"
    actions = [
      "s3:GetBucketAcl",
      "s3:ListBucket",
      "s3:GetObject"
    ]
    resources = [
      "${var.arn_prefix[var.region]}:s3:::${replace("${var.prefix}", "_", "-")}-kc-big-data-tf-state",
      "${var.arn_prefix[var.region]}:s3:::${replace("${var.prefix}", "_", "-")}-kc-big-data-tf-state/*"
    ]
  }

  statement {
    sid = "AllowPauseResume"
    actions = [
      "ec2:DescribeInstances",
      "ec2:StopInstances",
      "ec2:StartInstances",
      "rds:DescribeDBInstances",
      "rds:StopDBInstance",
      "rds:StartDBInstance",
      "rds:DescribeDBClusters",
      "rds:StopDBCluster",
      "rds:StartDBCluster",
      "redshift:DescribeClusters",
      "redshift:PauseCluster",
      "redshift:ResumeCluster",
      "autoscaling:DescribeAutoScalingGroups",
      "autoscaling:UpdateAutoScalingGroup",
      "ecs:ListServices",
      "ecs:DescribeServices",
      "ecs:UpdateService"
      
    ]
    resources = ["*"]
  }

}

resource "aws_iam_policy" "workload_lambda_policy" {
  name   = "${var.prefix}-workload-lambda"
  policy = data.aws_iam_policy_document.workload_lambda_policy_json.json
}

resource "aws_iam_role_policy_attachment" "workload_attach_lambda_generic" {
  role       = aws_iam_role.workload_lambda_role.name
  policy_arn = aws_iam_policy.lambda_generic_policy.arn
}

output "workload_lambda_role_arn" {
  value = aws_iam_role.workload_lambda_role.arn
}
