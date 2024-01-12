resource "helm_release" "cluster_autoscaler" {
  count      = tobool(var.install_cluster_autoscaler) ? 1 : 0
  name       = "cluster-autoscaler"
  namespace  = "kube-system"
  chart      = "cluster-autoscaler"
  repository = "https://kubernetes.github.io/autoscaler"
  values = [templatefile("${path.module}/cluster_autoscaler.yaml",
    {
      cluster_name    = var.cluster_name
      cluster_version = var.cluster_version
      region          = var.region
  })]
}
