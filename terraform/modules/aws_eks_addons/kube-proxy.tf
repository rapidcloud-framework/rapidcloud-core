data "aws_eks_addon_version" "kube_proxy" {
  addon_name         = "kube-proxy"
  kubernetes_version = var.eks_version
}

resource "aws_eks_addon" "kube_proxy" {
  count             = var.compute_type != "fargate" && var.enable_aws_kube_proxy == "true" ? 1 : 0
  addon_name        = "kube-proxy"
  addon_version     = var.aws_kube_proxy_version != "latest" ? var.aws_kube_proxy_version : data.aws_eks_addon_version.kube_proxy.version
  cluster_name      = var.cluster_name
  resolve_conflicts = "OVERWRITE"
  tags = merge(
    {
      "eks_addon" = "kube-proxy"
    }
  )
}
