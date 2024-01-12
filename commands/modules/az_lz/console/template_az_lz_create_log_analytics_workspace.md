### Log Analytics Monitoring Workspace

Manages a Log Analytics (formally Operational Insights) Workspace.

**Name**

Specifies the name of the Log Analytics Workspace. Workspace name should include 4-63 letters, digits or '-'. The '-' shouldn't be the first or the last symbol. Changing this forces a new resource to be created.

**Location**

Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.

**SKU**

Specifies the SKU of the Log Analytics Workspace. Possible values are Free, PerNode, Premium, Standard, Standalone, Unlimited, CapacityReservation, and PerGB2018 (new SKU as of 2018-04-03). Defaults to PerGB2018.

**Retention In Days**

The workspace data retention in days. Possible values are either 7 (Free Tier only) or range between 30 and 730.

**Resource Group Name**

The name of the resource group in which the Log Analytics workspace is created. Changing this forces a new resource to be created.



