# Insider Threat Event Dictionary

This document defines the specific log events that represent each insider threat scenario modeled in ShadowNet.  
It maps threat behaviors → event types → fields → suspicious patterns.  
This dictionary is used to guide both log generation and later ML detection.

---

# 1. After-hours Login Anomalies

## Related Event Types
- `auth.login`
- `auth.logout`

## Normal Pattern
- Logins between **08:00 and 18:00**
- Occasional failed attempts (1–2)
- Familiar IP addresses for the user

## Suspicious Pattern
- Logins between **23:00 and 05:00**
- 5+ failed logins in a short time window
- Successful login following multiple failures
- Unfamiliar or uncommon source IPs

## Relevant Fields
| Field | Usage |
|-------|--------|
| `timestamp` | Identify off-hours activity |
| `status` | Distinguish failed vs. successful logins |
| `src_ip` | Detect unusual IP patterns |
| `metadata.login_result` | Know login outcome |
| `metadata.mfa_used` | MFA bypass behavior |

## Example Suspicious Event (Conceptual)
```json
{
  "event_type": "auth.login",
  "timestamp": "2025-12-02T02:31:10Z",
  "status": "success",
  "src_ip": "172.16.92.44",
  "metadata": {"login_result": "success"}
}

2. Privilege Escalation
    **Related Event Types**

            1. iam.change_role
            2. iam.attach_policy
            3. iam.detach_policy

    **Normal Pattern**

            1. Admin-driven changes
            2. Ticket/approval ID present
            3. Happens during business hours

    **Suspicious Pattern**

            `. User grants themselves elevated permissions
            (requestor == target_user)
            2. Admin or SecurityAdmin roles added
            3. Change occurs after hours
            4. Missing ticket_id
            5. Followed by access to sensitive resources

Relevent Fields
| Field                              | Description               |
| ---------------------------------- | ------------------------- |
| `metadata.change_type`             | Type of IAM modification  |
| `metadata.target_user`             | Who gained new privileges |
| `metadata.requestor`               | Who initiated the change  |
| `metadata.old_roles` / `new_roles` | Compare privilege levels  |
| `metadata.ticket_id`               | Missing → suspicious      |


3. Lateral Movement Across Systems
    Related Event Types

        1. sys.command
        2. access.app
        3. access.db
        4. auth.login (on many different hosts)

    Normal Pattern

        1. Users access systems primarily assigned to their department
        2. Few distinct hostnames per day

    Suspicious Pattern

        1. Access to new hosts not previously used
        2. Cross-department resource access
        3. Sharp increase in number of systems accessed
        4. Commands executed on unfamiliar machines
        5. Combination with failed logins

Relevant Fields

| Field           | Usage                                          |
| --------------- | ---------------------------------------------- |
| `resource`      | Host/application accessed                      |
| `dept`          | Compare resource ownership vs. user department |
| `metadata.host` | Specific machines involved                     |
| `metadata.cmd`  | Identify sensitive/abnormal commands           |

Example Suspicious Commands

    1. "cat /etc/passwd"
    2. "ssh admin@finance-server"
    3. "SELECT * FROM payroll;"

4. Misuse of S3/EC2 Administrative Privileges

    Related Event Types

        1. access.s3
        2. cloud.ec2_state_change
        3. cloud.sg_update

    Normal Pattern

        1. Predictable S3 reads (backups, reports)
        2. EC2 instance operations during maintenance windows
        3. Security groups rarely modified

    Suspicious Pattern

        1. Large S3 downloads (bytes > 10MB)
        2. High-frequency GET/LIST operations
        3. Sudden EC2 stop/start/terminate actions
        4. Opening ports to the world (0.0.0.0/0)
        5. Rapid repeated modifications of cloud resources

Relevant Fields

| Field                  | Description                 |
| ---------------------- | --------------------------- |
| `metadata.bytes`       | Detect large transfers      |
| `metadata.operation`   | S3 operations like GET/LIST |
| `metadata.action`      | EC2 change type             |
| `metadata.instance_id` | Which instance was affected |
| `metadata.rule_change` | Security group manipulation |

Example Suspicious S3 Access
{
  "event_type": "access.s3",
  "resource": "sensitive-db-backups",
  "metadata": {
    "operation": "GET",
    "bytes": 25000000
  }
}

Summary Table
| Scenario                 | Related Event Types                      | Key Indicators                                |
| ------------------------ | ---------------------------------------- | --------------------------------------------- |
| **After-hours logins**   | `auth.login`                             | Off-hours, failed bursts, new IPs             |
| **Privilege escalation** | `iam.change_role`, `iam.attach_policy`   | New admin roles, no ticket, self-escalation   |
| **Lateral movement**     | `sys.command`, `access.app`, `access.db` | Many new hosts, cross-department access       |
| **S3/EC2 misuse**        | `access.s3`, `cloud.*`                   | Large downloads, EC2 terminations, SG changes |

Purpose of This Dictionary

    This event dictionary serves as:

        1. A guide for log generation: which events to create
        2. A reference for ETL & ML: which features matter
        3. A mapping between scenarios and real log patterns

    It will directly inform:

        1. log_generator.py
        2. Feature engineering
        3. ML anomaly scoring
        4. Dashboard visualizations