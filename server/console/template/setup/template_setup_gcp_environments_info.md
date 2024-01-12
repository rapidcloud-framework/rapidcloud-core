### Environments

An environment is a specific GCP workload or application, with its own business logic, security, data catalog, data lake, databases, compute services and other cloud resources.

You can create as many environments as you want, in any GCP Account, region and VPC.

Each environment is completely isolated and managed separately from other environments.

Environment name is comprised of  {`org`}\_{`workload`}\_{`environment`}. for example: `kinect_bitools_dev` or `abccorp_orders_test`

**Company or organization**

Enter your company or organization name without spaces or special characters.

**Workload/Application**

Workload Name without spaces or special characters. This should uniquely identify the type of workload or application you're creating this environment for.

**Environment**

This is a specific instance of the environment (e.g. dev|qa|uat|stg|prod)

**GCP Project Name**

GCP Project Name to create your environment in

**VPC**

GCP VPC ID where VPC specific resources will be created.

**Region**

GCP Region where region specific resources will be created.

**Are you using VPN to connect to your cloud account?**

We recommend always using VPN to connect to your cloud account.
