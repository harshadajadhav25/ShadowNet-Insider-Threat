# Threat Scoring Matrix

This document defines ShadowNet’s threat scoring system.  
The goal is to convert detection signals and anomaly model outputs into an easy-to-understand **risk score** and **severity level**.

ShadowNet assigns points to suspicious signals. The total points determine severity:
- **Low**
- **Medium**
- **High**
- **Critical**

---

## 1. Why a Scoring Matrix?

An anomaly model may output a score, but security teams need:

- Clear severity labels (Low/Medium/High/Critical)
- Explainable reasons behind each alert
- Consistent prioritization for investigation

This scoring matrix provides an interpretable decision layer on top of:
- Rules
- Feature anomalies
- ML anomaly score

---

## 2. Scoring Rules (Points Per Signal)

Each signal contributes points.

### 2.1 Authentication Signals

| Signal | Condition (Example) | Points |
|--------|----------------------|--------|
| After-hours login | after_hours_login_count ≥ 1 | +2 |
| Repeated after-hours logins | after_hours_login_count ≥ 3 | +3 |
| Failed login burst | failed_login_count ≥ 5/day | +3 |
| Failed then success | failed_login_count ≥ 5 AND success login exists | +2 |
| Many source IPs | distinct_src_ip_count ≥ 3/day | +2 |

---

### 2.2 Privilege Signals (High Risk)

| Signal | Condition (Example) | Points |
|--------|----------------------|--------|
| IAM change detected | iam_change_event_count ≥ 1 | +3 |
| Privilege escalation | priv_escalation_flag_count ≥ 1 | +6 |
| Missing ticket/approval | missing_ticket_id_count ≥ 1 | +3 |
| Self-escalation | requestor == target_user | +4 |

---

### 2.3 Lateral Movement / Access Signals

| Signal | Condition (Example) | Points |
|--------|----------------------|--------|
| Spike in distinct resources | distinct_resources_accessed ≥ 10/day | +3 |
| New resource access | new_resource_access_count ≥ 5/day | +2 |
| Cross-department access | cross_department_access_count ≥ 3/day | +3 |
| High command activity | command_event_count ≥ 20/day | +3 |

---

### 2.4 Data Exfiltration Signals (S3 / Data)

| Signal | Condition (Example) | Points |
|--------|----------------------|--------|
| High S3 download total | s3_bytes_downloaded > 50MB/day | +4 |
| Very high S3 download | s3_bytes_downloaded > 200MB/day | +6 |
| High-volume single event | s3_high_volume_event_count ≥ 1 | +3 |
| Many S3 GET/LIST operations | s3_get_count + s3_list_count ≥ 50/day | +3 |

---

### 2.5 Cloud Infrastructure Signals

| Signal | Condition (Example) | Points |
|--------|----------------------|--------|
| EC2 state changes | ec2_state_change_count ≥ 3/day | +3 |
| Stop/terminate events | metadata.action in (stop, terminate) | +4 |
| Security group update | security_group_update_count ≥ 1 | +4 |
| SG open to world | sg_open_to_world_flag_count ≥ 1 | +7 |

---

## 3. ML Anomaly Score Contribution (Optional)

If an anomaly model (e.g., Isolation Forest) is used:

| Model Score Range (Example) | Points |
|-----------------------------|--------|
| Medium anomaly score | +2 |
| High anomaly score | +4 |
| Extreme anomaly score | +6 |

This allows the model to increase risk even when a single rule is not triggered.

---

## 4. Severity Thresholds

Total risk score determines severity.

| Total Score | Severity |
|-------------|----------|
| 0–3 | Low |
| 4–7 | Medium |
| 8–12 | High |
| 13+ | Critical |

---

## 5. Example Scoring Scenarios

### Example A — After-hours + Failed Burst
- after-hours login (+2)
- failed login burst (+3)

Total = 5 → **Medium**

---

### Example B — Privilege Escalation + New Access
- privilege escalation (+6)
- missing ticket (+3)
- new resources (+2)

Total = 11 → **High**

---

### Example C — Exfiltration + Privilege Escalation
- privilege escalation (+6)
- high S3 download (+4)
- high-volume event (+3)

Total = 13 → **Critical**

---

## 6. Output Fields

When scoring is computed, ShadowNet will output:

- `risk_score` (numeric)
- `severity` (Low/Medium/High/Critical)
- `reasons` (list of triggered signals/rules)

Example:

```json
{
  "user_id": "emp_023",
  "event_date": "2025-12-02",
  "risk_score": 13,
  "severity": "Critical",
  "reasons": [
    "Privilege escalation detected",
    "High-volume S3 download",
    "After-hours login activity"
  ]
}
