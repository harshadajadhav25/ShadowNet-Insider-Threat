# 🛡️ ShadowNet — Insider Threat Detection Simulator

ShadowNet is a **Data Engineering + Cybersecurity project** that simulates real-world insider threats and models how logs flow through an AWS pipeline, how anomalies are detected, and how threat activity is visualized through dashboards.

This project includes:
- Synthetic security log generation  
- An AWS ETL pipeline (S3 → Glue → Athena)  
- Anomaly detection logic (ML + rule-based)  
- A Dash dashboard for visualizing suspicious behavior  

---

## 🎯 Project Goals

ShadowNet simulates and analyzes multiple insider threat behaviors, such as:

- **Privilege escalation**  
- **After-hours login anomalies**  
- **Lateral movement across systems**  
- **Misuse of S3/EC2 administrative privileges**

The project covers:
- Designing the log schema  
- Creating synthetic log events  
- Building AWS data pipelines  
- Developing anomaly detection logic  
- Designing visual dashboards  
- Writing a portfolio-grade technical report  

---

## 📅 Phase 1 (Week 1): Planning

During Phase 1, the following tasks were completed:

1. **Defined four insider threat scenarios**  
2. **Designed the complete data schema** (log fields + event types)  
3. **Created a high-level architecture diagram**  
4. **Set up the project folder structure**  
5. **Prepared the repository for Phase 2 development**

---

## 📅 Phase 2 (Week 2): Synthetic Log Generation

During Phase 2, the following work was completed:

### Designed Log Specifications  
`synthetic_log_spec.md` includes structure, fields, patterns, and log volume expectations.
### Built the Insider Threat Event Dictionary  
Defines each threat scenario and maps it to specific log events.
### Documented the Log Automation Workflow  
Explains daily log generation and storage.
### Implemented the First Working Python Log Generator  
File located at: `log_generator/log_generator.py`
### Generated Example JSONL Logs  
Stored in the `data/` folder (excluded from GitHub).

---

# Running the Log Generator

## **1. Activate your virtual environment**

### **PowerShell (with bypass):**
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

### **Command Prompt:**
```cmd
.venv\Scripts\activate.bat
```
### **Mac/Linux:**
```bash
source .venv/bin/activate
```

---

## **2. Run the generator**
```bash
python log_generator/log_generator.py
```
This will generate a file such as:
```
data/logs_YYYY-MM-DD.jsonl
```
Each line is one JSON event (e.g., `auth.login`, `failure`, `after-hours`, etc.).

---

## 📅 Phase 3 

During Phase 3, the following ETL design work was completed:

1. Designed the S3 Folder Hierarchy

    Date-partitioned structure (year=YYYY/month=MM/day=DD/)

    Documented in:
    etl_pipeline/s3_folder_structure.md

2. Created AWS Glue Table Schema

    Defined raw logs table (raw_logs)

    Specified SerDe, partition keys, and DDL

    Documented in:
    etl_pipeline/glue_table_schema.md

3. Wrote ETL Transformation Logic (PySpark-style)

    Flattening metadata fields

    Adding derived features (after-hours flag, failed login flag, etc.)

    Designing processed dataset (s3://shadownet-processed/)

    Documented in:
    etl_pipeline/transformation_logic.md

4. Designed Athena Query Plan

    Queries for failed logins, after-hours logins, privilege escalation, S3 misuse

    Partition-aware query patterns

    Documented in:
    etl_pipeline/athena_query_plan.md

## 📅 Phase 4

During Phase 4, the following detection design work was completed:

1. Defined Detection Signals
Authentication, access, privilege, and cloud-based signals
Documented in:
ml_detection/detection_signals.md

2. Designed Feature Engineering Plan
User-day aggregated features for ML and scoring
Documented in:
ml_detection/feature_engineering.md

3. Designed Anomaly Detection Models
Rule-based detection
Unsupervised ML (Isolation Forest, clustering)
Hybrid detection strategy
Documented in:
ml_detection/anomaly_models.md

4. Created Threat Scoring Matrix
Mapped signals to risk points
Defined severity levels (Low / Medium / High / Critical)
Documented in:
ml_detection/threat_scoring_matrix.md

5. Documented End-to-End Detection Workflow
From processed logs → features → detection → scoring → alerts
Documented in:
ml_detection/detection_workflow.md

Phase 5 (Upcoming): Dashboard & Reporting

Next steps include:
Designing dashboard wireframes
Mapping processed data to visualizations
Building a Dash-based threat analytics dashboard
Creating exportable reports (CSV / PDF)