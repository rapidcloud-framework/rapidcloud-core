### Azure Container App

Create the `Azure Container App`  
---
## Inputs

**Container App Name**

*Required*
The name of the `Container App`. 

**Resource Group Name**
*Required*
The name of the resource group.

**Container App Environment**
*Required*
The name of the container app environment.

**Revision Mode**
*Required*
Revisions operational mode for container app

**Container Name**
*Required*
Name of the container. The name must consist of lower case alphanumeric characters, '-' or '.', and must start and end with an alphanumeric character.

**Container Image**
*Required*
The image to use to create the container.

**Container CPU**
*Required*
The amount of vCPU to allocate to the container.

**Container Memory**
*Required*
The amount of memory to allocate to the container. `cpu` and `memory` must be specified in 0.25'/'0.5Gi combination increments. e.g. 1.25 / 2.5Gi or 0.75 / 1.5Gi

**Container Arguments**
*Optional*
A comma-separated list of extra arguments to pass to the container.

**Container Probe Path**
*Optional*
The URI to use with the host for http type probes.

**Container Probe Port**
*Optional*
The port number on which to connect. Possible values are between `1` and `65535`

**Maximum number of replicas**
*Optional*
The maximum number of replicas for this container. Defaults to 3.

**Managed Identity Type**
*Required*
The type of managed identity to assign.

**Managed Identities**
*Optional*
One or more user-assigned managed identities to assign. Required when `Managed Identity Type` is set to `UserAssigned`

**Target Port for Ingress**
*Required*
The port to use for ingress. Defaults to 80

**Transport Method for Ingress**
*Required*
The transport method for the Ingress.

**Registry Server**
*Required*
The hostname for the Container Registry.

**Managed Identity to use**
*Optional*
The User Assigned Managed identity to use when pulling from the Container Registry. Either the Managed Identity or the username/password value must be specified.

**Registry Username**
*Optional*
The username to use for this Container Registry.

**Registry Password Secret**
*Optional*
The name of the Secret Reference containing the password value for this user on the Container Registry, `username` must also be supplied..

