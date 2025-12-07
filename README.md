# 🛡️ ShadowNet — Insider Threat Detection Simulator

ShadowNet is a **Data Engineering + Cybersecurity project**.  
It simulates real-world insider threats and models how logs move through an AWS pipeline, how anomalies are detected, and how threat activity is visualized through dashboards.

This project includes:
- Synthetic security log generation  
- An AWS ETL pipeline (S3 → Glue → Athena)  
- Anomaly detection logic (ML + rule-based)  
- A Dash dashboard for visualizing suspicious behavior  

---

## 🎯 Project Goals

ShadowNet will simulate and analyze multiple insider threat behaviors, including:

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

## 📅 Phase 1 (Week 1): Planning

During Phase 1, we will:

1. **Define four insider threat scenarios**  
2. **Design the complete data schema** (log fields + event types)  
3. **Create a high-level architecture diagram**  
4. **Set up the project folder structure**  
5. **Prepare the repository for Phase 2 development**

📂 **Phase 1 Docs:**  
Located in the `docs/` folder:
- `docs/threat_scenarios/`
- `docs/schema/`
- `docs/architecture/`
---

# 📅 Phase 2 (Week 2): Synthetic Log Generation — ✅ Completed

During Phase 2, the following work was completed:

### ✔ Designed log specifications  
- `synthetic_log_spec.md` includes format, fields, patterns, and log volume.

### ✔ Built the Insider Threat Event Dictionary  
- Maps every threat scenario to the events that represent it.

### ✔ Documented the Log Automation Workflow  
- How logs are generated daily and stored.

### ✔ Implemented the first working Python Log Generator  
File: log_generator/log_generator.py


### ✔ Generated example JSONL logs
Stored in the `data/` folder (not committed to GitHub).

📂 **Phase 2 Docs:**  
- `docs/logs/synthetic_log_spec.md`  
- `docs/logs/insider_threat_event_dictionary.md`  
- `docs/logs/log_automation_workflow.md`

---

# 🧪 Running the Log Generator

### 1. Activate your virtual environment

**PowerShell (with bypass):**
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1

Command Prompt:
    .venv\Scripts\activate.bat
Mac/Linux:
    source .venv/bin/activate

2. Run the generator
    python log_generator/log_generator.py

This will create:
    data/logs_YYYY-MM-DD.jsonl

Each line is one JSON event (auth.login, failure, after-hours, etc.).

## Phase 3 will include:

    Designing S3 folder hierarchy
    Creating AWS Glue Data Catalog schemas
    Planning PySpark-style transformation logic
    Writing Athena queries for raw → processed logs