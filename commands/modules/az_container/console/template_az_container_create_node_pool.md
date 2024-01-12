
### AKS Node Pool

Create the `AKS` node pool 
---
## Inputs

**Node Pool Name**
*Required*
The name of the `AKS` node pool.

**AKS Version**
*Required*
The `AKS` Cluster version used for the agent

**Desired Size**
*Required*
The desired number of nodes in the node pool.

**Max Size**
*Required*
The maximum number of nodes in the node pool.

**Min Size**
*Required*
The minimum number of nodes in the node pool.

**VM Instance Type**
*Required*
The instance type for nodes in the node pool.

**OS SKU**
*Required*
The OS SKU for nodes in the node pool.

**Operating System**
*Required*
The Operating System used by the nodes in the node pool.

**Node Pool Mode**
*Required*
The mode of the node pool.

**Use Spot Instances**
*Required*
Enable spot instances for the nodes in the pool.

**Eviction Policy**
*Required*
The Eviction Policy which should be used for Virtual Machines within the Virtual Machine Scale Set powering this Node Pool.

**Node Pool Zones**
*Required*
List of Availability Zones in which this Kubernetes Cluster should be located.

**Node Pool Subnet**
*Required*
The Subnet where this Node Pool should exist.

**Node Labels**
*Optional*
A map of Kubernetes labels which should be applied to nodes in this Node Pool.

**Node Taints**
*Optional*
A list of Kubernetes taints which should be applied to nodes in the agent pool (e.g key=value:NoSchedule).


