data "aws_ssoadmin_instances" "main" {}

locals {
  identity_store_id = tolist(data.aws_ssoadmin_instances.main.identity_store_ids)[0]
}

resource "aws_identitystore_user" "main" {
  identity_store_id = local.identity_store_id

  display_name = var.display_name
  user_name    = var.user_name

  name {
    given_name  = var.first_name
    family_name = var.last_name
  }

  emails {
    value = var.email
  }
}