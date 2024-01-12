locals {
  node_pool_name = "${var.name}"
  rc_tags = {
    Name        = var.name
    env         = var.env
    profile     = var.profile
    author      = "rapid-cloud"
    cmd_id      = var.cmd_id
    workload    = var.workload
  }
}