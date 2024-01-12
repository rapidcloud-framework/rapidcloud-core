### ElastiCache - Memcached

Amazon ElastiCache is a web service that makes it easy to set up, manage, and scale a distributed in-memory data store or cache environment in the cloud. It provides a high-performance, scalable, and cost-effective caching solution while also removing the complexity associated with deploying and managing a distributed cache environment. Amazon ElastiCache works with both the Redis and Memcached engines.

**Name**

The Name of your cluster. ElastiCache converts this name to lowercase.

**Node Type**

(Required unless a replication group is selected)
The instance class for your cluster. See AWS documentation for information on [supported node types for Memcached](https://docs.aws.amazon.com/AmazonElastiCache/latest/mem-ug/CacheNodes.SupportedTypes.html) and [guidance on selecting node types for Memcached](https://docs.aws.amazon.com/AmazonElastiCache/latest/mem-ug/nodes-select-size.html).

**Number of Cache Nodes**
(Required unless a replication group is selected)
The initial number of cache nodes that the cache cluster will have. For Memcached, this value must be between 1 and 40.

**Parameter Group Name**
(Required unless a replication group is selected)
The name of the parameter group to associate with this cache cluster.

**Apply Immediately**
Whether any database modifications are applied immediately, or during the next maintenance window. AWS defaults to false.

**Availability Zones**
List of the Availability Zones in which cache nodes are created. If you are creating your cluster in an Amazon VPC you can only locate nodes in Availability Zones that are associated with the subnets you've selected. The number of Availability Zones listed must either equal the value of `num_cache_nodes` or equal 1 to apply the same zone to all nodes.

**Engine Version**
Version number of the cache engine to be used. If not set, defaults to the latest version. See documentation for supported versions [here](https://docs.aws.amazon.com/AmazonElastiCache/latest/mem-ug/supported-engine-versions-mc.html)

**Maintenance Window**
Specifies the weekly time range for when maintenance on the cache cluster is performed. The format is `ddd:hh24:mi-ddd:hh24:mi` (24H Clock UTC). The minimum maintenance window is a 60 minute period.

**Notification Topic ARN**
Optional ARN of an SNS topic to send ElastiCache notifications to.

**Security Groups**
One or more VPC security groups to associate with the cache cluster

**Subnets**
One or more VPC subnets to associate with the cache cluster
