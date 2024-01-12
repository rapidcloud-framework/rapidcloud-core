### LB Target Groups

**Name**

Name of the target group

**Port**

Port on which targets receive traffic

**Protocol**

Protocol to use for routing traffic to the targets

**Target Type**

Target Type for the group (instance|ip)

**VPC ID**

Identifier of the VPC in which to create the target group

**Load Balancer Type**

Load Balancer Type to be used with target group (ALB|NLB)

**Load Balancing Algorithm Type**

Valid only for ALB (round_robin|least_outstanding_requests)

**Preserve Client IP**

Whether client IP preservation is enabled, valid only for NLB. See more information [here](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/load-balancer-target-groups.html#client-ip-preservation)

**IP Address Type**

Valid only for IP target type (IPV4|IPV6)

**Protocol Version**

Valid only when protocol is HTTP/HTTPS (gRPC|HTTP1|HTTP2)

**IP Targets**

Comma-separated list of IPs

**EC2 Targets**

EC2 instances to attach to the target group