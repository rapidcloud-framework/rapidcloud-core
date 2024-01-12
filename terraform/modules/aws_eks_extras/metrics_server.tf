resource "helm_release" "metrics_server" {
  count      = tobool(var.install_metrics_server) ? 1 : 0
  name       = "metrics-server"
  namespace  = "kube-system"
  chart      = "metrics-server"
  repository = "https://kubernetes-sigs.github.io/metrics-server"
  values     = [templatefile("${path.module}/metrics_server.yaml", {})]
}
