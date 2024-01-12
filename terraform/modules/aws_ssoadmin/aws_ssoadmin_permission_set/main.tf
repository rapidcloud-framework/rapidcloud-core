data "aws_ssoadmin_instances" "main" {}

locals {
    sso_instance_arn          = tolist(data.aws_ssoadmin_instances.main.arns)[0]
    inline_policy_exists      = trimspace(var.inline_policy) != "" ? 1 : 0
    aws_managed_policy_arns   = { for _, arn in var.aws_managed_policy_arns: arn => arn }
    customer_managed_policies = { for _, policy in var.customer_managed_policies: policy.name => policy }
}

resource "aws_ssoadmin_permission_set" "main" {
  name             = var.name
  description      = var.description
  instance_arn     = local.sso_instance_arn
  relay_state      = var.relay_state
  session_duration = var.session_duration
  tags             = var.tags
}

resource "aws_ssoadmin_permission_set_inline_policy" "main" {
  count              = local.inline_policy_exists
  inline_policy      = var.inline_policy
  instance_arn       = local.sso_instance_arn
  permission_set_arn = aws_ssoadmin_permission_set.main.arn
}

resource "aws_ssoadmin_managed_policy_attachment" "main" {
  for_each           = local.aws_managed_policy_arns
  instance_arn       = local.sso_instance_arn
  managed_policy_arn = each.value
  permission_set_arn = aws_ssoadmin_permission_set.main.arn
}

resource "aws_ssoadmin_customer_managed_policy_attachment" "main" {
  for_each           = local.customer_managed_policies
  instance_arn       = local.sso_instance_arn
  permission_set_arn = aws_ssoadmin_permission_set.main.arn
  customer_managed_policy_reference {
    name = each.value.name
    path = each.value.path
  }
}