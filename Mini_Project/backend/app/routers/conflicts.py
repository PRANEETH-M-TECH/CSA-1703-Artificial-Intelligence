import json
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, Task, ScheduleEntry, Conflict
from app import schemas
from app.auth import get_current_user
from app.services.rules_engine import forward_chain, backward_chain_explain

router = APIRouter(prefix="/api/conflicts", tags=["conflicts"])


@router.post("/check", response_model=list[schemas.ConflictOut])
def check_conflicts(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    entries = db.query(ScheduleEntry).filter(ScheduleEntry.owner_id == current_user.id).all()
    tasks = db.query(Task).filter(Task.owner_id == current_user.id).all()
    tasks_by_id = {t.id: t for t in tasks}

    detected = forward_chain(entries, tasks_by_id, now=datetime.utcnow())

    db.query(Conflict).filter(Conflict.owner_id == current_user.id, Conflict.resolved == False).delete()  # noqa: E712

    out = []
    for d in detected:
        c = Conflict(
            owner_id=current_user.id, conflict_type=d.conflict_type,
            task_a_id=d.task_a_id, task_b_id=d.task_b_id,
            description=d.description, suggestion=d.suggestion,
            rule_trace=json.dumps(d.trace), resolved=False,
        )
        db.add(c)
        db.flush()
        out.append(c)
    db.commit()
    for c in out:
        db.refresh(c)
    return out


@router.get("", response_model=list[schemas.ConflictOut])
def list_conflicts(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Conflict).filter(Conflict.owner_id == current_user.id, Conflict.resolved == False).order_by(Conflict.created_at.desc()).all()  # noqa: E712


@router.get("/{conflict_id}/explain", response_model=schemas.ConflictExplainOut)
def explain_conflict(conflict_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    conflict = db.query(Conflict).filter(Conflict.id == conflict_id, Conflict.owner_id == current_user.id).first()
    if not conflict:
        raise HTTPException(status_code=404, detail="Conflict not found")
    tasks_by_id = {t.id: t for t in db.query(Task).filter(Task.owner_id == current_user.id).all()}
    trace = backward_chain_explain(conflict, tasks_by_id)
    return schemas.ConflictExplainOut(conflict_id=conflict.id, trace=trace)


@router.post("/{conflict_id}/resolve", response_model=schemas.ConflictOut)
def resolve_conflict(conflict_id: int, payload: schemas.ConflictResolveRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    conflict = db.query(Conflict).filter(Conflict.id == conflict_id, Conflict.owner_id == current_user.id).first()
    if not conflict:
        raise HTTPException(status_code=404, detail="Conflict not found")

    target_task_id = conflict.task_b_id or conflict.task_a_id
    task = db.query(Task).filter(Task.id == target_task_id).first() if target_task_id else None

    if task:
        if payload.action == "shorten":
            task.duration_minutes = max(15, int(task.duration_minutes * 0.6))
            task.status = "pending"
        elif payload.action == "drop":
            task.status = "pending"
            db.query(ScheduleEntry).filter(ScheduleEntry.task_id == task.id).delete()
        else:  # reschedule
            task.status = "pending"
            db.query(ScheduleEntry).filter(ScheduleEntry.task_id == task.id).delete()

    conflict.resolved = True
    db.commit()
    db.refresh(conflict)
    return conflict
