
### Subnet


Manages a subnet. Subnets represent network segments within the IP space defined by the virtual network.

**Name**

(Required) Specifies the name of the Virtual Network. Changing this forces a new resource to be created.

**Resource Group Name**

(Required) The name of the resource group in which to create the subnet. Changing this forces a new resource to be created.

**Address Space**

(Required) The address prefixes to use for the subnet.

**Virtual Network Name**

(Required) The name of the virtual network to which to attach the subnet. Changing this forces a new resource to be created.

**Service Endpoints**

(Optional) The list of Service endpoints to associate with the subnet. Possible values include: Microsoft.AzureActiveDirectory, Microsoft.AzureCosmosDB, Microsoft.ContainerRegistry, Microsoft.EventHub, Microsoft.KeyVault, Microsoft.ServiceBus, Microsoft.Sql, Microsoft.Storage, Microsoft.Storage.Global and Microsoft.Web.