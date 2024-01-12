# Cloudtrail

AWS CloudTrail monitors and records account activity across your AWS infrastructure, giving you control over storage, analysis, and remediation actions.

## Trail Name

This is the trail name. Please look at the S3 Bucket Name and KMS Key ARN sections to see how the trail name should be used on the policies. 

## S3 Bucket Name

In order to create a new trail, you need to create a S3 bucket to store the logs, so on the S3 Bucket Name you will set the S3 bucket name that you created.
Furthermore, this S3 bucket should have a special bucket policy so Cloudtrail can be able to store logs there. Please see the example bellow to make sure you are using the right policy.

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AWSCloudTrailAclCheck20150319",
            "Effect": "Allow",
            "Principal": {
                "Service": "cloudtrail.amazonaws.com"
            },
            "Action": "s3:GetBucketAcl",
            "Resource": "arn:aws:s3:::<bucket-name>",
            "Condition": {
                "StringEquals": {
                    "AWS:SourceArn": "arn:aws:cloudtrail:<region>:<account-id>:trail/<trail-name>"
                }
            }
        },
        {
            "Sid": "AWSCloudTrailWrite20150319",
            "Effect": "Allow",
            "Principal": {
                "Service": "cloudtrail.amazonaws.com"
            },
            "Action": "s3:PutObject",
            "Resource": "arn:aws:s3:::<<bucket-name>>/AWSLogs/<account-id>/*",
            "Condition": {
                "StringEquals": {
                    "AWS:SourceArn": "arn:aws:cloudtrail:<region>:<account-id>:trail/<trail-name>",
                    "s3:x-amz-acl": "bucket-owner-full-control"
                }
            }
        },
        {
            "Sid": "AWSCloudTrailWrite20150319",
            "Effect": "Allow",
            "Principal": {
                "Service": "cloudtrail.amazonaws.com"
            },
            "Action": "s3:PutObject",
            "Resource": "arn:aws:s3:::<bucket-name>/AWSLogs/<organization-id>/*",
            "Condition": {
                "StringEquals": {
                    "AWS:SourceArn": "arn:aws:cloudtrail:<region>:<account-id>:trail/<trail-name>",
                    "s3:x-amz-acl": "bucket-owner-full-control"
                }
            }
        }
    ]
}
```

## KMS Key ARN

Cloudtrail also requires a KMS key to encrypt the logs, so you have to create a KMS key ahead and use special key policy. Please take a look at the example bellow to make sure you are using the right policy.

```
{
    "Version": "2012-10-17",
    "Id": "Key policy created by CloudTrail",
    "Statement": [
        {
            "Sid": "Enable IAM User Permissions",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::<account-id>:root"
            },
            "Action": "kms:*",
            "Resource": "*"
        },
        {
            "Sid": "Allow CloudTrail to encrypt logs",
            "Effect": "Allow",
            "Principal": {
                "Service": "cloudtrail.amazonaws.com"
            },
            "Action": [
                "kms:GenerateDataKey*",
                "kms:DescribeKey",
                "kms:Decrypt",
                "kms:ReEncryptFrom"
            ],
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "AWS:SourceArn": "arn:aws:cloudtrail:<region>:<account-id>:trail/<trail-name>"
                },
                "StringLike": {
                    "kms:EncryptionContext:aws:cloudtrail:arn": "arn:aws:cloudtrail:*:<account-id>:trail/*"
                }
            }
        }
    ]
}
```

## Include global service events?

Whether the trail is publishing events from global services such as IAM to the log files

## Enable log file validation?

Whether log file integrity validation is enabled

## Is this an organization trail?

Whether the trail is an AWS Organizations trail. Organization trails log events for the master account and all member accounts. Can only be created in the organization master account

## Is this a multiregion trail?

Whether the trail is created in the current region or in all regions