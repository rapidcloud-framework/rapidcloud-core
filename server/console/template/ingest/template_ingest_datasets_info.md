### Database Tables

Depending on your specific use case, you may want to ingest only some tables or all. RapidCloud needs to know that.

**Database Name**

Select an already registered database name from the list

**Schema Name**

Schema name is automatically selected based on database selection 

**Include Tables**

Select table names or `all` to include all tables

**Table Size**

Select size of table to indicate type of DMS task. `Small` will be ingested and replaced based on schedule. `Medium`, `Large`, and `Xlarge` will be ingested using incremental replication.

**Dataset Prefix**

Example: prefix `hr_` for source table employee will create dataset `hr_employee`

**Partitions**

Comma separated list of attributes to organize this data in the datalake [default: year,month,day]. This will be applied to `raw` (aka organized) bucket in the datalake.