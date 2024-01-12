# Endpoints
Creates a `VPC Endpoint` in your environment.

This module supports the following end points:
- autoscaling 
- dynamodb
- ec2
- ecr-api
- ecr-dkr
- s3
- sns
- sqs

Please note:

Both `dynamodb` and `s3` create a `Route Table Association`, All others are `Interface` type and a `Security Group` will be attached to them allowing access from the `VPC CIDR`.

---
## Inputs

**Name**
The name of your `Endpoint`.

**Service**
The `Endpoint Service`.

**VPC ID**
The `VPC` ID in which to create this endpoint.

**Route Tables**
The `Route Tables` to associate with the `Endpoint Service`, only applies to `dynamodb` and `s3`.


---
## Outputs


---

