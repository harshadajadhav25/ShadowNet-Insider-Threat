# Log Automation Workflow

This document describes how ShadowNet's synthetic logs are generated on a recurring basis.  
The goal is to simulate continuous, daily security activity that can be ingested into the data pipeline.

---

## 1. High-level Workflow

At a high level, the log automation process is:

1. **Scheduler triggers the Python script once per day**
2. **`log_generator.py` generates a new JSONL log file for that date**
3. **The file is saved under `data/` with a date-based filename**
4. *(Future phase)* The file is uploaded to an S3 bucket and partitioned by date

### Text-based Flow

```text
Scheduler (cron / Task Scheduler / manual run)
        ↓
Python environment (.venv) + log_generator.py
        ↓
Generate events for target date
        ↓
Write to data/logs_YYYY-MM-DD.jsonl
        ↓
(Future) Upload to S3: s3://shadownet-raw/year=YYYY/month=MM/day=DD/logs.jsonl

2. Log Generation Script

    The main script responsible for creating logs is:
        log_generator/log_generator.py

    Core responsibilities:
        1. Load or generate a list of synthetic users
        2. For a given day, generate:
            Normal login events
            Failed login events
            After-hours login anomalies
        3. Write all events to a JSON Lines file in the data/ folder:
            data/logs_YYYY-MM-DD.jsonl

    Currently, the script uses the current UTC date when run:

    if __name__ == "__main__":
        today = datetime.utcnow()
        events = generate_day_logs(today, num_events=1000)
        write_events_to_file(events, today)

3. File Naming and Location

    Each time the script runs, it creates one file:

    data/logs_YYYY-MM-DD.jsonl


    Examples:

        data/logs_2025-12-01.jsonl

        data/logs_2025-12-02.jsonl

    This pattern makes it easy to:

        Upload files into S3 partitions (by year/month/day)
        Query logs per day in Athena
        Keep a clear history of simulated days

4. Manual Execution (Development Mode)

    During development, logs can be generated manually from the command line.

    From the project root:

    # Activate virtual environment first
    # Windows (PowerShell):
    .venv\Scripts\Activate.ps1

    # or Windows (CMD):
    .venv\Scripts\activate.bat

    # or Mac/Linux:
    source .venv/bin/activate

    # Then run the generator:
    python log_generator/log_generator.py


    Output:

        A message like Wrote 1000 events to data/logs_2025-12-01.jsonl
        A new JSONL file under data/
        This manual mode is useful for testing and debugging.

5. Daily Automation Examples

    In a real environment, the generator would be scheduled to run once per day.

    Below are two common approaches:

    5.1 Linux / Mac: cron Job

    Example cron entry to run the generator every day at 01:00:

        0 1 * * * /usr/bin/python /path/to/ShadowNet-Insider-Threat/log_generator/log_generator.py


    Explanation:

        0 1 * * * → at 01:00 every day
        /usr/bin/python → system Python interpreter
        The script will generate a new log file for the current date

    5.2 Windows: Task Scheduler (Conceptual)

        On Windows, Task Scheduler can be used:

        1. Open Task Scheduler
        2. Create Basic Task
        3. Trigger: Daily at a specified time
        4. Action: Start a program

            a. Program/script: python
            b. Arguments: C:\path\to\ShadowNet-Insider-Threat\log_generator\log_generator.py
            c. Start in: C:\path\to\ShadowNet-Insider-Threat

        This will run the script daily without manual intervention.

6. Future Extension: Upload to S3

    In a later phase, an additional step will be added:

    1. Generate the daily log file (as above)

    2. Upload it to an S3 bucket, for example:

        s3://shadownet-raw/year=YYYY/month=MM/day=DD/logs.jsonl


    This can be done using:

        AWS CLI (e.g., aws s3 cp data/logs_YYYY-MM-DD.jsonl s3://...)
        Or a Python script using boto3

    This upload step is not required for Phase 2, but the workflow is designed to support it.

7. Summary

    1. The scheduler (cron/Task Scheduler/manual) controls when logs are generated
    2. The Python script (log_generator.py) creates realistic daily security logs
    3. Files are stored under data/ using a date-based naming pattern
    4. This process simulates continuous security logging, which feeds into later ETL and ML stages in ShadowNet