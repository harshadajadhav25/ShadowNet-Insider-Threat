# Scenario: Privilege Escalation

## What this scenario is

A normal employee account (for example, a developer or analyst) suddenly gains elevated or admin-level permissions. This can allow them to access or modify resources they normally should not touch.

## Why this is dangerous

If an attacker or malicious insider escalates their privileges, they can:
- Read or exfiltrate sensitive data
- Modify security settings
- Create backdoor accounts or access keys

## Primary signals we want to detect

- IAM role changes that give a user new high-privilege roles
- New policies attached that include powerful permissions (like full access to S3 or EC2)
- Privilege changes happening outside normal business hours
- Privilege changes without a corresponding ticket or approval record

## Example log types involved

- **IAM change logs** — who changed which roles/policies
- **Authentication logs** — logins from the upgraded account
- **Data access logs** — new access to sensitive resources after escalation

## Normal vs suspicious behavior

**Normal:**
- Role changes requested by managers or admins
- Changes that match a ticket or change request
- Changes that happen during business hours

**Suspicious:**
- A user changes their own role to admin
- Privileges increased without a known ticket
- Multiple privilege changes in a short time window
- Changes followed by unusual data access activity

## Metrics / KPIs to compute later

- Number of high-privilege role assignments per day
- Number of self-initiated privilege changes
- Privilege changes without linked ticket/approval
- First-time access to sensitive resources after a role change
