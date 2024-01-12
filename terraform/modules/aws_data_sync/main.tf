resource "aws_datasync_agent" "agent" {
  name                  = var.agent_name
  ip_address            = var.ip_address
  security_group_arns   = var.security_groups_arns
  subnet_arns           = var.subnet_arns
  vpc_endpoint_id       = aws_vpc_endpoint.vpc_endpoint.id
  private_link_endpoint = data.aws_network_interface.net_interface.private_ip
  tags                  = var.tags
}
resource "aws_datasync_location_nfs" "source" {
  server_hostname = var.server_hostname
  subdirectory    = var.nfs_subdirectory
  on_prem_config {
    agent_arns = [aws_datasync_agent.agent.arn]
  }
  tags = merge(
    var.tags,
    {
      Name = var.nfs_location_name
    },
  )
}
resource "aws_datasync_location_s3" "destination" {
  s3_bucket_arn = var.s3_bucket_arn
  subdirectory  = var.s3_subdirectory
  s3_config {
    bucket_access_role_arn = aws_iam_role.s3_bucket_role.arn
  }
  tags = merge(
    var.tags,
    {
      Name = var.s3_location_name
    },
  )

}
data "aws_iam_policy_document" "s3_policy_doc_assume" {
  statement {
    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com","datasync.amazonaws.com"]
    }
    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "s3_bucket_role" {
  name               = "${var.tags["profile"]}_s3_rol_${var.agent_name}"
  assume_role_policy = data.aws_iam_policy_document.s3_policy_doc_assume.json
  inline_policy {
    name = "${var.tags["profile"]}_s3_policy_${var.agent_name}"

    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Action   = ["s3:PutObject","s3:ListBucket","s3:DeleteObject"]
          Effect   = "Allow"
          Resource = ["${var.s3_bucket_arn}","${var.s3_bucket_arn}/*"]
        },
      ]
    })
  }  
}

resource "aws_vpc_endpoint" "vpc_endpoint" {
  service_name       = "com.amazonaws.${data.aws_region.current.name}.datasync"
  vpc_id             = var.vpc_id
  security_group_ids = var.security_group_ids
  subnet_ids         = var.subnet_ids
  vpc_endpoint_type  = "Interface"
  tags               = var.tags

}
data "aws_network_interface" "net_interface" {
  id = tolist(aws_vpc_endpoint.vpc_endpoint.network_interface_ids)[0]
}
data "aws_region" "current" {}