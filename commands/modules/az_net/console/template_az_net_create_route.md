### Route

Manages a Route within a Route Table.

**Name**

 (Required) The name of the route. Changing this forces a new resource to be created.

**Resource Group**

(Required) The name of the resource group in which to create the route. Changing this forces a new resource to be created.

**Route Table Name**

(Required) The name of the route table within which create the route. Changing this forces a new resource to be created.

**Address Prefix**

(Required) The destination to which the route applies. Can be CIDR (such as 10.1.0.0/16) or Azure Service Tag (such as ApiManagement, AzureBackup or AzureMonitor) format.

**Next Hop Type**

(Required) The type of Azure hop the packet should be sent to. Possible values are VirtualNetworkGateway, VnetLocal, Internet, VirtualAppliance and None.
