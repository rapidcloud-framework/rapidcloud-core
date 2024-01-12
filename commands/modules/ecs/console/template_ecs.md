### Elastic Container Service

ECS is a fully managed container orchestration service that makes it easy for you to deploy, manage, and scale containerized applications

**Image URL**

The location of the image you're deploying

**Image Tag**

The tag of the image you're deploying, defaults to `latest`

**Enable Container Insights**

Container Insights collects metrics at the cluster, task and service levels. It also provides diagnostic information, such as container restart failures, to help you isolate issues and resolve them quickly.

**Task CPU Units**

The hard limit of CPU units to present for the task, view more information [here](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definition_parameters.html#task_size)

**Task Memory**

The hard limit of memory (in MiB) to present to the task, view more information [here](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definition_parameters.html#task_size)

**Container CPU Units**

The number of cpu units the Amazon ECS container agent reserves for the container, view more information [here](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definition_parameters.html#container_definition_environment)

**Container Memory**

The amount (in MiB) of memory to present to the container, view more information [here](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definition_parameters.html#standard_container_definition_params)

**Open Ports**

Specify which ports to make available in your ECS service

**Desired Count**

Number of task instances desired

**Task Role ARN**

ARN of IAM Role to attach to task. If left blank, RapidCloud will create an empty role

**Assign Public IP**

Whether to assign a public IP address to the ENI

**Subnet IDs**

Comma-separated list of subnets to associate

**Security Groups**

Comma-separated list of security groups to associate

**Environment Variables**

Comma-separated list of key/value pairs. E.g. env=dev, name=my-ecs-service