# Replication Instance

A terrafrom module to create a DMS replication instance
This module will create the following:

- IAM role `iam.tf`
- Security group `security-group.tf`
- Subnet Group `subnet-group.tf`
- Replication Instance `replication-instance.tf`
### TODO: add kms key

### Security Group Rules


Use the following to create security rules:

This will create two ingress rule with :

`description`: allow icmp
`from_port`: 443
`to_port` : 443
`protocol` : tcp
`cidr`: 0.0.0.0/0

`description`: allow udp
`from_port`: 53
`to_port` : 53
`protocol` : udp
`cidr`: 0.0.0.0/0

```
  cidr_ingress_rules = {
    "allow https" = "443,443,tcp,0.0.0.0/0"
    "allow dns" = "53,53,udp,0.0.0.0/0"
  }

```


## Example Usage
```
module "rep_instance_1" {
  env                                      = "${var.env}"
  source                                   = "../../dms/replication-instance"
  replication_instance_id                  = "${var.env}-rep-instance-1"
  replication_group_destination_subnets    = "${data.aws_subnet_ids.vpc.ids}"
  replication_instance_sg_egress_ports     = ["1521", "1433"]
  replication_instance_egress_cidr_blocks  = ["0.0.0.0/0"]
  replication_instance_sg_ingress_ports    = ["1521", "1433"]
  replication_instance_ingress_cidr_blocks = ["0.0.0.0/0"]
  vpc_id                                   = "vpc-5881c430"
  availability_zone                        = "us-west-2c"
  create_dms_iam_roles                     = 1

  tags = {
    "Name" = "rep-instance-2"
    "App"  = "DMS"
  }
}
```
## Inputs

This module has the following avaialbe Inputs, Inputs without a `default` value are **mandatory** and must be set in the calling module ( see example above )

| Name | Description | Type | Default | Required |
|------|-------------|:----:|:-----:|:-----:|
| allocated\_storage | The amount of storage (in gigabytes) to be initially allocated for the replication instance | string | `"50"` | no |
| apply\_immediately | Indicates whether the changes should be applied immediately or during the next maintenance window. | string | `"false"` | no |
| auto\_minor\_version\_upgrade | Indicates that minor engine upgrades will be applied automatically to the replication instance during the maintenance window | string | `"false"` | no |
| availability\_zone | The EC2 Availability Zone that the replication instance will be created in | string | n/a | yes |
| create\_dms\_iam\_roles | Needed once per AWS account | string | `"0"` | no |
| engine\_version | The engine version number of the replication instance | string | `"3.1.3"` | no |
| env | Environment name | string | n/a | yes |
| kms\_key\_arn | The Amazon Resource Name (ARN) for the KMS key that will be used to encrypt the connection parameters | string | `""` | no |
| multi\_az | Specifies if the replication instance is a multi-az deployment. You cannot set the availability_zone parameter if the multi_az parameter is set to true. | string | `"false"` | no |
| preferred\_maintenance\_window | The weekly time range during which system maintenance can occur, in Universal Coordinated Time (UTC) | string | `"sun:10:30-sun:14:30"` | no |
| publicly\_accessible | A value of true represents an instance with a public IP address | string | `"false"` | no |
| replication\_group\_destination\_subnets | The VPC subnet used to create the replication subnet group | list | n/a | yes |
| replication\_instance\_class | The compute and memory capacity of the replication instance as specified by the replication instance class | string | `"dms.t2.micro"` | no |
| replication\_instance\_egress\_cidr\_blocks | The CIDR allowed egress access to the Replication Instance | list | n/a | yes |
| replication\_instance\_id | The replication instance identifier | string | n/a | yes |
| replication\_instance\_ingress\_cidr\_blocks | The CIDR allowed ingress access to the Replication Instance | list | n/a | yes |
| replication\_instance\_sg\_egress\_ports | List of egress ports to the DMS instance | list | n/a | yes |
| replication\_instance\_sg\_ingress\_ports | List of ingress ports to the DMS instance | list | n/a | yes |
| replication\_subnet\_group\_ids | A subnet group to associate with the replication instance | list | `<list>` | no |
| tags | Map of tags to add to the resources | map | `<map>` | no |
| vpc\_id | The VPC in which to create the DMS instance, subnet and security group | string | n/a | yes |
| vpc\_security\_group\_ids | A list of VPC security group IDs to be used with the replication instance. The VPC security groups must work with the VPC containing the replication instance. | list | `<list>` | no |

## Outputs

| Name | Description |
|------|-------------|
| arn |  The replication instance |

