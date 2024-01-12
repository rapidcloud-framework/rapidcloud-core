### EKS Cluster

Create the `EKS` cluster control plane
---
## Inputs

**Cluster Name**
The name of the `EKS` cluster, your `profile` name will be prefixed to this value.

**EKS Version**
The `EKS` Cluster versions, a list of supported versions can be found <a href="https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions.html" target="_blank">here</a>

**Subnets**
Specify two subnets to place the `EKS` cluster API nodes in, it is recommended to use private `VPC` subnets to host your control plane. 

**Public API Access**
Toggle this to allow access to your `EKS` control plan from the internet.

**Public Api Access CIDRs** 
If you chose to allow internet access, you will need to provide a comma separated list of CIDRs to allow access, for example `10.0.0.1/32` 

**Log Types**
The `EKS` control plane logging provides audit and diagnostic logs directly from the Amazon EKS control plane to Cloudwatch Logs in your account.

```
API server (api) – Your cluster's API server is the control plane component that exposes the Kubernetes API. If you enable API server logs when you launch the cluster, or shortly thereafter, the logs include API server flags that were used to start the API server. For more information, see kube-apiserver and the audit policy in the Kubernetes documentation.

Audit (audit) – Kubernetes audit logs provide a record of the individual users, administrators, or system components that have affected your cluster. For more information, see Auditing in the Kubernetes documentation.

Authenticator (authenticator) – Authenticator logs are unique to Amazon EKS. These logs represent the control plane component that Amazon EKS uses for Kubernetes Role Based Access Control (RBAC) authentication using IAM credentials. For more information, see Cluster management.

Controller manager (controllerManager) – The controller manager manages the core control loops that are shipped with Kubernetes. For more information, see kube-controller-manager in the Kubernetes documentation.

Scheduler (scheduler) – The scheduler component manages when and where to run pods in your cluster. For more information, see kube-scheduler in the Kubernetes documentation.
```

Select the log groups you wish to export.

**Log Retention**
How long should the above logs be retained in Cloudwatch

**Tags**
Tags for your `EKS` cluster 
