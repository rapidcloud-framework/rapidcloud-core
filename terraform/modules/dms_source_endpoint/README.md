# Source Endpoint

This module creates a source endpoint

## Example Usage
```

module "oracle_source_endpoint_1" {
  source        = "../../dms/source_endpoint"
  endpoint_id   = "${var.env}-oracle-source-endpoint-1"
  engine_name   = "oracle"
  username      = "DLPULL"
  password      = "test"
  server_name   = "10.20.1.186"
  port          = 6021
  database_name = "cflysitg"
}
```
## Inputs

This module has the following avaialbe Inputs, Inputs without a `default` value are **mandatory** and must be set in the calling module ( see example above )

| Name | Description | Type | Default | Required |
|------|-------------|:----:|:-----:|:-----:|
| certificate\_arn | The Amazon Resource Name (ARN) for the certificate. | string | `""` | no |
| database\_name | The database to connect to | string | n/a | yes |
| endpoint\_id | The database endpoint identifier | string | n/a | yes |
| engine\_name | The type of engine for the endpoint. Can be one of aurora | azuredb | docdb | dynamodb | mariadb | mongodb | mysql | oracle | postgres | redshift | s3 | sqlserver | sybase. | string | n/a | yes |
| extra\_connection\_attributes | Additional attributes associated with the connection | string | `""` | no |
| kms\_key\_arn | The Amazon Resource Name (ARN) for the KMS key that will be used to encrypt the connection parameters | string | `""` | no |
| password | The password to be used to login to the endpoint database. | string | n/a | yes |
| port | The database server port to connect to | string | n/a | yes |
| s3\_compression\_type | An optional parameter when set to GZIP uses GZIP to compress the target .csv or .parquet files | string | `"none"` | no |
| s3\_csv\_delimiter | The CSV field Delimeter | string | `","` | no |
| s3\_csv\_row\_delimeter | CSV row delimeter | string | `"\n"` | no |
| server\_name | The server name to connect to | string | n/a | yes |
| tags | Tags ... | map | `<map>` | no |
| username | The user name to be used to login to the endpoint database. | string | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| arn |  |

