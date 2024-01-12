resource "aws_organizations_account" "account" {
  name      = var.name
  email     = var.email
  parent_id = var.parent_id
  lifecycle {
    ignore_changes = [
      name,
      email
    ]

    prevent_destroy = true
  }
}

resource "aws_organizations_policy_attachment" "attachment" {
  for_each = {for i, v in var.scps: i => v}
  policy_id = each.value
  target_id = resource.aws_organizations_account.account.id
}