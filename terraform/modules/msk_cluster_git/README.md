# Managed Streaming For Kafka

This module builds a Kafka cluster for theia

### example usage

```
module "kinect_theia_1_for_moti_msk_cluster" {
  source                 = "./msk"
  cluster_name           = "my_kafka_cluster"
  number_of_broker_nodes = "2"
  instance_type          = "kafka.t3.small"
  volume_size            = "10"
  kms_key_id             = aws_kms_key.key.arn
  kafka_version = "2.2.1"
  encryption_in_transit = "TLS_PLAINTEXT"
  log_retention_in_days = "7"
  enhanced_monitoring = "PER_BROKER"
  server_properties = "auto.create.topics.enable  = true\nunclean.leader.election.enable  = true\ndefault.replication.factor = 2\n"
  broker_subnets         = tolist(data.aws_subnet_ids.private.ids)
  allowed_cidrs = tolist(["172.30.10.0/24", "172.30.20.0/24"])
  allowed_sgs = tolist(["sg-xxxxxxxxx", "sg-yyyyyyyyy"])
  vpc_id                 = "vpc-vvvvvvvv"
  tags = {
    "Name"     = "my_kafka_cluster"
    "env"      = "prod"
  }
}

```
