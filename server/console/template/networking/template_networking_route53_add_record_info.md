### AWS Route 53

Amazon Route 53 is a highly available and scalable DNS web service

**Record Name**

The name of the record

**Record Type**

The record type. Valid values are: A alias and non-alias, NS, CNAME, CNAME alias and TXT

**Hosted Zone Name**

Hosted zone name for a Route 53 record

**TTL**

The TTL (Time to live) of the record. (Default is 300)

**Record List**

Comma-separated list of records

**Alias record name**

The dns of the destination where this record will redirect to.


**Alias zone Id**
Zone id of the destination record this alias record will point to. Only applicable to S3 buckets, Cloudfront distributions and other records in the same route 53 zone.

**Evaluate targets health**
Set to true if you want Route 53 to determine whether to respond to DNS queries using this resource record set by checking the health of the resource record set.