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

Planned next steps:

- Designing S3 folder hierarchy  
- Creating AWS Glue Data Catalog schemas  
- Writing transformation logic (PySpark-style)  
- Writing Athena queries for raw → processed logs  

---