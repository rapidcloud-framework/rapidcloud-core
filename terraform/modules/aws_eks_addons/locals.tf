locals {
  cluster_name = var.cluster_name
  profile_name = "${var.cluster_name}-coredns"
  rc_tags = {
    Name     = "${var.cluster_name}"
    env      = var.env
    profile  = var.profile
    author   = "rapid-cloud"
    fqn      = var.fqn
    cmd_id   = var.cmd_id
    workload = var.workload
  }
  subnet_ids = [for subnet, id in var.subnet_ids : id]

}
