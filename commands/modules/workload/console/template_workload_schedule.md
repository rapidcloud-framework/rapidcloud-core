### Workload Schedule

Use this page to schedule pause and resume times for your workload. You can create multiple schedules to fit your requirements.

For example, separate schedule for compute resources vs database resources. Or different schedule for weekdays vs weekends.

**Schedule Name**

Short identifier for this schedule. Up to 12 characters, no spaces.

**Schedule Description**

Schedule description

**Resource Types to Pause**

One or more resource types to be paused/resumed on this schedule


**Enter cron expression to schedule workload pause**

_Example:_ pause every weekday at 7 PM EST => `0 0 ? * MON-FRI *`

**Enter cron expression to schedule workload resume**

_Example:_ resume every weekday at 7 AM EST => `0 12 ? * MON-FRI *`
