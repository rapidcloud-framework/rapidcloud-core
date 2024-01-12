## Requirements

| Name | Version |
|------|---------|
| terraform | >= 0.12 |

## Providers

| Name | Version |
|------|---------|
| aws | n/a |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| allocated\_storage | n/a | `string` | `""` | no |
| allowed\_ips | n/a | `list(any)` | `[]` | no |
| allowed\_sgs | n/a | `list(any)` | `[]` | no |
| backup\_retention\_period | n/a | `number` | `30` | no |
| cloudwatch\_logs\_retention\_in\_days | n/a | `number` | `30` | no |
| database\_name | Database name | `string` | `"test"` | no |
| database\_password | The DB Password | `any` | n/a | yes |
| database\_username | The DB username | `any` | n/a | yes |
| db\_subnets | n/a | `list(any)` | n/a | yes |
| deletion\_protection | n/a | `bool` | `false` | no |
| enabled\_cloudwatch\_logs\_exports | n/a | `list` | <pre>[<br>  "audit",<br>  "error",<br>  "general",<br>  "slowquery"<br>]</pre> | no |
| engine | n/a | `string` | `"mysql"` | no |
| engine\_version | n/a | `string` | `"5.7.22"` | no |
| env | n/a | `any` | n/a | yes |
| instance\_class | n/a | `string` | `"db.t2.micro"` | no |
| instance\_name | The db instance name | `any` | n/a | yes |
| max\_allocated\_storage | n/a | `string` | `""` | no |
| monitoring\_interval | n/a | `number` | `0` | no |
| multi\_az | n/a | `bool` | `false` | no |
| parameters | A list of value to apply to the paramter group | `list(map(string))` | `[]` | no |
| port | n/a | `number` | `3306` | no |
| storage\_type | n/a | `string` | `"gp2"` | no |
| tags | Map of tags to add to the resources | `map(string)` | `{}` | no |
| vpc\_id | n/a | `any` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| endpoint | ------------------------------------------------------------------------------ Outputs ------------------------------------------------------------------------------ |
| id | n/a |

