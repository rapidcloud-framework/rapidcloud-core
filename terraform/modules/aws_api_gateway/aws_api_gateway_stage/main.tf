resource "aws_api_gateway_deployment" "deployment" {
  rest_api_id = var.rest_api_id

  triggers = {
    redeployment = sha1(jsonencode(var.triggers))
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "stage" {
    rest_api_id   = var.rest_api_id
    deployment_id = aws_api_gateway_deployment.deployment.id
    stage_name    = var.stage_name
}