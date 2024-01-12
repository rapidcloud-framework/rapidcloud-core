### Replication Schedule

Use cases that don't use DMS built-in on-going replication require replication scheduling via RapidCloud. This would be the case for larger dataabses with significant rate-of-change. For these use cases RapidCloud allows to set up tree types of replications.

* Full replication for smaller tables
* CDC for Inserts
* CDC for Updates

**Replication Type**

Select an already registered database name from the list

**Enter schedule as cron expression**

Example: run every day at midnight => `0 4 * * ? *`

**Enable this migration task**

Replication via DMS Tasks is not enabled by default

