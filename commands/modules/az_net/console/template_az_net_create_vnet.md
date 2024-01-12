### Virtual Network


Manages a virtual network including any configured subnets. Each subnet can optionally be configured with a security group to be associated with the subnet.

**Name**

(Required) Specifies the name of the Virtual Network. Changing this forces a new resource to be created.

**Resource Group Name**

(Required) The name of the resource group in which to create the network security group. Changing this forces a new resource to be created.

**Location**

(Required) Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.

**Address Space**

(Required) The address space that is used the virtual network. You can supply more than one address space.

**DNS Servers**

(Optional) List of IP addresses of DNS servers