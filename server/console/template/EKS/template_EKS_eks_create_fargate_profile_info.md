### This file is optional

Create a `Fargate` Profile 

---
## Inputs

**Profile Name**
The name of the `Fargate` profile, your `rapidcloud` profile will be prefixed to it.

**Cluster Name**
The name of the `EKS` cluster to attach this `Fargate` profile to.

**Namespaces**
`Fargate` Allows for up to five namespaces per profile, you may specificy the following for each namespace:

`Namespace (1-5)`: the name of the namespace to create.
`Namespace (1-5) Labels`: map of Kubernetes labels for selection of where to place pods. 

If you plan on using `CORE DNS` which may be deployed using the `Addons` section, remember to use only four of the possible five namespaces, since the addon would need its own `Fargate` compute resources and namespace.

**Tags**
Tags to apply to the `Fargate` profile.
