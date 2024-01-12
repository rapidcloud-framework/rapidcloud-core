### Source Databases

Each RDBMS to be ingested via RapidCloud must be registered here.

**Database Name**

Enter database name without space or special characters. This is the name to be used by RapidCloud internally and doesn't have to be the same as the source database name. Use something meaningful (e.g. `orders`, `hr`)

**Database Engine**

Select your source database engine from the list. RapidCloud currently supports Oracle, MS SQL Server, MySQL. PostgreSQL support is coming soon.

**Database Server Address**

Specify DNS name or IP Address for your database.

**Database Server Port**

Specify port for your database.

**Database User**

Database User with permissions to get schema details, read access to data and proper access to logs for replication.

**Password**

Database Password will be encrypted and saved in AWS Secrets Manager. It will never be stored or transmitted in plain text.

**Database/Catalog/SID**

Database name or catalog name 

**Service/Schema name**

Database schema name

**Database Rate of Change (GB/hr)**

How much data is being created or changed on the average every hour? This is important for RapidCloud to determine proper on-going replication architecture.