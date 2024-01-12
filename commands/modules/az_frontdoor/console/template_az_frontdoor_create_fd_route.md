### Azure Front Door Route

Create the `Azure Front Door Route`  
---
## Inputs

**Route Name**

*Required*
The name of the `Route`.

**Resource Group**
*Required*
The name of the resource group.

**Endpoint**
*Required*
The Front Door Endpoint where this Front Door Route should exist.

**Domains**
*Required*
One or more Front Door Domains that this Front Door Route will be associated with.

**Origin Group**
*Required*
The Front Door Origin Group where this Front Door Route should be created.

**Origins**
*Required*
One or more Front Door Origins that this Front Door Route will link to.

**Patterns to Match**
*Required*
The route patterns of the rule.

**Supported Protocols**
*Required*
One or more protocols supported by this Front Door Route.

**Redirect Https**
*Required*
Automatically redirect HTTP traffic to HTTPS.

**Enable Caching**
*Required*
Indicate whether the caching should be enabled for this route.

**Query Srting Caching Behavior**
*Required*
Defines how the Front Door Route will cache requests that include query strings.

**Forwarding Protocol**
*Required*
The protocol that will be use when forwarding traffic to backends

**Tags**
*Optional*
The tags you wish to apply to the front door route.