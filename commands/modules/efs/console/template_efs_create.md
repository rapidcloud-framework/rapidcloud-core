### Amazon Elastic File System

Amazon Elastic File System is a cloud storage service that provides scalable, elastic, and encrypted file storage.
This module will create the following: 
- EFS File System 
- Security Group Allowing EFS access from a selected VPC CIDR
- Mount Target in VPC Subnets, you should select at least 2 subnets and preferably private ones.


---

**File System Name**

The name of the file system, used by RapidCloud to identify the resource.

**Encrypted**

If true, the disk will be encrypted

**Performance Mode**

The file system performance mode. Valid values: 
 - generalPurpose (Default)
 - maxIO

**Throughput Mode**

The file system throughput mode. Valid values: 
 - bursting (Default)
 - provisioned
 - elastic

**Provisioned Throughput In MiB/s**

With Throughput mode `provisioned` set the throughput, measured in MiB/s, that you want to provision for the file system.

**Transition to IA Storage**

Set a policy to transition a file to IA storage", Valid Values:
- AFTER_1_DAY
- AFTER_7_DAYS
- AFTER_14_DAYS
- AFTER_30_DAYS
- AFTER_60_DAYS
- AFTER_90_DAYS


**Transition files from IA**

Set a policy to transition a file from IA storage to primary storage, Valid Values:
- AFTER_1_ACCESS

**VPC ID**

This module will create a security group allowing the VPC your select CIDR access to the EFS mount target.

**Subnet IDs**

The ID of the subnets to add the EFS mount target in, it is recommended to use at least two subnets in different availability zones.
