# Scenario: Misuse of S3/EC2 Administrative Privileges

## What this scenario is

An admin or privileged user misuses their power on AWS resources like S3 buckets and EC2 instances. This may include unusual data downloads, instance changes, or security group modifications.

## Why this is dangerous

Misuse of cloud privileges can lead to:
- Data exfiltration (copying large amounts of data from S3)
- Service disruption (stopping or terminating critical EC2 instances)
- Creating backdoors or unauthorized instances
- Making private data publicly accessible

## Primary signals we want to detect

- Large or unusual S3 data access
- New public access settings on private S3 buckets
- Starting/stopping/terminating EC2 instances unexpectedly
- Security group changes that open risky ports

## Example log types involved

- **S3 access logs** — GET, PUT, LIST, DELETE operations
- **CloudTrail logs** — API calls for EC2 and IAM actions
- **EC2 activity logs** — instance state changes and security group updates

## Normal vs suspicious behavior

**Normal:**
- Regular, scheduled maintenance
- Expected data processing operations
- Known backup patterns

**Suspicious:**
- Downloading entire S3 buckets
- Changing bucket policies to public-read
- Stopping/terminating EC2 instances outside maintenance windows
- Modifying security groups to allow 0.0.0.0/0 (open to world)

## Metrics / KPIs to compute later

- Total S3 bytes read per user per day
- Number of S3 objects listed or downloaded in short time
- Number of EC2 state changes per user
- Count of security group rule changes
