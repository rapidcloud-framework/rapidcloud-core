### Role Assignment

Assigns a given Principal (User or Group) to a given Role.

**Name**

 The scope at which the Role Definition applies to, such as /subscriptions/0b1f6471-1bf0-4dda-aec3-111122223333, /subscriptions/0b1f6471-1bf0-4dda-aec3-111122223333/resourceGroups/myGroup, or /subscriptions/0b1f6471-1bf0-4dda-aec3-111122223333/resourceGroups/myGroup/providers/Microsoft.Compute/virtualMachines/myVM. It is recommended to use the first entry of the assignable_scopes. Changing this forces a new resource to be created.

**Permission Actions**

(Optional) One or more Allowed Actions, such as *, Microsoft.Resources/subscriptions/resourceGroups/read. See 'Azure Resource Manager resource provider operations' for details.
**Permission no Actions**

(Optional) One or more Disallowed Actions, such as *, Microsoft.Resources/subscriptions/resourceGroups/read. See 'Azure Resource Manager resource provider operations' for details.

**Data Actions**

data_actions - (Optional) One or more Allowed Data Actions, such as *, Microsoft.Storage/storageAccounts/blobServices/containers/blobs/read. See 'Azure Resource Manager resource provider operations' for details.

**Data no Actions**

not_data_actions - (Optional) One or more Disallowed Data Actions, such as *, Microsoft.Resources/subscriptions/resourceGroups/read. See 'Azure Resource Manager resource provider operations' for details.

**Assignable Scopes**

(Optional) One or more assignable scopes for this Role Definition, such as /subscriptions/0b1f6471-1bf0-4dda-aec3-111122223333, /subscriptions/0b1f6471-1bf0-4dda-aec3-111122223333/resourceGroups/myGroup, or /subscriptions/0b1f6471-1bf0-4dda-aec3-111122223333/resourceGroups/myGroup/providers/Microsoft.Compute/virtualMachines/myVM

**Principal Id**

(Required) The ID of the Principal (User, Group or Service Principal) to assign the Role Definition to. Changing this forces a new resource to be created.



