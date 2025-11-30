# ShadowNet Architecture

This document explains the high-level architecture of the ShadowNet Insider Threat Detection Simulator.

The diagram in this folder (`architecture.png`) shows how data flows through the system from log generation to visualization.

---

## 1. Synthetic Log Generator (Python)

- This is a Python-based component that creates **synthetic security logs**.
- It simulates:
  - Authentication events (logins, logouts, failures)
  - IAM changes (role changes, policy attachments)
  - Data access (S3, databases, internal apps)
  - Cloud resource activity (EC2, security groups)
- The logs follow the schema defined in `docs/schema/`.

Output: log files (for example JSON or CSV) that look like real security activity.

---

## 2. S3 Raw Storage (Logs)

- The synthetic log files are uploaded into an **Amazon S3 bucket**.
- This acts as the **raw data lake** for ShadowNet.
- Logs can be partitioned by date and/or event type (for example: `year=2025/month=11/day=29`).

Output: raw log data stored in S3, ready to be cataloged.

---

## 3. AWS Glue Data Catalog

- AWS Glue is used to **catalog** the log data into structured tables.
- You can:
  - Define table schemas for each type of log
  - Or use a Glue Crawler to automatically infer the schema
- Once cataloged, the data becomes queryable through Amazon Athena.

Output: a searchable data catalog that knows how to read your log files.

---

## 4. Athena Queries / Transformations

- Amazon Athena runs **SQL queries** directly on the data stored in S3.
- This layer is used to:
  - Filter, clean, and transform raw logs
  - Aggregate events per user, per day, per department
  - Prepare features for anomaly detection (for example: failed_login_count, after_hours_login_rate, data_volume_read)

Output: transformed datasets and feature tables ready for analysis.

---

## 5. ML Anomaly Detection (Python / Notebook)

- Processed features are taken into Python (for example, in notebooks or scripts).
- Here you implement **anomaly detection logic**, which may include:
  - Simple rules (thresholds)
  - Scoring systems
  - Machine learning models (for example, clustering or outlier detection)
- This component assigns a **risk score or severity label** to events or users.

Output: a table or dataset of users/events with anomaly scores and severity levels.

---

## 6. Dash Dashboard + Reports (PDF/CSV)

- A **Dash** dashboard (built in Python) visualizes:
  - Anomalous users
  - Threat scores over time
  - Breakdown of events by department, type, and severity
- The dashboard can also provide:
  - Filters (by user, department, event type, time range)
  - Export options (PDF or CSV reports for sharing investigation results)

Output: visual interface and reports that help humans understand and act on detected threats.

---

## End-to-End Flow

1. Generate synthetic security logs in Python  
2. Store them in S3 as raw log files  
3. Catalog them with AWS Glue  
4. Query and transform them with Athena  
5. Run anomaly detection logic in Python  
6. Visualize results in a Dash dashboard and export reports  

This architecture makes ShadowNet a realistic, end-to-end simulation of a modern security analytics pipeline.
