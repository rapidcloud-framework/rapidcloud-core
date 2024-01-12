### Semi-structured Data

Register each unique type of file. RapidCloud supports ingestion of CSV, JSON, XML and Excel files.

**Enter Dataset Name with no spaces**

This uniquely identifes ingested data. For example, if you're ingesting CSV file that contains list of monthly invoices, then you can name this dataset `monthly_invoices`

**Enable this dataset?**

This instructs RapidCloud to start CDC for this dataset as soon as it is uploaded to `ingestion` bucket.

**CDC Type**

CDC (Change Data Capture) type instructs RapidCloud how to apply newly ingested files. 

- Delta (each file only contains incremental changes)
- Cumulative (each file contains all data and replaces previous file)
- Cumulative YTD (each file contains all data for specified year and replaces previous file for that year)
- Cumulative MTD (each file contains all data for specified year/month and replaces previous file for that year/month)

**File Format**

Choose file format. RapidCloud currently supports CSV, JSON, XML and Excel files

**Data Category (e.g. financials, legal, products)**

Data Category is a convenient way of categorizing your files 

**Separator Character**

This applies to CSV files only. Deafault: ","

**Use Quotes Around Strings**

This applies to CSV only

**Excel Sheet Name**

This only applies to Excel files with multiple worksheets. Leave empty if Excel file only contains one worksheet

**Enable post-processing / data enrichment for this dataset?**

This instructs RapidCloud to automatically trigger a lambda function as soon as file is ingested, to run some post-processing or business logic. For example, enriching dataset with additional data or calculating some derived values.

**Name of Post-processing lambda function**

Name of the lambda function to be created by RapidCloud to run post-processing logic

**Env Vars**

Environment Variables for post-processing Lambda Function

**Enable transformations for this dataset**

This instructs RapidCloud to automatically trigger transformation or analysis job for this dataset.

**Primary Key**

If known, enter primary key for this dataset.

**Partitions**

Comma separated list of attributes to organize this data in the datalake [default: `year,month,day,timestamp`]

**Source Location**

Source Location
