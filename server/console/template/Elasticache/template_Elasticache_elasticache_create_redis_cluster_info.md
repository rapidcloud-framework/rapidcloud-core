### ElastiCache - Redis

Amazon ElastiCache is a web service that makes it easy to set up, manage, and scale a distributed in-memory data store or cache environment in the cloud. It provides a high-performance, scalable, and cost-effective caching solution while also removing the complexity associated with deploying and managing a distributed cache environment. Amazon ElastiCache works with both the Redis and Memcached engines.

**Name**

The Name of your cluster. ElastiCache converts this name to lowercase.

**Node Type**

(Required unless a replication group is selected)
The instance class for your cluster. See AWS documentation for information on [supported node types for Redis](https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/CacheNodes.SupportedTypes.html) and [guidance on selecting node types for Redis](https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/nodes-select-size.html).

**Parameter Group Name**
(Required unless a replication group is selected)
The name of the parameter group to associate with this cache cluster.

**Apply Immediately**
Whether any database modifications are applied immediately, or during the next maintenance window. AWS defaults to false.

**Availability Zone**
Availability Zone for the cache cluster.

**Engine Version**
Version number of the cache engine to be used. If not set, defaults to the latest version. See documentation for supported versions [here](https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/supported-engine-versions-mc.html)

**Final Snapshot Identifier**
Name of your final cluster snapshot. If omitted, no final snapshot will be made.

**Maintenance Window**
Specifies the weekly time range for when maintenance on the cache cluster is performed. The format is `ddd:hh24:mi-ddd:hh24:mi` (24H Clock UTC). The minimum maintenance window is a 60 minute period.

**Notification Topic ARN**
Optional ARN of an SNS topic to send ElastiCache notifications to.

**Replication Group**
Name of the replication group to which this cluster should belong. If this parameter is specified, the cluster is added to the specified replication group as a read replica; otherwise, the cluster is a standalone primary that is not part of any replication group.

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
