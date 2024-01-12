### Transformations

Transformations are `Glue Jobs` to perform batch style data transformations, aggregations, integrations and analytics. RapidCloud generates Glue job templates for you, based on the selected `Job Type`. Transformations use `raw` catalog for input datasets and `analysis` catalog for the results. Transformations are automatically executed as part of you Data Pipeline, and when completed, they optionally trigger data publishing jobs

**Transformation Name**

Transformation Name (no spaces or special characters)

**Base Datasets**

Select source datasets from `raw` catalog for this transformation

**Job Type**

`Python Shell` and `Python Spark` job types are currently supported

**Refresh results as QuickSight SPICE dataset**

If enabled, transformation job will automatically update QuickSight SPICE Datasets to improve BI reports and dashboards performance when using Amazon QuickSight