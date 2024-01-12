### Network Watcher Flow Log

Manages a Network Watcher Flow Log.

**Name**

(Required) The name of the Network Watcher Flow Log. Changing this forces a new resource to be created.

**Resource Group Name**

(Required) The name of the resource group in which the Network Watcher was deployed. Changing this forces a new resource to be created.

**Location**

The location where the Network Watcher Flow Log resides. Changing this forces a new resource to be created. Defaults to the location of the Network Watcher.

**Network Watcher Name**

(Required) The name of the Network Watcher. Changing this forces a new resource to be created.

**Network Security Group**

(Required) The ID of the Network Security Group for which to enable flow logs for. Changing this forces a new resource to be created.

**Storage Account**

The ID of the Storage Account where flow logs are stored.

**Enabled**

(Required) Should Network Flow Logging be Enabled?

**Retention In Days**

(Required) The number of days to retain flow log records.

**Workspace Name**

(Required) The resource GUID of the attached workspace.
