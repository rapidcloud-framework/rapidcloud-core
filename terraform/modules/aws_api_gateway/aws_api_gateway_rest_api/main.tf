resource "aws_api_gateway_rest_api" "gw" {
    name = var.name
    disable_execute_api_endpoint = var.disable_execute_api_endpoint
    # https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/api_gateway_rest_api#endpoint_configuration
    # If set to PRIVATE recommend to set put_rest_api_mode = merge 
    # to not cause the endpoints and associated Route53 records to be deleted.
    # only available in latest provider
    #put_rest_api_mode = lower(var.endpoint_type) == "private" ? "merge" : "overwrite"
    endpoint_configuration {
        types = [var.endpoint_type]
    }
    tags = var.tags
}