# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* Quick summary
* Version
* [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)

### How do I get set up? ###

* Summary of set up
* Configuration
* Dependencies
* Database configuration
* How to run tests
* Deployment instructions

### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

### Who do I talk to? ###

* Repo owner or admin
* Other community or team contact

### Adding in Python Kinect-Consulting Custom Modules --> location kc-resources/modules/kc-datalake-glue-etl-toolkit-utils
### Note: Need to go back in and change the naming standard to use ALL lower case with underscore separation between words instead of camelCase.
### I still need to test all of this out whenever we get some of the AWS Services stood up.
- kc_athena_access (Class module for connecting and querying Athena)
- kc_aws_secret (Class module for accessing AWS Secret Services)
- kc_logging (Class module for json logging in AWS CloudWatch)
- kc_mysql_access (Class module for connecting and querying MySQL)
- kc_notification (CLass module for sending SNS notication)
- kc_redshift_access (Class module for connecting and querying MPP Redshift)
- kc_s3  (Class module for access AWS S3 using boto3)
- kc_snowflake_access (Class module for connecting and querying  MPP Snowflake)
- kc_sql_server_access (Class module for connecting and querying  MS SQL Server)
- kc_dq_record_count_log (Class module for log entry for our DQ Record Count Validation (AWS DynamoDB))
- kc_dq_duplicate_count_log (Class module for log entry for our DQ Duplicate Check  Validation (AWS DynamoDB))


### Adding in Python .egg distribution for the following --> location kc-resources/lib
- Python mysql-connector-python (Used for MySQL)
- Python psycopg2 (Used for Redshift)
- Python PyAthena (Used for PyAthena)
- Python pymssql (Used for MS SQL Server)
- Python s3fs (Used for  AWS S3 FUSE filesystem)
- Python snowflake-connector-py (Use for Snowflake Computing)
- Python snowflake-sqlalchemy (Used for Snowflake SQLAlchemy)
