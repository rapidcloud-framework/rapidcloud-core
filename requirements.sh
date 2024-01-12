#!/bin/bash

MODULES=(
    "coloredlogs"
    "configparser"
    "progress"
    "cx_Oracle"
    "pymssql"
    "awsglue3"
    "awswrangler"
    "boto3"
    "botocore"
    "component-extraction-api"
    "dj-git"
    "fake-awsglue"
    "jinja2"
    "json-flatten"
    "kupfer-plugin-git"
    "lambda-git"
    "modules-for-mozia"
    "mozia-modules"
    "names"
    "numpy"
    "pandas"
    "progress"
    "psycopg2"
    "pyarrow"
    "pyathena"
    "pymysql"
    "pyspark"
    "requests"
    "s3fs"
    "s3transfer"
    "setuptools"
    "sqlparse"
    "stripe"
    "tabulate"
    "mysql-connector-python"
    "pyfiglet"
    "deprecated"
    "flask"
    "flask_cors"
    "arnparse"
    "markdown"
    "cryptography"
    "python-jose"
    "flask_session"
    "tomark"
)

for MODULE in "${MODULES[@]}"
do
    pip3 install $MODULE
done