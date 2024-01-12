resource "aws_organizations_policy" "scp" {
  name        = var.name
  content     = var.policy_text
  description = var.description
}