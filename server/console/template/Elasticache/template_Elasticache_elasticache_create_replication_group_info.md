### Redis Replication Groups

Amazon ElastiCache is a web service that makes it easy to set up, manage, and scale a distributed in-memory data store or cache environment in the cloud. It provides a high-performance, scalable, and cost-effective caching solution while also removing the complexity associated with deploying and managing a distributed cache environment. Amazon ElastiCache works with both the Redis and Memcached engines.

**Name**
The Name of your cluster. ElastiCache converts this name to lowercase.

**Description**
Description for your replication group.

**Node Type**

(Required unless a replication group is selected)
The instance class for your cluster. See AWS documentation for information on [supported node types for Redis](https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/CacheNodes.SupportedTypes.html) and [guidance on selecting node types for Redis](https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/nodes-select-size.html).

**Parameter Group Name**
(Required unless a replication group is selected)
The name of the parameter group to associate with this cache cluster.

**Apply Immediately**
Whether any database modifications are applied immediately, or during the next maintenance window. AWS defaults to false.

**Engine Version**
Version number of the cache engine to be used. If not set, defaults to the latest version. See documentation for supported versions [here](https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/supported-engine-versions-mc.html)

**KMS Key**
The name of the key that you wish to use if encrypting at rest. If not supplied, uses service managed encryption. Can be specified only if at-rest encryption is enabled.

**At-Rest Encryption**
Whether to enable encryption at rest.

**In-Transit Encryption**
Whether to enable encryption in transit.

**Automatic Failover**
Specifies whether a read-only replica will be automatically promoted to read/write primary if the existing primary fails. If enabled, `num_cache_clusters` must be greater than 1. Must be enabled for Redis (cluster mode enabled) replication groups. Defaults to false.

**Multi-AZ**
Specifies whether to enable Multi-AZ Support for the replication group. If true, automatic failover must also be enabled. Defaults to false.

**User Group Name**
User Group to associate with the replication group. AWS allows a maximum of 1 user group to be associated.

**Number of Cache Clusters (Redis Cluster Mode Disabled)**
Number of cache clusters (primary and replicas) this replication group will have. If Multi-AZ is enabled, the value of this parameter must be at least 2. Conflicts with node groups/replicas per node settings.

**Number of Node Groups (Redis Cluster Mode Enabled)**
Number of node groups (shards) for this Redis replication group. Changing this number will trigger a resizing operation before other settings modifications.

**Replicas Per Node Group (Redis Cluster Mode Enabled)**
Number of replica nodes in each node group. Changing this number will trigger a resizing operation before other settings modifications. Valid values are 0 to 5.

**Final Snapshot Identifier**
Name of your final cluster snapshot. If omitted, no final snapshot will be made.

**Maintenance Window**
Specifies the weekly time range for when maintenance on the cache cluster is performed. The format is `ddd:hh24:mi-ddd:hh24:mi` (24H Clock UTC). The minimum maintenance window is a 60 minute period.

**Notification Topic ARN**
Optional ARN of an SNS topic to send ElastiCache notifications to.

**Log Destination**
Name of either the CloudWatch Logs LogGroup or Kinesis Data Firehose resource.

**Log Destination Type**
For CloudWatch Logs use `cloudwatch-logs` or for Kinesis Data Firehose use `kinesis-firehose`.

**Log Format**
Valid values are `json` or `text`

**Log Format**
Valid values are `slow-log` or `engine-log`

**Security Groups**
One or more VPC security groups to associate with the cache cluster

**Subnets**
One or more VPC subnets to associate with the cache cluster
