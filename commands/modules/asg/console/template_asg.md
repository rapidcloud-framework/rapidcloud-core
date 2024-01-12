### AutoScaling Groups

An Auto Scaling group is a logical grouping of EC2 instances that manages automatic scaling

**Launch Template Name**

A Launch Template specifies the necessary information to configure the EC2 instances in the ASG

**Launch Template Version**

The version of the launch template to use, defaults to $Latest

**Instance Type**

The instance type to use for your instance, defaults to `t2.micro`.
View available instance types [here](https://aws.amazon.com/ec2/instance-types)

**AMI ID**

The Amazon Machine Image to use for the EC2 instances in the ASG

**Placement Group Name**

The name of the placement group into which you'll launch your instances

**Placement Group Strategy**

The placement strategy, allowed values are (cluster | partition | spread).
Find more information [here](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/placement-groups.html)

**Subnets**

A comma-separated list of subnet IDs to attach to the LB

**Desired Capacity**

The number of Amazon EC2 instances that should be running in the ASG

**Min Size**

The minimum size of the Auto Scaling Group

**Max Size**

The maximum size of the Auto Scaling Group