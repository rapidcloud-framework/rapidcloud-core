# Internet Gateway
Creates a `Internet Gateway` in your environment.
Normally this will be used in `public` subnets, use the `route tables` drop down to select which route tables to create an internet route in.

---
## Inputs

**Name**
The name of your `Internet Gateway`

**VPC**
The VPC you wish to create the `Internet Gateway` in.

**Route Tables**
Select `route tables` to create a route to `0.0.0.0/0` via the `Internet Gateway`

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
The ID of the `Internet Gateway`.

---
