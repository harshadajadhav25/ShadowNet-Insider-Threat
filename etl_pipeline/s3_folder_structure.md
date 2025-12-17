# S3 Folder Structure & Partition Strategy

This document defines how synthetic logs generated in Phase 2 will be stored inside Amazon S3 in a structured, query-optimized layout.

---

1. S3 Bucket Name

The raw logs will be stored in a bucket like:

```text
s3://shadownet-raw/

This bucket will store all raw log files generated daily by the log generator.

2. Folder Structure (Partitioning by Date)

We will use a date-partitioned layout, which is standard for Athena and Glue:

s3://shadownet-raw/
    ├── year=2025/
    │     ├── month=12/
    │     │     ├── day=01/
    │     │     │     └── logs.jsonl
    │     │     ├── day=02/
    │     │     │     └── logs.jsonl
    │     │     └── day=03/
    │     │           └── logs.jsonl

Each day folder contains one or more JSON Lines log files for that date.

3. File Naming Convention

Each daily log file will follow this naming format: logs_YYYY-MM-DD.jsonl

Examples:
logs_2025-12-01.jsonl
logs_2025-12-02.jsonl
logs_2025-12-03.jsonl

When uploaded to S3, a single day might look like: s3://shadownet-raw/year=2025/month=12/day=01/logs_2025-12-01.jsonl

4. Why Partition by Year / Month / Day?

    a. Using year, month, and day as partition keys makes it easier to:
    b. Run time-based queries in Athena (for example: one week, one month)
    c. Reduce scan costs by narrowing queries to specific dates
    d. Help Glue crawlers detect partitions automatically
    e. Align with the daily synthetic log generation process from Phase 2

5. Integration with the Log Generator

The Phase 2 log generator currently writes logs locally to: data/logs_YYYY-MM-DD.jsonl


In a future step, these files will be:

    a. Generated locally
    b. Uploaded to the appropriate S3 path: s3://shadownet-raw/year=YYYY/month=MM/day=DD/logs_YYYY-MM-DD.jsonl

6. Future Extension: Processed Logs

Later, a separate bucket or prefix will be used for processed/cleaned logs, for example:

s3://shadownet-processed/
    ├── year=2025/
    │     ├── month=12/
    │     │     ├── day=01/
    │     │     └── day=02/

This will store ETL output that is ready for ML and dashboards.