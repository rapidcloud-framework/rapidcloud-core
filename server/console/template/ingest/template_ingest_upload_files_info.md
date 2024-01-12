### Upload Files

Upload Files to current environment's `*-ingestion` bucket

**Select File Type to upload**

RapidCloud supports two general categories of files:
- Binary/Unstructured (e.g. invoices, documents, audio, video, images, etc)
- Semi-Structured (Json, CSV, Excel, XML)

Binary/Unstructured files get uploaded using `{env}-ingestion/files/*` S3 Object Key Prefix.

Semi-Structured files get uploaded using `{env}-ingestion/semistructured/*`  S3 Object Key Prefix.

**Samples Toggle**

Uploaded files should only be used for learning purposes. This feature is only available for Binary/Unstructured files.

Sample files get uploaded using `{env}-ingestion/files/rc-samples/{dataset_type}/*` S3 Object Key Prefix.

**File Category (aka Dataset Type)**

Select existing dataset to upload files for. If you don't see a desired dataset, then you must first add it via `Documents & Binary Files` page. 

Files get uploaded using `{env}-ingestion/files/{dataset_type}/*` S3 Object Key Prefix.

Alternatively, select `Unknown` to use RapidCloud document categorization algorithm (this is only applicable for documents). If you use `Unknown`, then you must first upload sample files.

`Unknown` files get uploaded using `{env}-ingestion/files/rc-any/*` S3 Object Key Prefix.
