# Feature Engineering Plan

This document defines the feature engineering strategy for ShadowNet’s insider threat detection system.  
Features are derived from raw + processed logs (ETL output) and are designed to capture deviations from normal user behavior.

The features will be used for:
- Rule-based detection
- Unsupervised anomaly detection models
- Threat scoring and alerting

---

## 1. Feature Types

ShadowNet uses three main feature categories:

1. **Authentication Features**  
2. **Access & Movement Features**  
3. **Privilege & Cloud Activity Features**

Features are typically aggregated per:
- **user_id**
- **day (event_date)**  
(optionally also per hour or rolling time window)

---

## 2. Input Data for Features

Features will be computed from:

- Raw logs stored in S3 (`shadownet-raw`)
- Processed logs from ETL output (`shadownet-processed`)
- Flattened columns extracted from `metadata`

Core fields:
- `timestamp`, `event_type`, `user_id`, `dept`, `src_ip`, `resource`, `status`

Important metadata fields (flattened during ETL):
- `login_result`, `auth_method`, `mfa_used`
- `bytes`, `operation`
- `change_type`, `target_user`, `new_roles`, `ticket_id`
- `action`, `instance_id`, `rule_change`

---

## 3. Feature Table Design

### 3.1 Primary Feature Table (User Daily Aggregates)

A primary dataset will contain one row per user per day:

**Key columns:**
- `user_id`
- `dept`
- `event_date`

**Feature columns** (examples below).

This table becomes the main input for anomaly detection.

---

## 4. Authentication Features

### 4.1 failed_login_count
**Definition:** Number of failed logins per user per day  
**Why it matters:** High values may indicate brute-force or compromised credentials.

### 4.2 failed_login_rate
**Definition:** failed logins / total logins per day  
**Why it matters:** Helps normalize behavior across heavy vs light users.

### 4.3 after_hours_login_count
**Definition:** Count of logins outside business hours  
**Why it matters:** Off-hours activity is suspicious when uncommon for a user.

### 4.4 after_hours_login_rate
**Definition:** after-hours logins / total logins  
**Why it matters:** Strong signal if a user normally logs in only during work hours.

### 4.5 distinct_src_ip_count
**Definition:** Count of distinct `src_ip` per day  
**Why it matters:** Sudden spike may indicate credential use from multiple locations/devices.

### 4.6 mfa_disabled_or_not_used_count
**Definition:** Count of successful logins where MFA was not used  
**Why it matters:** MFA changes or bypass may indicate compromise.

---

## 5. Access & Movement Features

### 5.1 distinct_resources_accessed
**Definition:** Number of distinct `resource` values accessed per day  
**Why it matters:** A sudden spike indicates exploration/lateral movement.

### 5.2 new_resource_access_count
**Definition:** Count of resources accessed for the first time by a user  
**Why it matters:** First-time access to sensitive systems is suspicious.

### 5.3 cross_department_access_count
**Definition:** Access to resources not typically associated with the user’s dept  
**Why it matters:** Indicates lateral movement across teams.

### 5.4 command_event_count
**Definition:** Number of `sys.command` events per day  
**Why it matters:** Spikes in command executions may indicate suspicious activity.

### 5.5 suspicious_command_count (optional enhancement)
**Definition:** Count of commands matching risky patterns  
**Examples:** `cat /etc/passwd`, `sudo`, `ssh admin@...`, `SELECT * FROM payroll`  
**Why it matters:** These commands indicate reconnaissance or abuse.

---

## 6. Data Exfiltration Features (S3 / DB)

### 6.1 s3_get_count
**Definition:** Number of S3 GET operations per day  
**Why it matters:** High volume downloads may indicate exfiltration.

### 6.2 s3_list_count
**Definition:** Number of S3 LIST operations per day  
**Why it matters:** Listing many objects may indicate reconnaissance.

### 6.3 s3_bytes_downloaded
**Definition:** Total bytes read from S3 per user per day  
**Why it matters:** Large values strongly indicate data theft.

### 6.4 s3_high_volume_event_count
**Definition:** Count of S3 events with `bytes > 10MB`  
**Why it matters:** Large single downloads are suspicious.

---

## 7. Privilege & Cloud Activity Features

### 7.1 iam_change_event_count
**Definition:** Count of IAM change events per day  
**Why it matters:** Frequent permission changes are rare and suspicious.

### 7.2 privilege_escalation_flag_count
**Definition:** Count of IAM role changes that grant admin-level roles  
**Why it matters:** Direct insider privilege escalation behavior.

### 7.3 missing_ticket_id_count
**Definition:** IAM changes where `ticket_id` is null/missing  
**Why it matters:** Suggests unauthorized change.

### 7.4 ec2_state_change_count
**Definition:** Count of EC2 stop/start/terminate actions per day  
**Why it matters:** Unexpected changes can indicate sabotage or cover-up.

### 7.5 security_group_update_count
**Definition:** Count of SG updates per day  
**Why it matters:** Risky if changes occur outside normal operations.

### 7.6 sg_open_to_world_flag_count
**Definition:** Count of SG updates allowing `0.0.0.0/0`  
**Why it matters:** Strong indicator of dangerous exposure.

---

## 8. Feature Normalization & Baselines (Conceptual)

Since users have different job roles and activity levels, features will be normalized using:

- Per-user baselines (rolling mean & standard deviation)
- Percentile thresholds per department
- Z-score transformations (optional)

Example:
- User’s after-hours login rate compared to their past 7 days
- Bytes downloaded compared to department average

---

## 9. Output of Feature Engineering

Two main outputs are planned:

### A) Processed Event-Level Dataset
For dashboards and investigation.

### B) User Daily Feature Table
For ML anomaly detection and threat scoring.

---

## Summary

This feature plan transforms raw log events into structured, ML-ready signals.  
It provides the measurable inputs for:

- Anomaly detection models (Phase 4 – Step 4)
- Threat scoring matrix (Phase 4 – Step 5)
- Dashboard visualizations (Phase 5)
