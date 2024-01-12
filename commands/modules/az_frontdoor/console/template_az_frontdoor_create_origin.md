### Azure Front Door Origin

Create the `Azure Front Door Origin`  
---
## Inputs

**Origin Name**

*Required*
The name of the `Origin`.

**Origin Group**
*Required*
The front door origin group where the origin will be created.

**Hostname**
*Required*
The IPv4 address, IPv6 address or domain name of the origin

**Enable Certificate Check**
*Required*
Specify whether certificate name checks should be enabled for this origin. When this is enabled, Azure Front Door will validate if the request host name matches the host name in the certificate provided by the origin.