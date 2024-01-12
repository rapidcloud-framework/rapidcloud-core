### Azure Redis Cache

Create the `Azure Redis Cache`  
---
## Inputs

**Redis Cache Name**
*Required*
The name of the `Azure Redis Cache`.

**Resource Group Name**
*Required*
The name of the resource group.

**Location**
*Required*
The location where cache will be created.

**SKU**
*Required*
The SKU to use for the cache.
***Basic:*** Cache running on a single VM. No SLAs and is ideal for dev/test.
***Standard:*** Cache running on two VMs in a replicated configuration.
***Premium:*** High performance cache. This offers higher throughput, lower latency, better availability, etc.

**Storage Capacity**
*Required*
The size of the Redis Cache to deploy. Valid values for the Basic/Standard (C) SKU family are `0, 1, 2, 3, 4, 5, 6`, and for Premium (P) family are `1, 2, 3, 4, 5`

**Subnet**
*Required*
The subnet in which the Redis Cache should be deployed. Only available with `Premium` SKU

**Identity Type**
*Required*
The type of identity to use with the cache.

**Managed Identity**
*Required*
The user-assigned managed identities to use with the cache.

**Availability Zones**
*Required*
The availability zones in which the Redis Cache should be deployed.

**Tags**
*Required*
The tags to use for the cache.