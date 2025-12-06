# Synthetic Log Specification

This document defines how ShadowNet's synthetic security logs are generated, formatted, and structured. These logs simulate realistic organizational activity as well as suspicious insider behavior.

---

## 1. Log File Format

- **Format:** JSON Lines (`.jsonl`)
- **Encoding:** UTF-8
- **Structure:** One line = one JSON object (one event)
- **Reason:** JSONL is ideal for S3 + Athena because each event is independent.

### Example Filename
logs_2025-12-01.jsonl


### Example Event
```json
{
  "timestamp": "2025-12-01T09:15:22Z",
  "event_type": "auth.login",
  "user_id": "emp_023",
  "dept": "Engineering",
  "src_ip": "10.0.1.25",
  "resource": "vpn_gateway",
  "status": "success",
  "metadata": {
    "login_result": "success",
    "auth_method": "password",
    "mfa_used": true,
    "device_id": "laptop-023"
  }
}

This structure follows the base schema defined in docs/schema/base_fields.md and the event categories defined in docs/schema/event_types.md.

## 2. Daily Log Volume & Frequencies

Each simulated day will generate between 3,000 and 10,000 events.

| Event Type            | Expected Count | Notes                                  |
| --------------------- | -------------- | -------------------------------------- |
| Authentication logs   | 2000–6000      | Normal, failed, and after-hours logins |
| Data access logs      | 500–2000       | S3, DB, internal applications          |
| Command logs          | 50–200         | Engineering & IT users only            |
| IAM change events     | 1–20           | Includes privilege escalation attempts |
| Cloud resource events | 5–50           | EC2 state changes, SG updates, etc.    |

| Event Type            | Expected Count | Notes                                  |
| --------------------- | -------------- | -------------------------------------- |
| Authentication logs   | 2000–6000      | Normal, failed, and after-hours logins |
| Data access logs      | 500–2000       | S3, DB, internal applications          |
| Command logs          | 50–200         | Engineering & IT users only            |
| IAM change events     | 1–20           | Includes privilege escalation attempts |
| Cloud resource events | 5–50           | EC2 state changes, SG updates, etc.    |

These numbers create realistic daily activity volume for an enterprise environment.

3. Behavioral Simulation

ShadowNet models two categories of behavior: normal and suspicious.

A. Normal Behavior (95–98% of events)

Logins during business hours (08:00–18:00)

Resource access aligned with user’s department

Occasional failed logins (1–2 per day)

Small S3 reads/writes (< 5 MB)

Engineers performing a few server commands

Limited number of system interactions per user per day

B. Suspicious Behavior (2–5% of events)

Suspicious behavior corresponds to the Phase 1 insider threat scenarios.

1. After-hours Login Anomalies

Logins between 23:00–05:00

5+ failed login attempts in short time

Successful login after multiple failures

Logins from unusual IP addresses

2. Privilege Escalation

IAM role changes granting elevated permissions

Self-initiated changes (requestor == target_user)

Changes without a valid ticket_id

Escalation followed by new access patterns

3. Lateral Movement

Access to new hosts never accessed before

Interacting across multiple departments’ systems

Engineering-level commands issued from non-engineers

4. Misuse of S3/EC2 Administrative Privileges

High-volume S3 GET/LIST operations (100+)

Large object downloads (bytes > 10MB)

EC2 stop/start/terminate outside maintenance windows

Security group updates exposing ports to 0.0.0.0/0

Suspicious behavior is deliberately rare so anomalies can be detected by ML later.

4. File Naming Convention

Logs are generated once per simulated day.

logs_YYYY-MM-DD.jsonl


Examples:

logs_2025-12-01.jsonl
logs_2025-12-02.jsonl


This format aligns with future S3 partitioning:

s3://shadownet-raw/year=2025/month=12/day=01/logs.jsonl

5. Log Generation Inputs

The synthetic generator uses structured inputs to create realistic patterns.

👥 Users

50–100 synthetic employees

Each user has:

user_id

name

dept

normal login hours (08:00–18:00)

🏢 Departments

Engineering

HR

Finance

IT

Security

🗂 Department-Specific Resources
Department	Example Resources
Engineering	app servers, CI/CD, code repo
HR	HR portal, HR SQL database
Finance	financial DB, BI dashboards
IT/Security	VPN gateway, admin servers, S3 backup buckets

Resources determine normal access patterns and help detect anomalies.

6. Output Destination

All generated logs are saved locally in:

data/


Examples:

data/logs_2025-12-01.jsonl

data/logs_2025-12-02.jsonl

These files will later be uploaded to AWS S3 in Phase 3.

7. How Suspicious Events Are Injected

The generator injects anomalies by modifying:

timestamps → simulate after-hours login

IAM role assignments → privilege escalation

resource set → lateral movement

S3 request volume/size → S3 misuse

EC2 state changes → cloud resource misuse

Suspicious events appear as small but noticeable deviations from normal patterns.

