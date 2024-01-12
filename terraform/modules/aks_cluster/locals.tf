locals {
  cluster_name    = var.name
  rc_tags = {
    Name        = local.cluster_name
    profile     = var.profile
    author      = "rapid-cloud"
  }
}