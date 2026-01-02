# Anomaly Detection Models (ML + Rule-Based)

This document describes the detection approaches ShadowNet will use to identify insider threats from engineered features.  
Because insider threats are rare and labels are usually unavailable, ShadowNet primarily uses **unsupervised anomaly detection** along with **rule-based checks**.

---

## 1. Why Unsupervised Detection?

In most real organizations:

- Insider threat events are rare
- Ground-truth labels are limited or missing
- User behavior varies by role and department

Therefore, ShadowNet focuses on detecting **behavioral outliers** rather than training a supervised classifier.

---

## 2. Detection Approaches Used in ShadowNet

ShadowNet uses a layered strategy:

1. **Rule-based detection (high confidence rules)**
2. **Unsupervised ML anomaly detection**
3. **Hybrid scoring (combine ML score + rules for severity)**

This improves explainability and helps reduce false positives.

---

## 3. Rule-Based Detection (Baseline)

### 3.1 Purpose
Rules catch obvious suspicious behavior with simple thresholds.

Rules are easy to explain and make dashboards actionable.

### 3.2 Example Rules

| Rule | Logic | Why it matters |
|------|------|----------------|
| Failed login burst | failed_login_count ≥ 5 in 1 hour | Brute-force / misuse |
| After-hours logins | after_hours_login_count ≥ 3/day | Unusual work time |
| High S3 download | s3_bytes_downloaded > 50MB/day | Possible exfiltration |
| Privilege escalation | priv_escalation_flag_count ≥ 1 | Very high risk |
| SG open to world | sg_open_to_world_flag_count ≥ 1 | Critical exposure |

### 3.3 Rule Output
Rules produce:
- `rule_alert = true/false`
- `rule_type` (which rule triggered)
- `rule_severity` (low/medium/high/critical)

---

## 4. Unsupervised Anomaly Detection Models

Unsupervised models assign an anomaly score to each user-day row.

Input: user daily feature table from `feature_engineering.md`

Example features:
- failed_login_count
- after_hours_login_rate
- distinct_resources_accessed
- s3_bytes_downloaded
- iam_change_event_count

---

### 4.1 Isolation Forest (Primary Model)

**Why this model:**  
Isolation Forest works well for detecting rare outliers in mixed numeric features and is commonly used for anomaly detection.

**Concept:**  
It isolates anomalies faster because they are easier to separate in random decision trees.

**Output:**
- `anomaly_score` per user-day
- Higher score = more suspicious

**Good for:**
- Rare spikes in activity
- Users behaving very differently than normal population

---

### 4.2 Local Outlier Factor (Optional Model)

**Why it helps:**  
LOF detects anomalies based on **local neighborhood density**, which helps when behavior differs by department.

**Output:**
- Outlier score per user-day based on nearest neighbors

**Good for:**
- Detecting anomalies within a department/peer group

---

### 4.3 Clustering-Based Detection (Optional Model)

**Approach:**
- Cluster user-day behavior using KMeans or DBSCAN
- Points far from cluster centers or in tiny clusters can be anomalies

**Good for:**
- Grouping similar users (peer-based analysis)

---

## 5. Model Training Strategy (ShadowNet)

Because this is a simulation project, training is done on:

- “Mostly normal” days
- With a small percentage of injected anomalies (2–5%)

Training process:

1. Prepare feature table
2. Normalize numeric features
3. Fit model on historical days (baseline)
4. Score new day of activity

---

## 6. Output Fields from Detection

ShadowNet will produce these outputs:

| Output Field | Description |
|-------------|-------------|
| anomaly_score | ML-based anomaly score |
| anomaly_label | normal / suspicious (based on threshold) |
| triggered_rules | list of triggered rules (if any) |
| final_risk_score | combined score for severity |

---

## 7. Combining ML + Rules (Hybrid Logic)

ShadowNet uses a hybrid scoring strategy:

1. Compute ML anomaly score
2. Check rule-based triggers
3. Combine into a final severity score

Example logic:

- If privilege escalation rule triggers → severity is at least HIGH
- If anomaly_score is high + after-hours logins → HIGH
- If only small anomalies → MEDIUM

This makes alerts both **detectable** and **explainable**.

---

## 8. Evaluation Plan (Conceptual)

Since we generate synthetic anomalies, evaluation can be done by:

- Checking if injected anomalies appear in top scored users
- Comparing false positives on normal days
- Reviewing top anomaly examples manually

---

## Summary

ShadowNet anomaly detection is designed to be:

- **Realistic:** reflects how real orgs detect insider threats
- **Explainable:** rules + interpretable features
- **Flexible:** supports multiple models (Isolation Forest primary)
- **Actionable:** outputs final risk scores for dashboards and reports
