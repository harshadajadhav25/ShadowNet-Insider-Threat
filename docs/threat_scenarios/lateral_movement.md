# Scenario: Lateral Movement Across Systems

## What this scenario is

A user or attacker moves from one system to another, expanding their access. Instead of only using one machine or one service, they start touching many systems, especially those outside their normal department or role.

## Why this is dangerous

Lateral movement is a common step in attacks:
- An attacker compromises one machine or account
- Then uses it to pivot into more sensitive systems
- Eventually reaches critical data or admin interfaces

## Primary signals we want to detect

- A user accessing hosts, databases, or services they never touched before
- Access to systems outside their normal department (for example, HR data accessed by an engineer)
- Rapid increase in the number of distinct systems a user interacts with

## Example log types involved

- **System/host access logs** — SSH, RDP, or other remote access events
- **Application access logs** — user actions inside applications
- **Database access logs** — queries against new or sensitive databases

## Normal vs suspicious behavior

**Normal:**
- Access mainly to systems aligned with the user’s role/team
- Occasional cross-team access with known reasons (troubleshooting, collaboration)

**Suspicious:**
- Sudden spike in the number of systems accessed
- Access to systems owned by unrelated departments
- Lateral movement combined with failed logins on sensitive systems

## Metrics / KPIs to compute later

- Number of unique systems accessed per user per day
- Number of cross-department resource accesses
- First-time access events to sensitive systems
- Growth rate of “new systems accessed” over time
