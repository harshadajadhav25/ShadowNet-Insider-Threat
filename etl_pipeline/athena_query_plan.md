# Athena Query Plan

This document describes the main Amazon Athena queries that will be used to explore and analyze ShadowNet logs stored in S3.  
These queries operate on the `shadownet_logs.raw_logs` table defined in the Glue Data Catalog.

---

1. View Sample Raw Data

Used to quickly inspect logs and validate ingestion.

```sql
SELECT *
FROM shadownet_logs.raw_logs
LIMIT 20;

2. Count Events per Day

    Basic volume check to ensure logs are arriving correctly and to observe daily patterns.

    SELECT
    year,
    month,
    day,
    COUNT(*) AS total_events
    FROM shadownet_logs.raw_logs
    GROUP BY year, month, day
    ORDER BY year, month, day;

3. Failed Login Attempts per User

    Identify users with a high number of failed logins (possible brute-force or compromised credentials).

    SELECT
    user_id,
    COUNT(*) AS failed_login_count
    FROM shadownet_logs.raw_logs
    WHERE event_type = 'auth.login'
    AND status = 'failure'
    GROUP BY user_id
    ORDER BY failed_login_count DESC;

4. After-hours Login Activity

    Find logins that occur outside normal business hours (e.g., before 08:00 or after 18:00).

    SELECT
    user_id,
    timestamp,
    src_ip,
    dept
    FROM shadownet_logs.raw_logs
    WHERE event_type = 'auth.login'
    AND (
        hour(from_iso8601_timestamp(timestamp)) < 8
        OR hour(from_iso8601_timestamp(timestamp)) > 18
    )
    ORDER BY timestamp DESC;

5. IAM Privilege Escalation Events

    Focus on role change events and look for those that mention admin-like privileges in the metadata.

    SELECT
    timestamp,
    user_id,
    resource,
    metadata
    FROM shadownet_logs.raw_logs
    WHERE event_type = 'iam.change_role'
    AND metadata LIKE '%Admin%';

6. High-volume S3 Access

    Identify potential data exfiltration by looking for large S3 GET operations.

    Assuming bytes is stored inside metadata as JSON:

    SELECT
    user_id,
    resource AS bucket_name,
    metadata,
    CAST(json_extract_scalar(metadata, '$.bytes') AS bigint) AS bytes_transferred
    FROM shadownet_logs.raw_logs
    WHERE event_type = 'access.s3'
    AND CAST(json_extract_scalar(metadata, '$.bytes') AS bigint) > 10000000
    ORDER BY bytes_transferred DESC;

7. EC2 State Change Events

    Check for suspicious EC2 stop/terminate events, especially those happening off-hours.

    SELECT
    timestamp,
    user_id,
    resource AS instance_id,
    metadata
    FROM shadownet_logs.raw_logs
    WHERE event_type = 'cloud.ec2_state_change'
    AND (
        metadata LIKE '%terminate%' OR
        metadata LIKE '%stop%'
    )
    ORDER BY timestamp DESC;

8. Security Group Updates (Wide-open Access)

    Find security group changes that may have opened resources to the entire internet (0.0.0.0/0).

    SELECT
    timestamp,
    user_id,
    resource AS security_group_id,
    metadata
    FROM shadownet_logs.raw_logs
    WHERE event_type = 'cloud.sg_update'
    AND metadata LIKE '%0.0.0.0/0%';

9. Daily Risk Indicators (Conceptual Aggregation)

    A query to compute simple “risk indicators” per user per day (can be extended later):

    SELECT
    user_id,
    COUNT_IF(event_type = 'auth.login' AND status = 'failure') AS failed_logins,
    COUNT_IF(event_type = 'auth.login' AND (
        hour(from_iso8601_timestamp(timestamp)) < 8
        OR hour(from_iso8601_timestamp(timestamp)) > 18
    )) AS after_hours_logins,
    COUNT_IF(event_type = 'iam.change_role') AS iam_changes,
    COUNT_IF(event_type = 'access.s3' AND
        CAST(json_extract_scalar(metadata, '$.bytes') AS bigint) > 10000000
    ) AS high_volume_s3_events
    FROM shadownet_logs.raw_logs
    GROUP BY user_id
    ORDER BY failed_logins DESC;

    (Note: COUNT_IF is supported in Athena engine 3—if not available, replace with SUM(CASE WHEN ... THEN 1 ELSE 0 END).)

10. Query Optimization Tips

    Always filter by partitions where possible:

    SELECT *
    FROM shadownet_logs.raw_logs
    WHERE year = 2025
    AND month = 12
    AND day = 1;


    1. Avoid SELECT * in production queries; select only needed columns.
    2. Use JSON functions (json_extract, json_extract_scalar) to pull fields from the metadata JSON string.
    3. Add additional views or materialized tables for pre-aggregated risk scores later.

Summary

These Athena queries support:

    1. Basic data validation
    2. Security investigations
    3. Detection of insider threat patterns
    4. Input feature generation for ML models

They sit on top of the S3 + Glue table/partitioning design documented in earlier ETL steps.