# ShadowNet Event Types

This document describes the main categories of events ShadowNet will generate.  
Each category uses the **base fields** plus extra fields inside `metadata`.

---

## 1. Authentication Logs (`auth.*`)

Examples:
- `auth.login`
- `auth.logout`

Used for:
- Normal and suspicious login behavior
- After-hours login anomalies
- Brute-force login attempts

Extra fields in `metadata`:
- `login_result` — `success` or `failure`
- `auth_method` — `password`, `mfa`, `api_key`
- `mfa_used` — `true` or `false`
- `device_id` — optional ID of the device used
- `geo_location` — optional country or city (if you simulate it later)

---

## 2. IAM Change Logs (`iam.*`)

Examples:
- `iam.change_role`
- `iam.attach_policy`
- `iam.detach_policy`

Used for:
- Privilege escalation detection

Extra fields in `metadata`:
- `change_type` — `add_role`, `remove_role`, `attach_policy`, `detach_policy`
- `target_user` — the user whose permissions are being changed
- `old_roles` — list of roles before the change
- `new_roles` — list of roles after the change
- `policy_name` — name of the policy attached/detached (if applicable)
- `requestor` — who initiated the change
- `ticket_id` — optional link to a change request

---

## 3. Command History Logs (`sys.command`)

Examples:
- `sys.command` (each event is one command run on a host)

Used for:
- Lateral movement
- Suspicious commands on servers

Extra fields in `metadata`:
- `host` — hostname or instance ID where the command ran
- `cmd` — the full command string (e.g., `cat /etc/passwd`)
- `exit_code` — numeric result of the command (0 = success)
- `tty` — optional terminal info (if you want to simulate it)

---

## 4. Data Access Logs (`access.*`)

Examples:
- `access.s3`
- `access.db`
- `access.app`

Used for:
- Misuse of S3
- Accessing unusual databases or apps

Extra fields in `metadata`:
- `service` — `s3`, `rds`, `internal_app`, etc.
- `operation` — `GET`, `PUT`, `LIST`, `DELETE`, `SELECT`, `INSERT`, `UPDATE`
- `object_path` — the path to the object or resource (bucket/key, table, URL)
- `bytes` — number of bytes read or written (for downloads/uploads)
- `client_app` — optional, name of the client application

---

## 5. Cloud Resource Logs (`cloud.*`)

Examples:
- `cloud.ec2_state_change`
- `cloud.sg_update`

Used for:
- Misuse of EC2 admin privileges

Extra fields in `metadata`:
- `action` — `start_instance`, `stop_instance`, `terminate_instance`, `modify_sg`
- `instance_id` — EC2 instance ID (for instance actions)
- `security_group_id` — security group being modified
- `old_state` — previous state (e.g., `running`, `stopped`)
- `new_state` — new state (e.g., `stopped`, `terminated`)
- `rule_change` — description of security group rule modified (optional)
