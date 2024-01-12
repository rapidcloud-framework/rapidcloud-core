data "aws_partition" "current" {}
data "aws_caller_identity" "current" {}

data "aws_iam_policy_document" "fargate_sts" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["eks-fargate-pods.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "fargate" {
  name               = "${local.profile_name}EKSFargateRole"
  assume_role_policy = data.aws_iam_policy_document.fargate_sts.json
  tags               = merge(local.rc_tags, var.tags)
}

resource "aws_iam_role_policy_attachment" "fargate_pod" {
  policy_arn = "arn:${data.aws_partition.current.partition}:iam::aws:policy/AmazonEKSFargatePodExecutionRolePolicy"
  role       = aws_iam_role.fargate.name
}

resource "aws_iam_role_policy_attachment" "vpc_cni" {
  policy_arn = "arn:${data.aws_partition.current.partition}:iam::aws:policy/AmazonEKS_CNI_Policy"
  role       = aws_iam_role.fargate.name
}


data "aws_iam_policy_document" "logging" {
  statement {
    sid       = ""
    effect    = "Allow"
    resources = ["*"]

    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:DescribeLogStreams",
      "logs:PutLogEvents",
    ]
  }
}

resource "aws_iam_policy" "logging" {
  name        = "${local.profile_name}EksFargateLoggingtoCloudwatch"
  description = "Allow fargate profiles to write logs to CloudWatch"
  policy      = data.aws_iam_policy_document.logging.json
  tags        = merge(local.rc_tags, var.tags)
}

resource "aws_iam_role_policy_attachment" "logging" {
  policy_arn = aws_iam_policy.logging.arn
  role       = aws_iam_role.fargate.name
}

resource "aws_eks_fargate_profile" "fargate" {
  cluster_name           = local.cluster_name
  fargate_profile_name   = local.profile_name
  pod_execution_role_arn = aws_iam_role.fargate.arn
  subnet_ids             = local.subnet_ids


  dynamic "selector" {
    for_each = var.selectors

    content {
      namespace = selector.value.namespace
      labels    = lookup(selector.value, "labels", {})
    }
  }

  # dynamic "timeouts" {
  #   for_each = [var.timeouts]
  #   content {
  #     create = lookup(var.timeouts, "create", null)
  #     delete = lookup(var.timeouts, "delete", null)
  #   }
  # }

  tags = merge(local.rc_tags, var.tags)
}

