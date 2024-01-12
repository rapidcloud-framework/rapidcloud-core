### Azure Container Registry

Create the `Azure Container Registry`  
---
## Inputs

**Registry Name**

*Required*
The name of the `Container Registry`. 

**Resource Group Name**
*Required*
The name of the resource group.

**Location**
*Required*
The location where the registry should be created.

**SKU**
*Required*
The SKU name of the container registry.

**Enable Public Access**
*Required*
Whether public network access is allowed for the container registry.

**Enable Encryption**
*Required*
Whether encryption is allowed for the container registry.

**Encryption Identity**
*Required*
The managed identity associated with the encryption key.

**Encryption Key**
*Required*
The key used for encryption.

**Identity Type**
*Required*
The type of managed identity used for the container registry.

**Managed Identity**
*Required*
The managed identities used for the container registry.

**Enable Admin**
*Required*
Enable admin user on the container registry.

**Geolocations**
*Required*
The list of locations where the container registry would be replicated to.