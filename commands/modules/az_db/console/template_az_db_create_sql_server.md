### MSSQL Server

Manages a Microsoft SQL Azure Database Server.


**Name**

(Required) The name of the Microsoft SQL Server. This needs to be globally unique within Azure. Changing this forces a new resource to be created.

**Resource Group Name**

(Required) The name of the resource group in which to create the Microsoft SQL Server. Changing this forces a new resource to be created.

**Location**

(Required) Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.

**Administrator Login**

(Optional) The administrator login name for the new server. Required unless azuread_authentication_only in the azuread_administrator block is true. When omitted, Azure will generate a default username which cannot be subsequently changed. Changing this forces a new resource to be created.

**Administrator Login Password**

 (Optional) The password associated with the administrator_login user. Needs to comply with Azure's Password Policy. Required unless azuread_authentication_only in the azuread_administrator block is true.

**AD Admin**

 The login username of the Azure AD Administrator of this SQL Server.

**Object Id**

(Required) The object id of the Azure AD Administrator of this SQL Server.

 **DNS Alias**

(Required) The name which should be used for this MSSQL Server DNS Alias. Changing this forces a new MSSQL Server DNS Alias to be created.

 **Subnet**

(Required) The ID of the subnet from which the SQL server will accept communications.

 **Start IP Address**

(Required) Specifies the Start IP Address associated with this Firewall Rule.

 **End IP Address**

(Required) Specifies the End IP Address associated with this Firewall Rule.

