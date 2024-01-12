data "aws_caller_identity" "current" {}

resource "aws_api_gateway_resource" "resource" {
  rest_api_id = var.rest_api_id
  parent_id   = var.parent_resource_id
  path_part   = var.path_part
}

resource "aws_api_gateway_method" "method" {
  for_each      = { for i, v in var.lambda_integrations : v["http_method"] => v }
  rest_api_id   = var.rest_api_id
  resource_id   = aws_api_gateway_resource.resource.id
  http_method   = each.value.http_method
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "integration" {
  for_each                = { for i, v in var.lambda_integrations : v["http_method"] => v }
  rest_api_id             = var.rest_api_id
  resource_id             = aws_api_gateway_resource.resource.id
  http_method             = aws_api_gateway_method.method[each.key]["http_method"]
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "arn:aws:apigateway:${var.region}:lambda:path/2015-03-31/functions/arn:aws:lambda:${var.region}:${data.aws_caller_identity.current.account_id}:function:${each.value.lambda_name}/invocations"
}

resource "aws_lambda_permission" "integration" {
  for_each      = { for i, v in var.lambda_integrations : v["http_method"] => v }
  statement_id  = "AllowExecutionFromAPIGateway-${aws_api_gateway_method.method[each.key]["http_method"]}"
  action        = "lambda:InvokeFunction"
  function_name = each.value.lambda_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "arn:aws:execute-api:${var.region}:${data.aws_caller_identity.current.account_id}:${var.rest_api_id}/*/${aws_api_gateway_method.method[each.key]["http_method"]}${aws_api_gateway_resource.resource.path}"
}
