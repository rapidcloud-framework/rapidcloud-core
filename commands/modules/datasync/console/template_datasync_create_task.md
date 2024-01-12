### Datasync task

A Datasync task is what will actually help you accomplish the data transfer.

For a task you will have to pick a source and a destination.

**Rapid cloud resource name**
Name for the RC resource that will identify this within the RC console.

**Task name**
Name of the DataSync Task.

**Location Destination ID**
Location ID of the destionation for the data transfer.

**Location Source ID**
Location ID of the source for the data transfer.

**Exclude pattern**
A single filter string that consists of the patterns to exclude. The patterns are delimited by "|" (that is, a pipe), for example: /folder1|/folder2

**Include pattern**
A single filter string that consists of the patterns to exclude. The patterns are delimited by "|" (that is, a pipe), for example: /folder1|/folder2

**Schedule expression**
Specifies a schedule used to periodically transfer files from a source to a destination location. See more on scheduled expressinos [here](https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html).