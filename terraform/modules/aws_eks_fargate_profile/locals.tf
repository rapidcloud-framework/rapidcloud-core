locals {
  cluster_name = var.cluster_name
  profile_name = "${var.cluster_name}-${var.profile_name}"
  rc_tags = {
    Name        = local.profile_name
    ClusterName = local.cluster_name
    env         = var.env
    profile     = var.profile
    author      = "rapid-cloud"
    fqn         = var.fqn
    cmd_id      = var.cmd_id
    workload    = var.workload
  }
  subnet_ids = [for subnet, id in var.subnet_ids : id]
}

