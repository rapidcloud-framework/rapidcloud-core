### Azure Function App

Manages a Linux/Windows Function App.

**Name**

(Required) The name which should be used for this Linux/Windows Function App. Changing this forces a new Linux/Windows Function App to be created. Limit the function name to 32 characters to avoid naming collisions. For more information about Function App naming rule and Host ID Collisions

**Resource Group Name**

(Required) The name of the Resource Group where the Function App should exist. Changing this forces a new Function App to be created.

**Location**

(Required) The Azure Region where the Function App should exist. Changing this forces a new Function App to be created.(Required) The Azure Region where the Function App should exist. Changing this forces a new Function App to be created.

**Operative System**

(Required) Linux or Windows.

**Service Plan**

(Required) The name of the App Service Plan within which to create this Function App.

**Stack Version (Runtime)**

(Optional) The runtime version associated with the Function App. Defaults to ~4.

**Storage Account**

(Optional) The backend storage account name which will be used by this Function App

**Storage Account Access Type**

(Optional) Access Key or Managed Identity Access Type. 

**Managed Identity**

A list of User Managed identities to assign

**Enable Public Access**

(Optional) Should public network access be enabled for the Function App. Defaults to true.

**HTTPS Only**

(Optional) Can the Function App only be accessed via HTTPS? Defaults to false.

**Subnet**

(Optional) The subnet id which will be used by this Function App for regional virtual network integration.








