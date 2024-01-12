
A terraform module that creates the s3 bucket consumed by DMS/GLUE
This module will create the following resources:

- IAM role
- S3 bucket

### TODO:  add kms key

## Example Usage

```

module "bucket" {
  source      = "../../dms/s3"
  bucket_name = "dms-bucket-storage"
}

output "dms_s3_bucket_arn" {
  value = "${module.bucket.bucket_arn}"
}

output "dms_s3_bucket_role" {
  value = "${module.bucket.role_arn}"
}

## Inputs
| Name | Description | Type | Default | Required |
|------|-------------|:----:|:-----:|:-----:|
| block\_public\_acls |  | string | `"true"` | no |
| block\_public\_policy |  | string | `"true"` | no |
| bucket\_name | The name of the s3 bucket to create | string | n/a | yes |
| enable\_bucket\_policy | Enable bucket policy | string | `"1"` | no |
| ignore\_public\_acls |  | string | `"true"` | no |
| kms\_key\_arn | ARN of the kms key used to encrypt the bucket | string | n/a | yes |
| restrict\_public\_buckets |  | string | `"true"` | no |
| tags | Map of tags to assign to this bucket | map | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| bucket\_arn |  |
| bucket\_name |  |
| role\_arn |  |

