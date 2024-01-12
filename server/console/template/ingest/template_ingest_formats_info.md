### Data Formatting

Specify formatting rules at the field level for a dataset 

**Data Pipeline Phase**

Data formatting is currently only supported during ingestion

**Dataset Name**

Select existing dataset 

**Attribute Name**

Enter attribute name

**Attribute Type**

Select attribute type 

**Source Format**

Specify source format using Python format structure

Examples:
- Dates: '%m/%d/%Y' (10/15/2020), '%m/%d/%Y %H:%M' (10/15/2020 13:59)
- Amount: '$*' ($152.75) 
- Full Name: 'l,f' (Doe, John), 'f l'
- Use "eval" to instruct RapidCloud to apply "`target format`" by evaluating Python statement

**Target Format**

Specify target format using Python format structure

Examples:
- Dates: '%Y-%m-%d' (2020-10-15)
- Amount: '*' (152.75)
- Full Name: 'split'
- Enter Python statement (e.g `patient_gender[0].upper()`) if "`source format`" is `eval`
