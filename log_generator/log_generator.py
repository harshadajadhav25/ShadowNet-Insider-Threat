import random
import json
from datetime import datetime, timedelta
from pathlib import Path

from faker import Faker

fake = Faker()

# Where to save logs
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

# Simple departments to use
DEPARTMENTS = ["Engineering", "HR", "Finance", "Security", "IT"]


def generate_users(num_users: int = 50):
    """
    Create a list of fake users with departments and normal login hours.
    """
    users = []
    for i in range(num_users):
        user_id = f"emp_{i:03d}"  # emp_000, emp_001, ...
        dept = random.choice(DEPARTMENTS)
        users.append(
            {
                "user_id": user_id,
                "name": fake.name(),
                "dept": dept,
                # Normal login window (8 AM to 6 PM)
                "normal_login_start": 8,
                "normal_login_end": 18,
            }
        )
    return users


def random_time_in_day(date: datetime, start_hour: int, end_hour: int) -> datetime:
    """
    Return a random datetime within a given day and hour range.
    """
    base = datetime(date.year, date.month, date.day, start_hour, 0, 0)
    end = datetime(date.year, date.month, date.day, end_hour, 59, 59)
    total_seconds = int((end - base).total_seconds())
    offset = random.randint(0, total_seconds)
    return base + timedelta(seconds=offset)


def make_auth_event(user: dict, date: datetime, *, after_hours=False, failed=False) -> dict:
    """
    Generate a single auth.login event for a given user on a given date.
    """
    if after_hours:
        # After-hours window: 23:00–23:59 (simple version)
        event_time = random_time_in_day(date, 23, 23)
    else:
        # Normal working hours: user-specific window (here all users share 8–18)
        event_time = random_time_in_day(
            date,
            user["normal_login_start"],
            user["normal_login_end"],
        )

    success = not failed
    status = "success" if success else "failure"

    event = {
        "timestamp": event_time.isoformat() + "Z",
        "event_type": "auth.login",
        "user_id": user["user_id"],
        "dept": user["dept"],
        "src_ip": fake.ipv4_private(),
        "resource": "vpn_gateway",
        "status": status,
        "metadata": {
            "login_result": status,
            "auth_method": "password",
            "mfa_used": success and random.random() < 0.8,
            "device_id": f"laptop-{user['user_id']}",
        },
    }
    return event


def generate_day_logs(target_date: datetime, num_events: int = 1000):
    """
    Generate a list of auth.login events for a single simulated day.
    Mix of:
      - normal logins
      - failed logins
      - some after-hours logins (suspicious)
    """
    users = generate_users()
    events = []

    # Probabilities for different types of auth events
    event_kinds = ["normal_login", "failed_login", "after_hours_login"]
    weights = [0.75, 0.15, 0.10]  # 75% normal, 15% failed, 10% after-hours

    for _ in range(num_events):
        user = random.choice(users)
        kind = random.choices(event_kinds, weights=weights, k=1)[0]

        if kind == "normal_login":
            events.append(make_auth_event(user, target_date, after_hours=False, failed=False))
        elif kind == "failed_login":
            events.append(make_auth_event(user, target_date, after_hours=False, failed=True))
        elif kind == "after_hours_login":
            events.append(make_auth_event(user, target_date, after_hours=True, failed=False))

    return events


def write_events_to_file(events: list, date: datetime):
    """
    Write events to data/logs_YYYY-MM-DD.jsonl (JSON Lines format).
    """
    filename = DATA_DIR / f"logs_{date.date()}.jsonl"
    with filename.open("w", encoding="utf-8") as f:
        for event in events:
            f.write(json.dumps(event) + "\n")

    print(f"Wrote {len(events)} events to {filename}")


if __name__ == "__main__":
    # Generate logs for "today" in UTC
    today = datetime.utcnow()
    events = generate_day_logs(today, num_events=1000)
    write_events_to_file(events, today)
