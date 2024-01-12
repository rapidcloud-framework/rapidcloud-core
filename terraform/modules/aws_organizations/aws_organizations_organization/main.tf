resource "aws_organizations_organization" "main" {
  feature_set = "ALL"

  aws_service_access_principals = var.aws_service_access_principals
  enabled_policy_types = var.enabled_policy_types
  lifecycle {
    ignore_changes = [
      feature_set
    ]
  }
}