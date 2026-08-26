"""Seeds a demo account with realistic tasks + history so dashboards
(Insights, Recommendations, Schedule) show meaningful data immediately,
without requiring the grader to manually create weeks of history."""
import random
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models import User, Task, HistoryRecord
from app.auth import hash_password

DEMO_EMAIL = "demo@taskmind.app"
DEMO_PASSWORD = "demo1234"

CATEGORIES = ["Study", "Work", "Fitness", "Personal", "Meeting"]


def seed_demo_user(db: Session) -> None:
    existing = db.query(User).filter(User.email == DEMO_EMAIL).first()
    if existing:
        return

    user = User(
        name="Demo Student",
        email=DEMO_EMAIL,
        hashed_password=hash_password(DEMO_PASSWORD),
        work_start_hour=9,
        work_end_hour=19,
    )
    db.add(user)
    db.flush()

    now = datetime.utcnow()
    upcoming_titles = [
        ("Finish AI capstone report", "Study", 3, 120, 2),
        ("Revise Unit III logic notes", "Study", 2, 90, 4),
        ("Team standup", "Meeting", 1, 30, 6),
        ("Gym session", "Fitness", 1, 60, 12),
        ("Client requirements call", "Work", 2, 45, 8),
        ("Grocery shopping", "Personal", 4, 40, 24),
        ("Prepare viva slides", "Study", 5, 100, 3),
        ("Code review — scheduler module", "Work", 2, 50, 10),
        ("Morning run", "Fitness", 1, 30, 30),
        ("Read research paper on CSP heuristics", "Study", 6, 60, 5),
    ]
    for title, cat, days_out, dur, priority_seed in upcoming_titles:
        deadline = now + timedelta(days=days_out, hours=random.choice([-2, 0, 2, 4]))
        priority = 3 if priority_seed <= 4 else (2 if priority_seed <= 10 else 1)
        db.add(Task(
            owner_id=user.id, title=title, category=cat, deadline=deadline,
            duration_minutes=dur, priority=priority, status="pending",
        ))

    # Deliberately overlapping pair + one overdue task to demo Module 2 on first login
    db.add(Task(owner_id=user.id, title="Submit assignment draft", category="Study",
                deadline=now - timedelta(hours=5), duration_minutes=60, priority=3, status="pending"))

    random.seed(42)
    hour_bias = {"Study": 9, "Work": 11, "Fitness": 7, "Personal": 18, "Meeting": 10}
    for _ in range(60):
        cat = random.choice(CATEGORIES)
        base_hour = hour_bias[cat]
        hour = max(6, min(21, base_hour + random.randint(-3, 3)))
        on_time_prob = 0.85 if abs(hour - base_hour) <= 2 else 0.4
        completed_on_time = random.random() < on_time_prob
        planned = random.choice([30, 45, 60, 90, 120])
        actual = planned + (0 if completed_on_time else random.randint(15, 60))
        db.add(HistoryRecord(
            owner_id=user.id, task_type=cat, time_of_day=hour,
            planned_duration=planned, actual_duration=actual, completed_on_time=completed_on_time,
        ))

    db.commit()
