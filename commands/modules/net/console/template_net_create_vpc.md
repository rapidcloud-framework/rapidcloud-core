# VPC
Creates a `VPC` in your environment

---
## Inputs

**Name**
The name of your `VPC`

**CIDR**
The IPv4 CIDR block for the `VPC`.

**Enable DNS Hostnames**
Enable/disable [DNS hostnames](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-dns.html#vpc-dns-hostnames) in the `VPC`. Defaults to true.


**Enable DNS Support**
Enable/disable [DNS support](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-dns.html#AmazonDNS) in the `VPC`. Defaults to true.

**Tags**
Provide additional tags, by default Rapid Cloud will add the following tags to all possible resources:

```
 Name    
 env      
 profile  
 author 
 fqn      
 cmd_id 
 workload 
```
---
## Outputs

**ID**
The ID of the `VPC`.

---
