### OpenSearch Notes
Search and analytics suite used for a broad set of use cases like real-time application monitoring, log analytics, and website search.

**Name**
Equivalent to the OpenSearch Domain.

**Instance Type**
Sets the instance type for the nodes in the OpenSearch cluster.

**Available options:**
 - c5.large.search
 - c5.xlarge.search
 - c5.2xlarge.search
 - c5.4xlarge.search
 - c5.9xlarge.search
 - c5.18xlarge.search
 - c6g.large.search
 - c6g.xlarge.search
 - c6g.2xlarge.search
 - c6g.4xlarge.search
 - c6g.8xlarge.search
 - c6g.12xlarge.search
 - i3.large.search
 - i3.xlarge.search
 - i3.2xlarge.search
 - i3.4xlarge.search
 - i3.8xlarge.search
 - i3.16xlarge.search
 - m5.large.search
 - m5.xlarge.search
 - m5.2xlarge.searc
 - m5.4xlarge.search
 - m5.12xlarge.search
 - m6g.large.search
 - m6g.xlarge.search
 - m6g.2xlarge.search
 - m6g.4xlarge.search
 - m6g.8xlarge.search
 - m6g.12xlarge.search
 - r5.large.search
 - r5.xlarge.search
 - r5.2xlarge.search
 -  r5.4xlarge.search
 - r5.12xlarge.search
 - r5.large.search
 - r5.xlarge.search
 - r5.2xlarge.search
 - r5.4xlarge.search
 - r5.12xlarge.search
 - r6gd.large.search
 - r6gd.xlarge.search
 - r6gd.2xlarge.search
 - r6gd.4xlarge.search
 - r6gd.8xlarge.search
 - r6gd.12xlarge.search
 - r6gd.16xlarge.search

**Autotune**
Autotune in Amazon OpenSearch Service uses performance and usage metrics from your OpenSearch cluster to suggest memory-related configuration changes, including queue and cache sizes and Java virtual machine (JVM) settings on your nodes. These optional changes improve cluster speed and stability.

**High Availability**
Sets the availability zones to 3 - recommended for production workloads with higher availability requirements.

**Nodes**
Total number of nodes (if high-availability is disabled, must be a multiple of 2).

**EBS Storage Size**
Storage capacity (GiB) per node, minimum of 10 and maximum of 2048.

**Ultra Warm**
UltraWarm is a fully-managed, low-cost, warm storage tier for Amazon OpenSearch Service, enabling you to analyze data using the same tools that Amazon OpenSearch Service provides today. UltraWarm seamlessly integrates with Amazon OpenSearch Service’s existing features such as integrated alerting, SQL querying, and more. 

UltraWarm enables you to cost effectively expand the data you want to analyze on Amazon OpenSearch Service gaining valuable insights on data that previously may have been deleted or archived. With UltraWarm, you can now economically retain more of your data to interactively analyze it whenever you want.

**Dedicated Master Nodes**
Amazon OpenSearch Service uses dedicated master nodes to increase cluster stability. A dedicated master node performs cluster management tasks, but does not hold data or respond to data upload requests. This offloading of cluster management tasks increases the stability of your domain. Just like all other node types, you pay an hourly rate for each dedicated master node.

Dedicated master nodes perform the following cluster management tasks:
- Track all nodes in the cluster.
- Track the number of indexes in the cluster.
- Track the number of shards belonging to each index.
- Maintain routing information for nodes in the cluster.
- Update the cluster state after state changes, such as creating an index and adding or removing nodes in the cluster.
- Replicate changes to the cluster state across all nodes in the cluster.
- Monitor the health of all cluster nodes by sending heartbeat signals, periodic signals that monitor the availability of the data nodes in the cluster.