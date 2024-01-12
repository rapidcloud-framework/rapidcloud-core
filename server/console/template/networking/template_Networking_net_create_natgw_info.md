# NAT Gateway
Creates a `NAT Gateway` in your environment.

Please note:

A `NAT Gateway` needs to be in a subnet that's internet enabled/has route to an `Internet Gateway`.
It is recomended to create a `NAT Gateway` per Availability Zone.

---
## Inputs

**Name**
The name of your `NAT Gateway`

**Subnet**
The rapidcloud fqn of the module used to create the `Subnet` you wish to create the `NAT Gateway` in.
This subnet needs to have an Internet route.

**Route Tables**
Select `route tables` to create a route to `0.0.0.0/0` via the `NAT Gateway` in the related `Subnet`.


---
## Outputs

**ID**
The ID of the `NAT Gateway`.

---
