### App Service Environment

Manages an App Service Environment.

**Name**

(Required) The name of the App Service Environment. Changing this forces a new resource to be created.

**Resource Group Name**

(Required) The name of the Resource Group where the App Service Environment exists. Defaults to the Resource Group of the Subnet (specified by subnet_id).

**Subnet**

(Required) The ID of the Subnet which the App Service Environment should be connected to. Changing this forces a new resource to be created.

**Subnet**

(Required) Reference to a subnet in which this Bastion Host has been created. Changing this forces a new resource to be created.

**Load Balancing Mode**

(Optional) Specifies which endpoints to serve internally in the Virtual Network for the App Service Environment. Possible values are None, Web, Publishing, Defaults to None. Changing this forces a new resource to be created.

**Pricing Tier**

(Optional) Pricing tier for the front end instances. Possible values are I1, I2 and I3. Defaults to I1

**Allowed Ips**

(Optional) Allowed user added IP ranges on the ASE database. Use the addresses you want to set as the explicit egress address ranges.





