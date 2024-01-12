resource "aws_organizations_organizational_unit" "ou" {
  name      = var.name
  parent_id = var.parent_id
}

resource "aws_organizations_policy_attachment" "attachment" {
  for_each = {for i, v in var.scps: i => v}
  policy_id = each.value
  target_id = resource.aws_organizations_organizational_unit.ou.id
}
