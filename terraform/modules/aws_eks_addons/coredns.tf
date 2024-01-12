data "aws_eks_addon_version" "coredns" {
  addon_name         = "coredns"
  kubernetes_version = var.eks_version
}

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
  count              = var.compute_type == "fargate" && var.enable_aws_coredns ? 1 : 0
  name               = "${local.profile_name}-eks-fargate-role"
  assume_role_policy = data.aws_iam_policy_document.fargate_sts.json
  tags               = merge(local.rc_tags, var.tags)
}

resource "aws_iam_role_policy_attachment" "fargate_pod" {
  count      = var.compute_type == "fargate" && var.enable_aws_coredns ? 1 : 0
  policy_arn = "arn:${data.aws_partition.current.partition}:iam::aws:policy/AmazonEKSFargatePodExecutionRolePolicy"
  role       = aws_iam_role.fargate[0].name
}

data "aws_partition" "current" {}

resource "aws_iam_role_policy_attachment" "vpc_cni" {
  count      = var.compute_type == "fargate" && var.enable_aws_coredns ? 1 : 0
  policy_arn = "arn:${data.aws_partition.current.partition}:iam::aws:policy/AmazonEKS_CNI_Policy"
  role       = aws_iam_role.fargate[0].name
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
  count       = var.compute_type == "fargate" && var.enable_aws_coredns ? 1 : 0
  name        = "${local.profile_name}-eks-fargate-logging"
  description = "Allow fargate profiles to write logs to CloudWatch"
  policy      = data.aws_iam_policy_document.logging.json
  tags        = merge(local.rc_tags, var.tags)
}

resource "aws_iam_role_policy_attachment" "logging" {
  count      = var.compute_type == "fargate" && var.enable_aws_coredns ? 1 : 0
  policy_arn = aws_iam_policy.logging[0].arn
  role       = aws_iam_role.fargate[0].name
}

resource "aws_eks_fargate_profile" "coredns" {
  count                  = var.compute_type == "fargate" && var.enable_aws_coredns ? 1 : 0
  cluster_name           = local.cluster_name
  fargate_profile_name   = "coredns"
  pod_execution_role_arn = aws_iam_role.fargate[0].arn
  subnet_ids             = local.subnet_ids

  selector {
    namespace = "kube-system"
    labels = {
      k8s-app = "kube-dns"
    }
  }
  tags = merge(local.rc_tags, var.tags)
}


resource "aws_eks_addon" "coredns" {
  count             = var.enable_aws_coredns == "true" ? 1 : 0
  addon_name        = "coredns"
  addon_version     = var.aws_coredns_version != "latest" ? var.aws_coredns_version : data.aws_eks_addon_version.coredns.version
  cluster_name      = var.cluster_name
  resolve_conflicts = "OVERWRITE"

  depends_on = [aws_eks_fargate_profile.coredns]

  tags = merge(
    {
      "eks_addon" = "coredns"
    }
  )
  configuration_values = jsonencode({
    replicaCount = tonumber(var.aws_coredns_replica_count)
    computeType  = var.compute_type
    resources = {
      limits = {
        cpu    = "0.25"
        memory = "256M"
      }
      requests = {
        cpu    = "0.25"
        memory = "256M"
      }
    }
    }
  )
}
