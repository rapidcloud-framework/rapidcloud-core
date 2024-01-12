# REDSHIFT CLUSTER
This is an *opininated* module which assumes the cluster will reside in a VPC, it will create the following:
- paramter group
- security group
- redshift cluster
- logging bucket

## Supported version
This module was built and tested for terraform 0.12.8

## Parameter Group

A parameter group is create for each cluster by default, to add parameters use the `paramters` map.
Refer to : https://docs.aws.amazon.com/redshift/latest/mgmt/working-with-parameter-groups.html for options.

Example map:
```
  parameters = {
    "require_ssl"                  = "true"
    "enable_user_activity_logging" = "true"
  }
```

## Security Group
Will open access to `cluster_port` from `allowed_cidr`

## Logging Bucket
Will be created if `enable_logging` is enabled


## Sample usage
```

module "redshift_cluster" {
  source          = "../../../../terraform-modules-aws/redshift"
  cluster_name    = "${data.template_file.prefix.rendered}-redshift-cluster"
  subnets         = [data.aws_subnet.private_az1.id, data.aws_subnet.private_az2.id]
  node_count      = 1
  master_username = "datalake"
  master_password = "us3_KMS_h3r3"
  vpc_id          = data.aws_vpc.vpc.id
  allowed_cidr    = [data.aws_subnet.private_az1.cidr_block, data.aws_subnet.private_az2.cidr_block]
  kms_key_id      = "${data.aws_kms_key.redshift.arn}"
  # enable_logging  = true

  parameters = {
    "require_ssl"                  = "true"
    "enable_user_activity_logging" = "true"
  }
  tags = {
    Name = "${data.template_file.prefix.rendered}-redshift-cluster"
    Tier = "private"
  }

}

output "redshift_cluster_identifier" {
  value = module.redshift_cluster.cluster_identifier
}
output "redshift_cluster_endpoint" {
  value = module.redshift_cluster.endpoint
}
output "redshift_cluster_dns_name" {
  value = module.redshift_cluster.dns_name
}

```

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|:----:|:-----:|:-----:|
| allow\_version\_upgrade | If true , major version upgrades can be applied during the maintenance window to the Amazon Redshift engine that is running on the cluster | string | `"true"` | no |
| allowed\_cidr | This CIDR is allowed ingress access to the Redshift port ( 5439 by default ) | list | n/a | yes |
| automated\_snapshot\_retention\_period | The number of days that automated snapshots are retained. If the value is 0, automated snapshots are disabled | string | `"1"` | no |
| availability\_zone | The EC2 Availability Zone (AZ) in which you want Amazon Redshift to provision the cluster | string | `""` | no |
| cluster\_name | The Cluster Name | string | n/a | yes |
| cluster\_port | Redhsift Cluster Port | string | `"5439"` | no |
| database\_name | The name of the first database to be created when the cluster is created. If you do not provide a name, Amazon Redshift will create a default database called dev | string | `"dev"` | no |
| enable\_logging | Enables logging | string | `"false"` | no |
| encrypted | If true , the data in the cluster is encrypted at rest | string | `"true"` | no |
| final\_snapshot\_identifier | The name of the snapshot from which to create the new cluster | string | `""` | no |
| kms\_key\_id | The ARN for the KMS encryption key. When specifying kms_key_id, encrypted needs to be set to true | string | n/a | yes |
| master\_password | (Required unless a snapshot_identifier is provided) Password for the master DB user, DO NOT USE PLAIN TEXT HERE | string | `""` | no |
| master\_username | (Required unless a snapshot_identifier is provided) Username for the master DB user | string | `""` | no |
| node\_count | The number of compute nodes in the cluster, setting this to more then the default 1 will create a multi-node cluste | string | `"1"` | no |
| node\_type | Size of the compute nodes, https://docs.aws.amazon.com/redshift/latest/mgmt/working-with-clusters.html | string | `"dc2.large"` | no |
| parameters | A map containing a list of desired paramaters | map | n/a | yes |
| preferred\_maintenance\_window | The weekly time range (in UTC) during which automated cluster maintenance can occur. Format: ddd:hh24:mi-ddd:hh24:mi | string | `"sat:10:00-sat:10:30"` | no |
| skip\_final\_snapshot | Determines whether a final snapshot of the cluster is created before Amazon Redshift deletes the cluster, if true a snapshot will be created | string | `"true"` | no |
| snapshot\_cluster\_identifier | The name of the cluster the source snapshot was created from | string | `""` | no |
| snapshot\_identifier | The name of the snapshot from which to create the new cluster | string | `""` | no |
| subnets | The subnets where the cluster will reside | list | n/a | yes |
| tags | A map of tags to attach to resources | map | n/a | yes |
| vpc\_id | The VPC where the cluster will reside | string | n/a | yes |

