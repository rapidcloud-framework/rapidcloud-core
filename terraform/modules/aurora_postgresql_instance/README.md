## RDS POSGRESQL
This module creates an RDS postgresql cluster, it will create:
1. a subnet group
2. a paramter group
3. a security group
4. an rds cluster
5. one or more instances to acheive HA

## SECRETS
Use the `aws_kms_secrets` and `aws kms encrypt` to store the password for the master account

```

# how to generate a kms payload for password
# 1. echo -n 'master-password' > plaintext-password
# 2. aws kms encrypt --key-id ab123456-c012-4567-890a-deadbeef123 --plaintext fileb://plaintext-password --encryption-context foo=bar --output text --query CiphertextBlob
# this will output a blob : AQECAHgaPa0J8WadplGCqqVAr4HNvDaF.....
# That encrypted output can now be inserted into Terraform configurations without exposing the plaintext secret directly.
```

### example usage
```
data "aws_kms_secrets" "psql" {
  secret {
    name = "psql_instance1_password"

    #   payload = "AQICAHjW3wL+vloD6wOqPVNL78G0EXzPUtS1R6zyNJ3UfttMCAFIgnHl3nBJy6uxr5QpqWdUAAAAfzB9BgkqhkiG9w0BBwagcDBuAgEAMGkGCSqGSIb3DQEHATAeBglghkgBZQMEAS4wEQQMQeraYolzw41DfBOAAgEQgDw0Zg6sKLG+p+Kjq29okCrMxtvwDiC7zVKWKi3WCAN95QlG0l+bujfPu7vnQSPcrDwNmpxmDWa8yWZpYGk="
    payload = "AQICAHjW3wL+vloD6wOqPVNL78G0EXzPUtS1R6zyNJ3UfttMCAGx2W9rfPJ7/7wgxx02tlCtAAAAfjB8BgkqhkiG9w0BBwagbzBtAgEAMGgGCSqGSIb3DQEHATAeBglghkgBZQMEAS4wEQQMExO3pjdFB9sd3BexAgEQgDuvwqQ9T3lkLi5kM/7XwsXHhw3MO2mNcPwTZ7lNOGEocSuNcYa0cdf8byw8x+CHXnjPugjVG5azpoJ0+A=="
  }
}
```

## RDS CREATION EXAMPLE
```
# see above for how to generate this
output "psql_pass" {
  value = "${data.aws_kms_secrets.psql.plaintext["psql_instance1_password"]}"
}

module "psql_instance" {
  source                 = "../../../../platform-engineering/terraform-modules/rds/postgresql"
  cluster_identifier     = "${data.template_file.prefix.rendered}-psql"
  cluster_instance_count = 1
  cluster_instance_size  = "db.r4.large"
  vpc_id                 = "${data.aws_vpc.vpc.id}"
  azs                    = "${var.azs}"
  engine_version         = "10.4"
  database_name          = "test"
  master_username        = "postgres"

  master_password = "pk0Jl0RRNadclqt7HDDSOR1jFmIZx5sj"

  # master_password   = "${data.aws_kms_secrets.psql.plaintext["psql_instance1_password"]}"
  kms_key_id          = "${data.aws_kms_key.rds.arn}"
  storage_encrypted   = true
  param_group_family  = "aurora-postgresql10"
  allowed_ips         = ["${var.cidr}"]
  subnet_ids          = ["${data.aws_subnet.private_az1.id}", "${data.aws_subnet.private_az2.id}"]
  monitoring_interval = 60

  tags = {
    "Name"     = "${data.template_file.prefix.rendered}-psql"
    "author"   = "${var.author}"
    "env"      = "${var.env}"
    "workload" = "${var.workload}"
  }

  parameters = [
    {
      name  = "enable_hashjoin"
      value = true
    },
  ]
}
```

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|:----:|:-----:|:-----:|
| allowed\_ips | A list of IPs or CIDR's which are allowed access to this instance | list | `<list>` | no |
| allowed\_sgs | A list of Security Groups which are allowed access to this instance | list | `<list>` | no |
| azs | A list of EC2 Availability Zones for the DB cluster storage where DB cluster instances can be created | list | n/a | yes |
| backup\_retention\_period | The days to retain backups | string | `"7"` | no |
| cluster\_identifier | The cluster name | string | n/a | yes |
| cluster\_instance\_count | The RDS instance count, use 2 for replication | string | `"1"` | no |
| cluster\_instance\_size | The RDS instance size | string | n/a | yes |
| database\_name | Name for an automatically created database on cluster creation | string | n/a | yes |
| deletion\_protection | If the DB instance should have deletion protection enabled, set to true for prod | string | `"false"` | no |
| enabled\_cloudwatch\_logs\_exports | List of log types to export to cloudwatch | list | `<list>` | no |
| engine\_version | The engine version this cluster will use | string | n/a | yes |
| kms\_key\_id | Kms key used for encription | string | n/a | yes |
| master\_password | Password for the master DB user | string | n/a | yes |
| master\_username | Username for the master DB user | string | n/a | yes |
| monitoring\_interval | The interval, in seconds, between points when Enhanced Monitoring metrics are collected for the DB instance. To disable collecting Enhanced Monitoring metrics, specify 0. The default is 0. Valid Values: 0, 1, 5, 10, 15, 30, 60. | string | `"0"` | no |
| param\_group\_family | The family used for creating the RDS paramter group | string | n/a | yes |
| parameters | A list of value to apply to the paramter group | list | `<list>` | no |
| skip\_final\_snapshot | Determines whether a final DB snapshot is created before the DB cluster is deleted, set to false if you dont need one | string | `"true"` | no |
| storage\_encrypted | Specifies whether the DB cluster is encrypted | string | `"true"` | no |
| subnet\_ids | The subnets the RDS subnet group will use | list | `<list>` | no |
| tags | Map of tags to add to the resources | map | `<map>` | no |
| vpc\_id | The ID of the VPC where the RDS cluster will be created | string | n/a | yes |

