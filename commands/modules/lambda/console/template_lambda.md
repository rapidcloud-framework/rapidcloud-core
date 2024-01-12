### Lambda Function

Create Lamabda Function. RapidCloud generates function template for you as well as helkpful Lambda Layers for common Python Lambda operations, including boto3 (awswrangler) and various database drivers.

**Lambda Function Name**

Lambda Function Name

**Memory**

Specify how much memory to allocate for this Lambda Function. Default is 128 MB

**Schedule**

Enter a cron expression if you want this lambda function to be automatically invoked on a specific schedule. This will create a CloudWatch Event Rule.

Example: run every day at midnight => `0 4 * * ? *`

**Environment Variables**

Environment Variables for this Lambda Function
