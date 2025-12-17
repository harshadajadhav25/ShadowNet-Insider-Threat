# AWS Glue Table Schema (ShadowNet Logs)

This document defines the schema for the AWS Glue Data Catalog table that represents raw log data stored in Amazon S3.

---

1. Glue Database Name

We will create a Glue database called:

```text
shadownet_logs

2. Table Name

The name of the table will represent the raw logs is: raw_logs

3. Table Location
The logs are stored in the following S3 path: s3://shadownet-raw/

4. SerDe & Input Format

    a. InputFormat: org.apache.hadoop.mapred.TextInputFormat
    b. SerDe: org.apache.hive.hcatalog.data.JsonSerDe
    c. OutputFormat: org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat

These settings are appropriate for processing JSON Lines files in S3.

5. Table Columns

Below is the schema for the raw_logs table. The metadata field will contain a nested JSON object with additional event-specific details.

| Column       | Type   | Description                                                                        |
| ------------ | ------ | ---------------------------------------------------------------------------------- |
| `timestamp`  | string | The timestamp of the log event in ISO-8601 format (UTC).                           |
| `event_type` | string | Type of the event (e.g., `auth.login`, `iam.change_role`, `access.s3`).            |
| `user_id`    | string | The unique ID of the user or system triggering the event.                          |
| `dept`       | string | The department of the user (e.g., `Engineering`, `HR`, `Finance`).                 |
| `src_ip`     | string | The source IP address where the event originated from.                             |
| `resource`   | string | The resource being accessed or modified (e.g., `vpn_gateway`, `EC2`, `S3 bucket`). |
| `status`     | string | The status of the event (e.g., `success`, `failure`).                              |
| `metadata`   | string | JSON string containing event-specific details.                                     |

6. Partion Keys

We will partition the table by year, month, and day to optimize query performance in Athena.

| Partition Key | Type |
| ------------- | ---- |
| `year`        | int  |
| `month`       | int  |
| `day`         | int  |

7. Glue Table DDL (Example)

Here is an example of the Glue DDL (Data Definition Language) that could be used to create the raw_logs table:

CREATE EXTERNAL TABLE IF NOT EXISTS shadownet_logs.raw_logs (
    timestamp string,
    event_type string,
    user_id string,
    dept string,
    src_ip string,
    resource string,
    status string,
    metadata string
)
PARTITIONED BY (year int, month int, day int)
ROW FORMAT SERDE 'org.apache.hive.hcatalog.data.JsonSerDe'
WITH SERDEPROPERTIES (
  "serialization.encoding"="UTF-8"
)
LOCATION 's3://shadownet-raw/'
TBLPROPERTIES ("skip.header.line.count"="1");

8. Crawlers & Glue Jobs

Once the table is created, a Glue crawler can be used to crawl the S3 path (s3://shadownet-raw/) and automatically populate the Glue table partitions.

Future Glue jobs can process the data, transform it (e.g., flatten metadata), and store it in s3://shadownet-processed/ for downstream analysis.

9. Integration with Athena

Athena will query the raw_logs table and allow you to run SQL queries on the logs directly from S3.

Example Athena query:

SELECT user_id, COUNT(*) AS failed_logins
FROM shadownet_logs.raw_logs
WHERE status = 'failure'
GROUP BY user_id;