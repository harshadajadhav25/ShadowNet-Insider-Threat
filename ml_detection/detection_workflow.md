# Detection Workflow (End-to-End)

This document describes the end-to-end workflow ShadowNet uses to detect insider threats, score risk, and generate outputs for dashboards and reports.

The workflow connects:
- Raw logs (S3)
- ETL processing (Glue/Athena)
- Feature engineering
- Anomaly detection (ML + rules)
- Threat scoring
- Alerts + visualization

---

## 1. High-Level Workflow Overview

```text
Synthetic Log Generator (local)
        ↓
S3 Raw Storage (shadownet-raw)
        ↓
Glue Data Catalog (raw_logs table + partitions)
        ↓
ETL Transformations (flatten metadata + derive flags)
        ↓
Processed Dataset (shadownet-processed)
        ↓
Feature Engineering (user/day feature table)
        ↓
Detection Layer (Rules + ML anomaly model)
        ↓
Threat Scoring (risk_score + severity)
        ↓
Dashboard + Reports (Dash / CSV / PDF)
