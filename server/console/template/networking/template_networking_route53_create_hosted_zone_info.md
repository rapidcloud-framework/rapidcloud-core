### AWS Route 53 Hosted zone

A hosted zone is a container for records, and records contain information about how you want to route traffic for a specific domain, such as test.io, and its subdomains (dev.test.io, qa.test.io). A hosted zone and the corresponding domain have the same name. 

**Hosted zone domain**
A domain to associate to your zone

**Zone comment**
A comment to help you identify the zones purpose.

**Hosted zone type**
A **private** hosted zone is a container that holds information about how you want Amazon Route 53 to respond to DNS queries for a domain and its subdomains within one or more VPCs that you create with the Amazon VPC service. More details [here](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/hosted-zones-private.html).

A **public** hosted zone is a container that holds information about how you want to route traffic on the internet for a specific domain. More details [here](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/AboutHZWorkingWith.html).

**Add delegation set**
Explicitly add a reusable delegation set to this zone.

**Delegation set id**
Add the id of an existing delegation set id

**VPC Id**
To make a zone **private** you need to associate it with a VPC

**Force destroy records**
Whether to destroy all records (possibly managed outside of Terraform) in the zone when destroying the zone.
