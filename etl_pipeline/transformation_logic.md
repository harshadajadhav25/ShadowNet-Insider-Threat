# Transformation Logic (ETL Processing Plan)

This document outlines the transformation steps that will be applied to raw ShadowNet logs after they are loaded from S3. The goal is to clean, normalize, and enrich the data so it can be used for anomaly detection and analytics.

---

1. ETL Goals

The ETL (Extract, Transform, Load) process for ShadowNet should:

- Read **raw JSONL logs** from `s3://shadownet-raw/`
- Flatten useful fields from the `metadata` JSON object
- Add **derived features** related to insider threat behavior
- Filter out corrupt or incomplete records
- Write a **processed dataset** to `s3://shadownet-processed/` in a columnar format (e.g., Parquet)

---

2. Input Dataset (Raw Logs)

The input is the `raw_logs` table in Glue / Athena:

- Location: `s3://shadownet-raw/`
- Format: JSON Lines (`.jsonl`)
- Partitioned by: `year`, `month`, `day`
- Columns:
  - `timestamp`, `event_type`, `user_id`, `dept`, `src_ip`, `resource`, `status`, `metadata` (string/JSON)

Example PySpark read (conceptual):

```python
df_raw = spark.read.json("s3://shadownet-raw/year=*/month=*/day=*/logs_*.jsonl")

Or via Glue Data Catalog table:

df_raw = glueContext.create_dynamic_frame.from_catalog(
    database="shadownet_logs",
    table_name="raw_logs"
).toDF()


3. Step-by-Step Transformation Plan

Step 1 — Basic Cleanup

    Drop rows with missing critical fields: timestamp,event_type, user_id

    Conceptual PySpark: df = df_raw.dropna(subset=["timestamp", "event_type", "user_id"])

Step 2 — Parse Timestamp & Add Time Components

    a. Convert timestamp string → proper timestamp type
    b. Extract hour, day, etc.

    from pyspark.sql.functions import col, hour, to_timestamp

    df = df.withColumn("ts", to_timestamp(col("timestamp"))) \
        .withColumn("hour", hour(col("ts")))

These fields are useful to detect after-hours behavior.

Step 3 — Flatten Metadata Fields

    Depending on event_type, different keys exist in metadata.
    We extract common ones for analysis:

    Examples:

        For auth.login:

            login_result
            auth_method
            mfa_used

        For access.s3:
            operation
            bytes

        For iam.change_role:
            change_type
            target_user
            old_roles
            new_roles
            ticket_id

    Conceptual PySpark using JSON functions:

    from pyspark.sql.functions import json_extract, json_extract_scalar

    # Example: extract login result from metadata JSON
    df = df.withColumn("login_result", json_extract_scalar("metadata", "$.login_result")) \
        .withColumn("auth_method", json_extract_scalar("metadata", "$.auth_method")) \
        .withColumn("mfa_used", json_extract_scalar("metadata", "$.mfa_used")) \
        .withColumn("bytes", json_extract_scalar("metadata", "$.bytes"))

Step 4 — Add Derived Flags & Features

    We derive features used for anomaly detection.

    4.1 After-hours login flag
        from pyspark.sql.functions import when

        df = df.withColumn(
            "after_hours_flag",
            when((col("event_type") == "auth.login") & ((col("hour") < 8) | (col("hour") > 18)), 1).otherwise(0)
        )

    4.2 Failed login flag
        df = df.withColumn(
            "failed_login_flag",
            when((col("event_type") == "auth.login") & (col("status") == "failure"), 1).otherwise(0)
        )

    4.3 Potential privilege escalation flag
        df = df.withColumn(
            "priv_escalation_flag",
            when(
                (col("event_type") == "iam.change_role") &
                (col("metadata").contains("Admin")),
                1
            ).otherwise(0)
        )

Step 5 — Aggregate Features per User (Optional)

    We can compute daily aggregates per user_id + date:

    Examples:
        failed_login_count
        after_hours_login_count
        s3_high_volume_count
        priv_escalation_events

    Conceptual PySpark:

        from pyspark.sql.functions import date_format, sum as _sum

        df = df.withColumn("event_date", date_format(col("ts"), "yyyy-MM-dd"))

        df_user_daily = df.groupBy("user_id", "dept", "event_date").agg(
            _sum("failed_login_flag").alias("failed_login_count"),
            _sum("after_hours_flag").alias("after_hours_login_count"),
            _sum("priv_escalation_flag").alias("priv_escalation_events"),
            _sum("s3_high_volume_flag").alias("s3_high_volume_events")
        )


    This aggregated dataset can be used directly by ML models.

4. Output Dataset (Processed Logs)

    Processed logs can be stored in: s3://shadownet-processed/

    Partitioned by: year, month, day

    Example write (conceptual):

        df.write.mode("overwrite") \
        .partitionBy("year", "month", "day") \
        .parquet("s3://shadownet-processed/")


    Or for aggregated user-level data:

        df_user_daily.write.mode("overwrite") \
        .partitionBy("event_date") \
        .parquet("s3://shadownet-processed/user_daily/")

5. Summary

    The transformation logic:

    1. Reads raw JSONL logs from s3://shadownet-raw/
    2. Cleans and parses core fields
    3. Flattens the metadata JSON
    4. Adds derived flags and behavioral features
    5. Writes processed, query-friendly data to s3://shadownet-processed/

This ETL layer bridges the gap between raw logs and ML-ready datasets used for insider threat detection.