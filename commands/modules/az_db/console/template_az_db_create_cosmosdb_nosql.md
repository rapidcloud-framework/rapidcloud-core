### Cosmos DB NoSQL

Manages a CosmosDB (formally DocumentDB) Account.


**Name**

(Required) Specifies the name of the CosmosDB Account. Changing this forces a new resource to be created.

**Resource Group**

(Required) The name of the resource group in which the CosmosDB Account is created. Changing this forces a new resource to be created.

**Enable Serverless**

(Optional) The capability to enable Serverless

 **Enable Free Tier**

(Optional) Enable the Free Tier pricing option for this Cosmos DB account. Defaults to false. Changing this forces a new resource to be created.

 **Total throughput Limit**

(Required) The total throughput limit imposed on this Cosmos DB account (RU/s). Possible values are at least -1. -1 means no limit.

 **Geolocation**

(Required) Specifies a geo_location resource, used to define where data should be replicated with the failover_priority.

 **Enable Multiple write locations**

(Optional) Enable multiple write locations for this Cosmos DB account.

 **Allow IPs**

(Optional) CosmosDB Firewall Support: This value specifies the set of IP addresses or IP address ranges in CIDR form to be included as the allowed list of client IPs for a given database account. IP addresses/ranges must be comma separated and must not contain any spaces.

 **Subnet**

(Optional) used to define which subnets are allowed to access this CosmosDB account.

 **Encryption Key**

(Optional) A versionless Key Vault Key ID for CMK encryption. Changing this forces a new resource to be created.

 **Backup**

(Required) The type of the backup. Possible values are Continuous and Periodic. Migration of Periodic to Continuous is one-way, changing Continuous to Periodic forces a new resource to be created.

 **Interval in minutes**

(Optional) The interval in minutes between two backups. This is configurable only when type is Periodic. Possible values are between 60 and 1440.

 **Retention in hours**

(Optional) The time in hours that each backup is retained. This is configurable only when type is Periodic. Possible values are between 8 and 720.

 **Storage Redundancy**

(Optional) The storage redundancy is used to indicate the type of backup residency. This is configurable only when type is Periodic. Possible values are Geo, Local and Zone.




