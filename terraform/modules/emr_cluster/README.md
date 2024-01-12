## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|:----:|:-----:|:-----:|
| cluster\_name | The cluster name, will be used to tag/name resources | string | n/a | yes |
| core\_instance\_count | The number of core nodes to build | string | n/a | yes |
| core\_instance\_type | The instance size used for core nodes | string | n/a | yes |
| region | The VPC ID where this cluster will reside | string | n/a | yes |
| subnet\_id | The subnet where the cluster nodes will reside | string | n/a | yes |
| tags | Map of tags to assign to this bucket | map | n/a | yes |
| vpc\_id | The VPC ID where this cluster will reside | string | n/a | yes |

| Name | Description | Type | Default | Required |
|------|-------------|:----:|:-----:|:-----:|
| applications | A list of applications for the cluster. Valid values are: Flink, Hadoop, Hive, Mahout, Pig, Spark, and JupyterHub (as of EMR 5.14.0). Case insensitive | list | `<list>` | no |
| configuration\_json\_file\_name | A json file containing extra configuration for the cluster | string | `"none.json"` | no |
| core\_cidr\_ingress\_rules | A list of INGRESS cidr's to add to the slaves security group | list | `<list>` | no |
| core\_instance\_bid\_price | Optional, if specificed will use spot instances | string | `""` | no |
| core\_sg\_ingress\_rules | A list of INGRESS sg's to add to the slaves security group | list | `<list>` | no |
| master\_cidr\_ingress\_rules | A list of INGRESS cidr's to add to the masters security group | list | `<list>` | no |
| master\_instance\_count | The number of master nodes to build, can be 1 or 3 only | string | `"1"` | no |
| master\_instance\_type | The instance size used for master nodes | string | `"m5.xlarge"` | no |
| master\_sg\_ingress\_rules | A list of INGRESS sg's to add to the masters security group | list | `<list>` | no |
| ssh\_pub\_key | The rsa pub key used to ssh into cluster nodes, needs to be generate via ssh-keygen -t rsa | string | n/a | no |
| release\_label | The release label for the Amazon EMR release | string | `"emr-5.26.0"` | no |

## Outputs

| Name | Description |
|------|-------------|
| core\_sg |  |
| instance\_profile |  |
| master\_sg |  |
| service\_role |  |

