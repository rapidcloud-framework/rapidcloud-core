# S3 Target Endpoint
This module creates an s3 target endpoint to store GLUE/DMS jobs output and an IAM role allow access to the bucket.

# Example Usage
```

module "s3_target_endpoint_1" {
  source                     = "../../dms/s3_target_endpoint"
  s3_bucker_arn              = "${module.bucket.role_arn}"
  s3_bucket_name             = "${module.bucket.bucket_name}"
  endpoint_id                = "${var.env}-s3-target-endpoint-1"
}

```

## Inputs

This module has the following avaialbe Inputs, Inputs without a `default` value are **mandatory** and must be set in the calling module ( see example above )

| Name | Description | Type | Default | Required |
|------|-------------|:----:|:-----:|:-----:|
| certificate\_arn | The Amazon Resource Name (ARN) for the certificate. | string | `""` | no |
| endpoint\_id | The database endpoint identifier | string | n/a | yes |
| extra\_connection\_attributes | Additional attributes associated with the connection | string | `""` | no |
| kms\_key\_arn | The Amazon Resource Name (ARN) for the KMS key that will be used to encrypt the connection parameters | string | `""` | no |
| s3\_bucket\_folder | Where the files are created in the s3 bucket | string | `""` | no |
| s3\_bucket\_name | The Bucket Name | string | `""` | no |
| s3\_bucket\_arn | The Bucket Arn | string | `""` | no |
| s3\_compression\_type | An optional parameter when set to GZIP uses GZIP to compress the target .csv or .parquet files | string | `"NONE"` | no |
| s3\_create\_iam\_role | Set this to 1 to create an IAM policy allowing access to the target s3 bucket | string | `"0"` | no |
| s3\_csv\_delimiter | The CSV field Delimeter | string | `","` | no |
| s3\_csv\_row\_delimeter | CSV row delimeter | string | `"\n"` | no |
| s3\_external\_table\_definition |  | string | `""` | no |
| s3\_service\_access\_role\_arn | The IAM role granting access to the s3 bucket | string | `""` | no |
| tags | Tags ... | map | `<map>` | no |

## Outputs

| Name | Description |
|------|-------------|
| arn |  |

