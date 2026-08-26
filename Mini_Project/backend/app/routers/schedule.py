from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, Task, ScheduleEntry
from app import schemas
from app.auth import get_current_user
from app.services.scheduler import generate_schedule, SchedulableTask

router = APIRouter(prefix="/api/schedule", tags=["schedule"])


def _entry_out(e: ScheduleEntry, task_title: str, category: str, priority: int) -> schemas.ScheduleEntryOut:
    return schemas.ScheduleEntryOut(
        id=e.id, task_id=e.task_id, task_title=task_title, category=category, priority=priority,
        start_time=e.start_time, end_time=e.end_time, slack_minutes=e.slack_minutes,
    )


@router.post("/generate", response_model=schemas.ScheduleGenerateResponse)
def generate(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tasks = db.query(Task).filter(Task.owner_id == current_user.id, Task.status != "completed").all()
    schedulable = [
        SchedulableTask(id=t.id, title=t.title, category=t.category, priority=t.priority,
                         duration_minutes=t.duration_minutes, deadline=t.deadline)
        for t in tasks
    ]

    placed, unscheduled_ids, total_lateness = generate_schedule(
        schedulable, now=datetime.utcnow(),
        work_start_hour=current_user.work_start_hour, work_end_hour=current_user.work_end_hour,
    )

    db.query(ScheduleEntry).filter(ScheduleEntry.owner_id == current_user.id).delete()
    db.query(Task).filter(Task.owner_id == current_user.id, Task.status == "scheduled").update({"status": "pending"})

    entries_out = []
    for p in placed:
        entry = ScheduleEntry(owner_id=current_user.id, task_id=p.task_id, start_time=p.start_time,
                               end_time=p.end_time, slack_minutes=p.slack_minutes)
        db.add(entry)
        db.flush()
        task = db.query(Task).filter(Task.id == p.task_id).first()
        if task:
            task.status = "scheduled"
        entries_out.append(_entry_out(entry, p.task_title, p.category, p.priority))

    db.commit()

    return schemas.ScheduleGenerateResponse(
        entries=entries_out, unscheduled_task_ids=unscheduled_ids,
        algorithm="CSP domain generation + A* search (g=lateness minutes, h=time-from-now tie-break)",
        total_lateness_minutes=total_lateness,
    )


@router.get("", response_model=list[schemas.ScheduleEntryOut])
def get_schedule(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    entries = db.query(ScheduleEntry).filter(ScheduleEntry.owner_id == current_user.id).order_by(ScheduleEntry.start_time).all()
    out = []
    for e in entries:
        task = db.query(Task).filter(Task.id == e.task_id).first()
        if task:
            out.append(_entry_out(e, task.title, task.category, task.priority))
    return out
