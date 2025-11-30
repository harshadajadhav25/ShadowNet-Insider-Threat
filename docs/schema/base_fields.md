# ShadowNet Base Event Fields

These fields appear in almost every log event in ShadowNet. Think of them as the "common columns" for your log table.

- `timestamp`  
  - **What it is:** When the event happened  
  - **Format:** ISO-8601 string in UTC (example: `2025-11-29T10:15:30Z`)

- `event_type`  
  - **What it is:** What kind of event this is  
  - **Examples:** `auth.login`, `auth.logout`, `iam.change`, `access.s3`, `sys.command`

- `user_id`  
  - **What it is:** Which user or account performed the action  
  - **Examples:** `emp_001`, `emp_123`, `svc_backup_bot`

- `dept`  
  - **What it is:** The department of the user  
  - **Examples:** `Engineering`, `HR`, `Finance`, `Security`

- `src_ip`  
  - **What it is:** The source IP address where the action came from  
  - **Examples:** `10.0.0.5`, `192.168.1.10`

- `resource`  
  - **What it is:** The main resource being accessed or changed  
  - **Examples:** an S3 bucket name, EC2 instance ID, server hostname, database name

- `status`  
  - **What it is:** Whether the action succeeded or failed  
  - **Examples:** `success`, `failure`

- `metadata`  
  - **What it is:** A nested object that stores extra fields specific to that event type  
  - **Examples:** login method, command string, API operation, bytes transferred
