### Node Groups

Create and attach an `EKS Managed Node Group` to an `EKS` cluster.
<a href="https://docs.aws.amazon.com/eks/latest/userguide/managed-node-groups.html)" target="_blank">EKS Managed Node Group</a>


---
## Inputs
**Node Group Name**

The name of your `Node Group`, your profile name will be prefixed to it.

**Cluster Name**
Select the `EKS` Cluster you wish to attach this `Node Group` to.

**Subnets**
Select at least two subnets to place your EKS nodes in.

**Instance Types**
Comma separated list of instance types for your node group, you should pick different families with similar CPU/RAM sizes for better availability

**Node Group Sizing**
`Desired Size`: the amount of initial nodes provisioned in this `Node Group`
`Max Size`: the maximum amount of initial nodes provisioned in this `Node Group`
`Min Size`: the minimum amount of initial nodes provisioned in this `Node Group`

**Capacity Type**
`SPOT`: use spot instances for this `Node Group`
`ON DEMAND`: use on demand instances for this `Node Group`

**Volume Size**
The size of the `EBS` volume attached to each node in this `Node Group` 

**Volume Type**
The type of the `EBS` volume attached to each node in this `Node Group` 

**Force Node Version Update**
Force version update if existing pods are unable to be drained due to a pod disruption budget issue, as described <a href="https://docs.aws.amazon.com/eks/latest/userguide/managed-node-update-behavior.html" target="_blank">here</a>

**Labels**
`EKS` labels for each node in this `Node Group`

**Tags**
`AWS` tags for each node in this `Node Group`

