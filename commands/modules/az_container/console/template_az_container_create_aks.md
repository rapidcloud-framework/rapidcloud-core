### AKS Cluster

Create the `Azure AKS` cluster 
---
## Inputs

**Cluster Name**
*Required*
The name of the `AKS` cluster.

**Resource Group Name**
*Required*
The name of the resource group.

**Location**
*Required*
The location where the cluster should be created.

**AKS Version**
*Required*
The `AKS` Cluster version

**Auto Upgrade**
*Required*
Setting this value to true will update the Kubernetes cluster (and its node pools) to the latest GA version automatically.

**Enable Private Cluster**
*Required*
Setting this value to true will have the Kubernetes Cluster to have its API server only exposed on internal IP addresses.

**Enable VNET Integration**
*Required*
Setting this value to true will have the Kubernetes Cluster project the API server endpoint directly into a delegated subnet in the VNet where AKS is deployed. API Server VNet Integration enables network communication between the API server and the cluster nodes without requiring a private link or tunnel.

**API Server Subnet**
*Required when VNET Integration is enabled*
The API Server Subnet. Must be at least /28 and cannot be used for any other workloads, but you can use it for multiple AKS clusters located in the same virtual network.

**Authorized IP Ranges**
*Required when Private Cluster is disabled*
Set of authorized IP ranges to allow access to API server.

**Desired Size**
*Required*
The desired number of nodes in the cluster.

**Max Size**
*Required*
The maximum number of nodes in the cluster.

**Min Size**
*Required*
The minimum number of nodes in the cluster.

**VM Instance Type**
*Required*
The instance type for nodes in the cluster.

**Node Pool Zones**
*Required*
List of Availability Zones in which this Kubernetes Cluster should be located.

**Enable Azure CNI**
*Required*
Setting this value to true enables Azure CNI on the cluster

**Subnet**
*Required when Azure CNI is enabled*
Subnet where Kubernetes Node Pool should exist

**Service CIDR**
*Required when Azure CNI is enabled*
The Network Range used by the Kubernetes service

**DNS Service IP**
*Required when Azure CNI is enabled*
IP address within the Kubernetes service address range that will be used by cluster service discovery (kube-dns)

**Network Policy**
*Required*
The Network Policy to be used with the cluster. `azure` is only allowed when Azure CNI is enabled.

**Pod CIDR**
*Optional*
The CIDR to use for pod IP addresses. Allowed only when Azure CNI is disabled.

**Enable Azure AD Integration**
*Required*
Enable Azure AD Integration on the cluster

**Enable Azure RBAC**
*Required*
Enable Azure RBAC for authorization

**Admin Groups**
*Required when Azure RBAC is enabled*
List of Azure Active Directory Groups which should have Admin Role on the Cluster

**Enable Blob Driver**
*Required*
Enable Azure Blob CSI driver on the cluster

**Enable File Driver**
*Required*
Enable Azure File CSI driver on the cluster

**Enable Disk Driver**
*Required*
Enable Azure Disk CSI driver on the cluster

**Log Analytics Workspace**
*Required*
The Log Analytics Workspace to use for the cluster.







