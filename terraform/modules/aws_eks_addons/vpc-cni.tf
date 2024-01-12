data "aws_eks_addon_version" "vpc_cni" {
  addon_name         = "vpc-cni"
  kubernetes_version = var.eks_version
}

resource "aws_iam_role" "eks_cni" {
  count              = var.compute_type != "fargate" && var.enable_aws_vpc_cni == "true" ? 1 : 0
  name               = "${var.cluster_name}-eks-cni-addon"
  description        = "Role for Amazon to assign IPs from VPCs."
  assume_role_policy = data.aws_iam_policy_document.eks_cni.json
}

data "aws_iam_policy_document" "eks_cni" {
  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]
    effect  = "Allow"

    condition {
      test     = "StringEquals"
      variable = "${replace(var.eks_oidc_provider.url, "https://", "")}:sub"
      values   = ["system:serviceaccount:kube-system:aws-node"]
    }

    principals {
      identifiers = [var.eks_oidc_provider.arn]
      type        = "Federated"
    }
  }
}

resource "aws_iam_role_policy_attachment" "eks_cni" {
  count      = var.compute_type != "fargate" && var.enable_aws_vpc_cni == "true" ? 1 : 0
  role       = aws_iam_role.eks_cni[0].name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
}

resource "aws_eks_addon" "vpc-cni" {
  count             = var.compute_type != "fargate" && var.enable_aws_vpc_cni == "true" ? 1 : 0
  addon_name        = "vpc-cni"
  addon_version     = var.aws_vpc_cni_version != "latest" ? var.aws_vpc_cni_version : data.aws_eks_addon_version.vpc_cni.version
  cluster_name      = var.cluster_name
  resolve_conflicts = "OVERWRITE"
  depends_on        = [aws_iam_role.eks_cni]
  tags = merge(
    {
      "eks_addon" = "vpc-cni"
    }
  )
}
