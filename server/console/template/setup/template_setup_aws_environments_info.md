### Environments

An environment is a specific AWS workload or application, with its own business logic, security, data catalog, data lake, databases, compute services and other cloud resources.

You can create as many environments as you want, in any AWS Account, region and VPC.

Each environment is completely isolated and managed separately from other environments.

Environment name is comprised of  {`org`}\_{`workload`}\_{`environment`}. for example: `kinect_bitools_dev` or `abccorp_orders_test`

**Company or organization**

Enter your company or organization name without spaces or special characters.

**Workload/Application**

Workload Name without spaces or special characters. This should uniquely identify the type of workload or application you're creating this environment for.

**Environment**

This is a specific instance of the environment (e.g. dev|qa|uat|stg|prod)

**AWS Profile**

Select the name of AWS Profile that will allow RapidCloud access to your Environment's AWS account. AWS Profile must be previosely set up on the machine that hosts RapidCloud. 

RapidCloud will run `aws configure list-profiles` command to present available AWS Profiles. Please make sure AWS CLI is properly configured and use `aws configure` command to create your profile.

**Cross-Account Role ARN**

Specify Cross-Account Role ARN that will allow RapidCloud access to your Environment's AWS Account.

**VPC**

AWS VPC ID where VPC specific resources will be created.

**Region**

AWS Region where region specific resources will be created.

**SSH Public Key**

SSH Public Key will be used to access EMR clusters through SSH. This is only applicable for workloads that require EMR.

**Allowed IP Addresses**

Comma separated list of IP Addresses to be allowed SSH Access to EMR Cluster.

**Are you using VPN to connect to your cloud account?**

We recommend always using VPN to connect to your cloud account.
