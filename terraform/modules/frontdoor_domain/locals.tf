locals {
  domain_name   = "${var.name}-custom-domain"
  rc_tags = {
    Name        = var.name
    env         = var.env
    profile     = var.profile
    author      = "rapid-cloud"
    cmd_id      = var.cmd_id
    workload    = var.workload
  }
}