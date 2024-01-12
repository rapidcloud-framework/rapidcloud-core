resource "aws_msk_configuration" "msk" {
  kafka_versions = [var.kafka_version]
  name           = var.cluster_name

  server_properties = <<PROPERTIES
  ${var.server_properties}
PROPERTIES

  lifecycle {
    create_before_destroy = true
  }
}


resource "aws_msk_cluster" "msk" {
  cluster_name           = var.cluster_name
  kafka_version          = var.kafka_version
  number_of_broker_nodes = var.number_of_broker_nodes
  enhanced_monitoring    = var.enhanced_monitoring
  configuration_info {
    arn      = aws_msk_configuration.msk.arn
    revision = aws_msk_configuration.msk.latest_revision

  }

  broker_node_group_info {
    instance_type   = var.instance_type
    ebs_volume_size = var.volume_size
    client_subnets  = var.broker_subnets
    security_groups = [aws_security_group.msk.id]
  }

  encryption_info {
    encryption_in_transit {
      client_broker = var.encryption_in_transit
    }
    encryption_at_rest_kms_key_arn = var.kms_key_id
  }

  # open_monitoring {
  #   prometheus {
  #     jmx_exporter {
  #       enabled_in_broker = var.jmx_exporter
  #     }
  #     node_exporter {
  #       enabled_in_broker = var.node_exporter
  #     }
  #   }
  # }

  logging_info {
    broker_logs {
      cloudwatch_logs {
        enabled   = true
        log_group = aws_cloudwatch_log_group.msk.name
      }
      # firehose {
      #   enabled         = true
      #   delivery_stream = aws_kinesis_firehose_delivery_stream.test_stream.name
      # }
      # s3 {
      #   enabled = true
      #   bucket  = aws_s3_bucket.bucket.id
      #   prefix  = "logs/msk-"
      # }
    }
  }

  tags = merge(var.tags, tomap({"Name" = var.cluster_name}))
}

output "zookeeper_connect_string" {
  value = aws_msk_cluster.msk.zookeeper_connect_string
}

output "bootstrap_brokers" {
  description = "host:port pairs"
  value       = aws_msk_cluster.msk.bootstrap_brokers
}

output "bootstrap_brokers_tls" {
  description = "TLS host:port pairs"
  value       = aws_msk_cluster.msk.bootstrap_brokers_tls
}
