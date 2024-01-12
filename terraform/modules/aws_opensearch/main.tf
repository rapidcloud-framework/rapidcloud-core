resource "aws_cloudwatch_log_group" "opensearch_log_group_rc" {
  name_prefix = "opensearch-log-group-rc"
}

resource "aws_cloudwatch_log_resource_policy" "opensearch_log_group_rc_policy" {
  policy_name = "opensearch-log-group-rc-policy"

  policy_document = <<CONFIG
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "es.amazonaws.com"
      },
      "Action": [
        "logs:PutLogEvents",
        "logs:PutLogEventsBatch",
        "logs:CreateLogStream"
      ],
      "Resource": "arn:aws:logs:*"
    }
  ]
}
CONFIG
}


resource "aws_opensearch_domain" "main" {
  domain_name = var.name
  engine_version = "OpenSearch_2.3"

  cluster_config {
    instance_count = var.nodes
    instance_type = var.instance_type
    zone_awareness_enabled = var.high_availability
  }

  auto_tune_options {
    desired_state = var.autotune
    rollback_on_disable = "NO_ROLLBACK"
  }

  ebs_options {
    ebs_enabled = true
    iops = var.iops
    throughput = var.throughput
    volume_size = var.ebs_storage_size
  }

  log_publishing_options {
    cloudwatch_log_group_arn = aws_cloudwatch_log_group.opensearch_log_group_rc.arn
    log_type = "INDEX_SLOW_LOGS"
  }

  vpc_options {
    subnet_ids = var.subnet_ids
    security_group_ids = var.security_group_ids
  }
  
  tags = var.tags

}