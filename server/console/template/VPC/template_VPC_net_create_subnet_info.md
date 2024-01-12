# SUBNETS
This section allows you to create a `subnet` in a VPC, by default a `route table` will be created and associate it with the `subnet` you are creating.

You may use an existing `route table` (created by `rapidcloud subnet` module) by selecting it from the drop down menu.

Generaly a `shared route table` is useful in `public` subnets since internet gateways are per region. 

## Inputs

**Name**
The name of your `subnet` and `route table` (if creating both).

**VPC**
The VPC you wish to create the `subnet` in.

**CIDR**
The IPv4 CIDR block for the `subnet`.

**Availability Zones**
The availability zone to create the `subnet` in"

**Use Existing Route Table**
Select an existing `route table` to associate this `subnet` with.

**Create Route Table**
Toggle On to create a `route table` and associate it with the `subnet`.

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
The ID of the `Subnet`.

**Route Table ID**
The ID of the `route table` (if created).

---
