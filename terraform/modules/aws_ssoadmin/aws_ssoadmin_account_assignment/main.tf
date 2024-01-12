data "aws_ssoadmin_instances" "main" {}

locals {
  identity_store_id = tolist(data.aws_ssoadmin_instances.main.identity_store_ids)[0]
  sso_instance_arn  = tolist(data.aws_ssoadmin_instances.main.arns)[0]
  principal_ids     = { for _, id in var.principal_ids: id => id }
}

resource "aws_ssoadmin_account_assignment" "main" {
  for_each           = local.principal_ids
  instance_arn       = local.sso_instance_arn
  permission_set_arn = var.permission_set_arn
  principal_id       = each.value
  principal_type     = var.principal_type
  target_id          = var.account_id
  target_type        = "AWS_ACCOUNT"
}