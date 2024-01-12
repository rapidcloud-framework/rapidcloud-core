### App Service Plan

Manages an App Service: Service Plan.

**Name**

(Required) The name which should be used for this Service Plan. Changing this forces a new AppService to be created.

**Resource Group Name**

(Required) The name of the Resource Group where the AppService should exist. Changing this forces a new AppService to be created.

**Location**

(Required) The Azure Region where the Service Plan should exist. Changing this forces a new AppService to be created.

**SKU**

(Required) The SKU for the plan. Possible values include B1, B2, B3, D1, F1, I1, I2, I3, I1v2, I2v2, I3v2, I4v2, I5v2, I6v2, P1v2, P2v2, P3v2, P0v3, P1v3, P2v3, P3v3, P1mv3, P2mv3, P3mv3, P4mv3, P5mv3, S1, S2, S3, SHARED, EP1, EP2, EP3, WS1, WS2, WS3, and Y1.

**OS Type**

(Required) The O/S type for the App Services to be hosted in this plan. Possible values include Windows, Linux, and WindowsContainer. Changing this forces a new resource to be created.

**Service Environment**

(Optional) The App Service Environment to create this Service Plan in.







