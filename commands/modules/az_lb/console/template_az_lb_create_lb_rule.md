### Load Balancer rule

Manages a Load Balancer Rule.


**Name**

(Required) Specifies the name of the LB Rule. Changing this forces a new resource to be created.

**Load Balancer**

(Required) Specifies the name of the Load Balancer. Changing this forces a new resource to be created.

**Protocol**

(Required) The transport protocol for the external endpoint. Possible values are Tcp, Udp or All.

**Frontend Port**

(Required) The port for the external endpoint. Port numbers for each Rule must be unique within the Load Balancer. Possible values range between 0 and 65534, inclusive.


**Backend Port**

(Required) The port used for internal connections on the endpoint. Possible values range between 0 and 65535, inclusive.



