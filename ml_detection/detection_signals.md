# Detection Signals for Insider Threats

This document defines the behavioral signals used by ShadowNet to identify potential insider threats.  
These signals are derived from authentication logs, IAM activity, data access events, and cloud resource usage.

Each signal represents a measurable deviation from normal user behavior and serves as input to anomaly detection and threat scoring.

---

## 1. Authentication-Based Signals

### 1.1 After-Hours Login Signal

**Description:**  
Detects user logins that occur outside normal business hours.

**Why it matters:**  
Malicious insiders and compromised accounts often operate late at night to avoid detection.

**Signal indicators:**
- Login timestamp between **23:00–05:00**
- Sudden shift from normal login schedule
- Multiple after-hours logins within a short time window

**Source fields:**
- `timestamp`
- `event_type = auth.login`

---

### 1.2 Failed Login Burst Signal

**Description:**  
Detects multiple failed login attempts in a short period.

**Why it matters:**  
This may indicate password guessing, brute-force attempts, or credential misuse.

**Signal indicators:**
- 5 or more failed logins within 1 hour
- Failed attempts followed by a successful login

**Source fields:**
- `status = failure`
- `metadata.login_result`

---

## 2. Privilege & Identity Signals

### 2.1 Privilege Escalation Signal

**Description:**  
Detects sudden increases in user permissions.

**Why it matters:**  
Privilege escalation is one of the most dangerous insider actions and often precedes data exfiltration.

**Signal indicators:**
- IAM role change granting admin-level permissions
- `requestor == target_user` (self-escalation)
- Missing approval or `ticket_id`

**Source fields:**
- `event_type = iam.change_role`
- `metadata.new_roles`
- `metadata.requestor`
- `metadata.ticket_id`

---

## 3. Access Pattern Signals

### 3.1 Lateral Movement Signal

**Description:**  
Detects users accessing systems outside their normal department or role.

**Why it matters:**  
Lateral movement is commonly used to explore the environment and reach sensitive systems.

**Signal indicators:**
- Access to many **new resources** in one day
- Cross-department system access
- Sudden spike in distinct hosts or applications accessed

**Source fields:**
- `resource`
- `dept`
- `metadata.host`

---

### 3.2 First-Time Resource Access Signal

**Description:**  
Detects access to a resource a user has never accessed before.

**Why it matters:**  
First-time access to sensitive systems may indicate reconnaissance or misuse.

**Signal indicators:**
- Resource not previously seen for the user
- Combined with off-hours or failed login signals

**Source fields:**
- `user_id`
- `resource`

---

## 4. Data Access & Exfiltration Signals

### 4.1 High-Volume S3 Access Signal

**Description:**  
Detects unusually large data reads from S3 buckets.

**Why it matters:**  
Large downloads may indicate data exfiltration.

**Signal indicators:**
- S3 `GET` or `LIST` operations
- `metadata.bytes > 10 MB`
- Sudden spike in download volume

**Source fields:**
- `event_type = access.s3`
- `metadata.operation`
- `metadata.bytes`

---

## 5. Cloud Infrastructure Signals

### 5.1 EC2 State Change Signal

**Description:**  
Detects unexpected changes to EC2 instances.

**Why it matters:**  
Stopping or terminating instances may disrupt services or hide malicious activity.

**Signal indicators:**
- `stop_instance` or `terminate_instance`
- Actions outside maintenance windows
- Performed by non-admin users

**Source fields:**
- `event_type = cloud.ec2_state_change`
- `metadata.action`
- `metadata.instance_id`

---

### 5.2 Security Group Misconfiguration Signal

**Description:**  
Detects risky security group changes.

**Why it matters:**  
Opening resources to the internet can expose sensitive systems.

**Signal indicators:**
- Security group rules allowing `0.0.0.0/0`
- Sudden rule changes by unexpected users

**Source fields:**
- `event_type = cloud.sg_update`
- `metadata.rule_change`

---

## 6. Signal Combination & Context

Single signals may not always indicate malicious behavior.  
ShadowNet considers **combinations of signals** to increase confidence.

**Examples:**
- After-hours login + failed login burst  
- Privilege escalation + new resource access  
- High-volume S3 access + off-hours activity  

These combined signals will later feed into **threat scoring and anomaly models**.

---

## Summary

Detection signals are the foundation of ShadowNet’s anomaly detection system.  
They convert raw log data into meaningful indicators of insider risk and are used in:

- Feature engineering (Phase 4 – Step 3)
- Anomaly detection models (Phase 4 – Step 4)
- Threat scoring and alerting (Phase 4 – Step 5)
