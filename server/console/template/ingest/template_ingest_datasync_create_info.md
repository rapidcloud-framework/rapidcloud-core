### Datasync service

Datasync is a service that will help you transfering data from one location to another.

At the moment this service will provide you with a datasync agent, vpc endpoint to access datasync service, nfs location (source) and s3 location (destination).

Prerequites:
Datasync service running in some sort of compute. We recommend you setup your service as close to the source data as possible. See more on how to setup your service [here](https://docs.aws.amazon.com/datasync/latest/userguide/deploy-agents.html).

**Rapid cloud resource name**
Name for the RC resource that will identify this within the RC console.

**Agent name**
User friendly name to assign to the Datasync agent.

**IP address of the agent**
DataSync Agent IP address to retrieve activation key during resource creation. DataSync Agent must be accessible on port 80 from where Rapidcloud is running.

**Source NFS server hostname**
pecifies the IP address or DNS name of the NFS server. The DataSync Agent(s) use this to mount the NFS server.

**NFS subdirectory**
Subdirectory to perform actions as source or destination. Should be exported by the NFS server.

**Destination s3 bucket name**
S3 Bucket name to pick as destination.

**VPC Id**
The ID of the VPC in which the endpoint will be used.

**Security groups for the vpc endpoint**
The ID of one or more security groups to associate with the network interface.

**Security groups for the Datasync agent**
The Ids of the security groups used to protect your data transfer task subnets.

**Subnet ids for the Datasync agent**
The Ids of the subnets in which DataSync will create elastic network interfaces for each data transfer task.
