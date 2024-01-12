### Azure Storage Account

Create the `Azure Storage Account`  
---
## Inputs

**Storage Account Name**
*Required*
The name of the `Azure Storage Account`.

**Resource Group Name**
*Required*
The name of the resource group.

**Location**
*Required*
The location where cache will be created.

**Access Tier**
*Required*
The access type for this storage account.
***Standard:*** Recommended for most scenarios. General-purpose v2 account.
***Premium:*** Recommended for scenarios that require low latency.

**Replication Type**
*Required*
The type of replication to use for this storage account.

**IP Addresses**
*Required*
Comma-separated list of Public IP addresses to allow access to the storage account. Must in valid CIDR range. /31 and /32 are not allowed

**Subnets**
*Required*
The subnets to allow access to the storage account.

**Tags**
*Required*
The tags to use for the cache.