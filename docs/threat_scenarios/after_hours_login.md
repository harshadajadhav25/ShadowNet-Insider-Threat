# Scenario: After-hours Login Anomalies

## What this scenario is

Users log in at unusual times compared to their normal work pattern (for example, many logins late at night or early in the morning). These can indicate compromised accounts or insiders trying to avoid detection.

## Why this is dangerous

Malicious users may prefer off-hours when fewer people are monitoring systems. They may:
- Try passwords repeatedly (brute-force)
- Access sensitive systems while fewer alerts are actively monitored

## Primary signals we want to detect

- Logins outside normal business hours (for example, 08:00–18:00 local time)
- Sudden change in a user’s typical login time
- Many failed login attempts followed by a success
- Logins from unusual IP addresses during off-hours

## Example log types involved

- **Authentication logs** — login_success, login_failed events
- **MFA logs** — whether multi-factor authentication was used or bypassed
- **Device/IP logs** — information about where the login came from

## Normal vs suspicious behavior

**Normal:**
- User logs in during their usual shift hours
- Occasional off-hours login with a valid reason (maintenance, emergencies)

**Suspicious:**
- Bursts of failed logins between 23:00–03:00
- Off-hours login from an IP or location not previously seen
- Off-hours login followed by access to sensitive resources

## Metrics / KPIs to compute later

- After-hours login rate per user
- Count of failed logins in 1-hour windows
- Ratio of off-hours logins to normal-hours logins
- Number of distinct IPs seen for a user in a short period
