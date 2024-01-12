data "conformity_external_id" "main"{}

resource "aws_cloudformation_stack" "cloud_conformity_stack" {
  name         = var.stack_name
  template_url = "https://s3-us-west-2.amazonaws.com/cloudconformity/CloudConformity.template"
  parameters = {
    AccountId  = "717210094962"
    ExternalId = data.conformity_external_id.main.external_id
  }
  capabilities = ["CAPABILITY_NAMED_IAM"]
}

resource "conformity_aws_account" "conformity_setup" {
    name        = var.conformity_aws_account_name
    environment = var.conformity_environment
    role_arn    = aws_cloudformation_stack.cloud_conformity_stack.outputs["CloudConformityRoleArn"]
    external_id = data.conformity_external_id.main.external_id
    tags        = var.tags
}