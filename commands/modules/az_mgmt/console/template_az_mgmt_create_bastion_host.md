
### Azure Bastion Host

Manages a network security group that contains a list of network security rules. Network security groups enable inbound or outbound traffic to be enabled or denied.

**Name**

(Required) Specifies the name of the network security group. Changing this forces a new resource to be created.

**Resource Group Name**

(Required) The name of the resource group in which to create the network security group. Changing this forces a new resource to be created.

**Location**

(Required) Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.

**Subnet**

(Required) Reference to a subnet in which this Bastion Host has been created. Changing this forces a new resource to be created.

**Public IP Address**

(Required) Reference to a Public IP Address to associate with this Bastion Host. Changing this forces a new resource to be created.

**Copy Paste Enabled**

(Optional) Is Copy/Paste feature enabled for the Bastion Host. Defaults to true.

**File Copy Enabled**

(Optional) Is File Copy feature enabled for the Bastion Host. Defaults to false.



