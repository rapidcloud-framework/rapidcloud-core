locals {
  node_pool_name = "${var.name}"
  cluster_name    = var.cluster_name
  rc_tags = {
    Name        = local.node_pool_name
    ClusterName = var.cluster_name
    env         = var.env
    profile     = var.profile
    author      = "rapid-cloud"
    cmd_id      = var.cmd_id
    workload    = var.workload
  }
}