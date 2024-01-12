### This file is optional

Install `EKS Addons` provided and managed by AWS.

---
## Inputs 

**Cluster Name**
The name of the `EKS` cluster the addons should be installed to. 

**Compute Type**
`Fargate`: only supports `CORE DNS`, requires a fargate profile with an available namespace.
`EC2`: supports all addons, requires at least 2 managed nodes.

**Subnets**
When installing to `Fargate` a profile will be created using at least two subnets, select the subnets you wish to deploy the `CORE DNS` `Fargate` profile to.

**CORE DNS**
```
A flexible, extensible DNS server that can serve as the Kubernetes cluster DNS. The self-managed or managed type of this add-on was installed, by default, when you created your cluster. When you launch an Amazon EKS cluster with at least one node, two replicas of the CoreDNS image are deployed by default, regardless of the number of nodes deployed in your cluster. The CoreDNS pods provide name resolution for all pods in the cluster. You can deploy the CoreDNS pods to Fargate nodes if your cluster includes an AWS Fargate profile with a namespace that matches the namespace for the CoreDNS deployment.
```

`Enable`: toggle on/off to install the addon.
`Version`: select the version for your cluster.
`Pod Count`: by default, AWS will launch two `CORE DNS` pods, this field allows you to add pods to your replica set.

**Kube Proxy**
```
Maintains network rules on each Amazon EC2 node. It enables network communication to your pods. The self-managed or managed type of this add-on is installed on each Amazon EC2 node in your cluster, by default.
```

`Enable`: toggle on/off to install the addon.
`Version`: select the version for your cluster.

**VPC CNI**
```
provides native VPC networking for your cluster. The self-managed or managed type of this add-on is installed on each Amazon EC2 node, by default.
```

`Enable`: toggle on/off to install the addon.
`Version`: select the version for your cluster.

**EBS CSI**
```
A Kubernetes Container Storage Interface (CSI) plugin that provides Amazon EBS storage for your cluster.
```

`Enable`: toggle on/off to install the addon.
`Version`: select the version for your cluster.
