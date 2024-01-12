## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|:----:|:-----:|:-----:|
| allocated\_storage |  | string | `""` | no |
| allowed\_ips |  | list | `<list>` | no |
| allowed\_sgs |  | list | `<list>` | no |
| backup\_retention\_period |  | string | `"30"` | no |
| cloudwatch\_logs\_retention\_in\_days |  | string | `"30"` | no |
| cluster\_identifier | The cluster name | string | n/a | yes |
| cluster\_instance\_count |  | string | `"1"` | no |
| cluster\_instance\_size |  | string | `"db.t2.micro"` | no |
| database\_name |  | string | `"test"` | no |
| db\_subnets |  | list | n/a | yes |
| deletion\_protection |  | string | `"false"` | no |
| engine |  | string | `"mysql"` | no |
| engine\_version |  | string | `"5.7.22"` | no |
| env |  | string | n/a | yes |
| master\_password |  | string | n/a | yes |
| master\_username |  | string | n/a | yes |
| monitoring\_interval |  | string | n/a | yes |
| parameters | A list of value to apply to the paramter group | list | `<list>` | no |
| port | port the server will be listening on | string | 3306 | no |
| server\_audit\_events |  | string | `"CONNECT,QUERY,QUERY_DCL,QUERY_DDL,QUERY_DML"` | no |
| tags | Map of tags to add to the resources | map | `<map>` | no |
| vpc\_id |  | string | n/a | yes |

