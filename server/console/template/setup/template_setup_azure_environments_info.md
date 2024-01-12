### Environments

An environment is a specific Azure workload or application, with its own business logic, security, data catalog, data lake, databases, compute services and other cloud resources.

You can create as many environments as you want, in any Azure Account, region and VNet.

Each environment is completely isolated and managed separately from other environments.

Environment name is comprised of  {`org`}\_{`workload`}\_{`environment`}. for example: `kinect_bitools_dev` or `abccorp_orders_test`

**Company or organization**

Enter your company or organization name without spaces or special characters.

**Workload/Application**

Workload Name without spaces or special characters. This should uniquely identify the type of workload or application you're creating this environment for.

**Environment**

This is a specific instance of the environment (e.g. dev|qa|uat|stg|prod)

**Azure Subscription**

Select the name of Azure Subscription that will allow RapidCloud access to your Environment's Azure account. Azure Subscription must be previosely set up on the machine that hosts RapidCloud.

RapidCloud will run `az account list` command to present available Azure Subscriptions. Please make sure Azure CLI is properly configured and use `az login` command to login to your Azure Account.

**VNet**

Azure VNet ID where VNet specific resources will be created.

**Region**

Azure Region where region specific resources will be created.

**Are you using VPN to connect to your cloud account?**

We recommend always using VPN to connect to your cloud account.
