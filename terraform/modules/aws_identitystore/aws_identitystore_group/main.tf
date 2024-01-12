data "aws_ssoadmin_instances" "main" {}

locals {
  identity_store_id = tolist(data.aws_ssoadmin_instances.main.identity_store_ids)[0]
  user_ids = { for idx, u in var.user_ids: idx => u }
}

resource "aws_identitystore_group" "main" {
  display_name      = var.display_name
  description       = var.description
  identity_store_id = local.identity_store_id
}

resource "aws_identitystore_group_membership" "example" {
  for_each          = local.user_ids
  identity_store_id = local.identity_store_id
  group_id          = aws_identitystore_group.main.group_id
  member_id         = each.value
}