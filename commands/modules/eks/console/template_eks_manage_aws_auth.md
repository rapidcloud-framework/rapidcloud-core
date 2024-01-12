### EKS AWS Auth Config Map

This section allows you to add users and roles to the EKS `aws-auth` config map.

Note:

- It is recommended to add roles and users AFTER you created at least one compute resource (Fargate or Managed Group)
- You should remove this configuration and `apply` before removing an EKS cluster.

---
## Inputs

**Cluster Name**
The name of the `EKS` cluster, your `profile` name will be prefixed to this value.

**Map Roles**
Provide a json list of maps containing roles you wish to add to the `aws-auth` map. 

Example: 

```
[
  {
    "rolearn": "arn:aws:iam::123456789:role/RoleOne",
    "username": "user.one",
    "groups": [
      "some:group",
      "some:another-group"
    ]
  },
  {
    "rolearn": "arn:aws:iam::123456789:role/RoleTwo",
    "username": "user.two",
    "groups": [
      "system:masters"
    ]
  },
  {
    "rolearn": "arn:aws:iam::123456789:role/user.three",
    "username": "user.three",
    "groups": [
      "system:masters"
    ]
  }
]

```

**Map Users**
Provide a json list of maps containing users you wish to add to the `aws-auth` map. 

Example:

```
[
  {
    "userarn": "arn:aws:iam::123456789:user/user.one",
    "username": "user.one",
    "groups": [
      "group:main",
      "group:misc",
      "group:others"
    ]
  },
  {
    "userarn": "arn:aws:iam::123456789:user/user.two",
    "username": "user.two",
    "groups": [
      "system:masters",
      "group:others"
    ]
  },
  {
    "userarn": "arn:aws:iam::123456789:user/user.three",
    "username": "user.three",
    "groups": [
      "system:masters"
    ]
  }
]
```


**Fargate Profile**
RapidCloud will auto populate this field when adding or removing a Fargate profile.


**Node Groups**
RapidCloud will auto populate this field when adding or removing a Managed node group.
