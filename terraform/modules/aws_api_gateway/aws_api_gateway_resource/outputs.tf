//resource id, method ids, integration ids
output "resource_id" {
    value = aws_api_gateway_resource.resource.id
}

output "method_ids" {
    value = [ for k, v in aws_api_gateway_method.method : v.id ]
}

output "integration_ids" {
    value = [ for k, v in aws_api_gateway_integration.integration : v.id ]
}