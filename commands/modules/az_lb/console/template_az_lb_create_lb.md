### Load Balancer

Manages a Load Balancer Resource.


**Name**

(Required) Specifies the name of the Load Balancer. Changing this forces a new resource to be created.

**Resource Group Name**

(Required) The name of the Resource Group in which to create the Load Balancer. Changing this forces a new resource to be created.

**Location**

(Required) Specifies the supported Azure Region where the Load Balancer should be created. Changing this forces a new resource to be created.


**Public IP**

(Required) Specifies the Public IP address attached to the LB.

**Sku**

(Optional) The SKU of the Azure Load Balancer. Accepted values are Basic, Standard and Gateway. Defaults to Basic. Changing this forces a new resource to be created.

**Sku tier**

(Optional) The SKU tier of this Load Balancer. Possible values are Global and Regional. Defaults to Regional. Changing this forces a new resource to be created.


