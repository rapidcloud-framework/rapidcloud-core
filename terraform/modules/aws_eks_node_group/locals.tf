locals {
  node_group_name = "${var.cluster_name}-${var.node_group_name}"
  cluster_name    = var.cluster_name
  rc_tags = {
    Name        = local.node_group_name
    ClusterName = local.node_group_name
    env         = var.env
    profile     = var.profile
    author      = "rapid-cloud"
    fqn         = var.fqn
    cmd_id      = var.cmd_id
    workload    = var.workload
  }
  subnet_ids = [for subnet, id in var.subnet_ids : id]
}
