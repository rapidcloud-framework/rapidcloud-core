data "aws_kms_alias" "env" {
  name = "alias/${var.profile}"
}

# Cluster IAM Role
data "aws_iam_policy_document" "eks_sts" {
  statement {
    actions = ["sts:AssumeRole"]
    effect  = "Allow"
    principals {
      type        = "Service"
      identifiers = ["eks.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "eks" {
  name               = "${local.cluster_name}-EKSClusterRole"
  assume_role_policy = data.aws_iam_policy_document.eks_sts.json
}

resource "aws_iam_role_policy_attachment" "eks_cluster" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.eks.name
}

resource "aws_iam_role_policy_attachment" "eks_service" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSServicePolicy"
  role       = aws_iam_role.eks.name
}

resource "aws_iam_role_policy_attachment" "eks_vpc_resource_controller" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSVPCResourceController"
  role       = aws_iam_role.eks.name
}

# Cloudwatch Log Group
resource "aws_cloudwatch_log_group" "eks" {
  name_prefix       = "/aws/eks/${local.cluster_name}/cluster"
  retention_in_days = var.cluster_log_retention_period
  lifecycle {
    create_before_destroy = false
  }
}

# locals {
#   enable_encryption = var.kms_key_arn != "" ? ["${var.kms_key_arn}"] : []
# }


resource "aws_eks_cluster" "eks" {
  role_arn                  = aws_iam_role.eks.arn
  enabled_cluster_log_types = toset(split(",", var.cluster_log_types))
  name                      = local.cluster_name

  vpc_config {
    subnet_ids         = local.subnet_ids
    security_group_ids = []
    # security_group_ids      = aws_security_group.eks.id
    endpoint_private_access = true
    endpoint_public_access  = var.endpoint_public_access == "true" ? true : false
    public_access_cidrs     = var.endpoint_public_access == "true" && var.endpoint_public_access_cidrs != "" ? split(",", var.endpoint_public_access_cidrs) : []
  }

  version = var.eks_version

  encryption_config {
    provider {
      key_arn = data.aws_kms_alias.env.target_key_arn
    }
    resources = ["secrets"]
  }

  tags = merge(local.rc_tags, var.tags)

  depends_on = [
    aws_iam_role_policy_attachment.eks_cluster,
    aws_iam_role_policy_attachment.eks_service,
    aws_cloudwatch_log_group.eks
  ]
}

data "tls_certificate" "eks" {
  url = aws_eks_cluster.eks.identity[0].oidc[0].issuer
}

resource "aws_iam_openid_connect_provider" "eks" {
  client_id_list  = ["sts.amazonaws.com"]
  thumbprint_list = [data.tls_certificate.eks.certificates[0].sha1_fingerprint]
  url             = aws_eks_cluster.eks.identity[0].oidc[0].issuer
}

output "eks_cluster_security_group_id" {
  value = join("", aws_eks_cluster.eks.*.vpc_config.0.cluster_security_group_id)
}

output "eks_cluster_info" {
  value = aws_eks_cluster.eks
}


output "eks_cluster_name" {
  value = join("", aws_eks_cluster.eks.*.id)
}

output "eks_cluster_endpoint" {
  value = join("", aws_eks_cluster.eks.*.endpoint)
}

output "eks_cluster_platform_version" {
  value = join("", aws_eks_cluster.eks.*.platform_version)
}

output "eks_cluster_kubernetes_version" {
  value = join("", aws_eks_cluster.eks.*.version)
}

output "eks_cluster_vpc_config" {
  value = join("", aws_eks_cluster.eks.*.vpc_config.0.vpc_id)
}

output "cluster_role_arn" {
  value = join("", aws_iam_role.eks.*.arn)
}

output "eks_oidc_provider" {
  value = aws_iam_openid_connect_provider.eks
}
