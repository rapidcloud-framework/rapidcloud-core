### SSO Permission Sets

Permission sets define the level of access that users and groups have to an AWS account.

**Name**

The name of your permission set.

**Description**

The description for your permission set.

**Relay State URL**

(Optional) The relay state URL used to redirect users within the application during the federation authentication process.

**Session Duration**

The length of time that the application user sessions are valid in the ISO-8601 standard. Default: PT1H.

**AWS Managed Policy ARNs**

Comma-separated list of policy ARNs to attach to the permission set.

**Custom Policy Text**

The IAM inline policy to attach to a permission set.