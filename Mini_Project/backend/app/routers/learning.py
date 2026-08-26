from collections import defaultdict
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, Task, HistoryRecord
from app import schemas
from app.auth import get_current_user
from app.services.ml_model import train_decision_tree, recommend_best_hours

router = APIRouter(tags=["learning"])


def _history_rows(db: Session, user_id: int) -> list[dict]:
    rows = db.query(HistoryRecord).filter(HistoryRecord.owner_id == user_id).all()
    return [
        {
            "task_type": r.task_type,
            "time_of_day": r.time_of_day,
            "planned_duration": r.planned_duration,
            "actual_duration": r.actual_duration,
            "completed_on_time": r.completed_on_time,
        }
        for r in rows
    ]


@router.post("/api/history")
def log_history(payload: schemas.HistoryCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    record = HistoryRecord(owner_id=current_user.id, **payload.model_dump())
    db.add(record)
    if payload.task_id:
        task = db.query(Task).filter(Task.id == payload.task_id, Task.owner_id == current_user.id).first()
        if task:
            task.status = "completed"
    db.commit()
    db.refresh(record)
    return {"ok": True, "id": record.id}


@router.post("/api/model/train")
def train_model(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = _history_rows(db, current_user.id)
    trained = train_decision_tree(rows)
    if trained is None:
        return {"trained": False, "reason": f"Need at least {6} history records; have {len(rows)}.", "n_samples": len(rows)}
    return {"trained": True, "n_samples": trained.n_samples, "accuracy": trained.accuracy, "categories": trained.categories}


@router.get("/api/recommendations", response_model=list[schemas.RecommendationOut])
def get_recommendations(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = _history_rows(db, current_user.id)
    trained = train_decision_tree(rows)
    if trained is None:
        return []
    recs = recommend_best_hours(trained)
    return [schemas.RecommendationOut(**r) for r in recs]


@router.post("/api/recommendations/accept", response_model=schemas.UserOut)
def accept_recommendation(payload: schemas.AcceptRecommendationRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Persists the accepted recommendation as a per-category preferred hour.
    AddEditTask reads this back (via GET /auth/me) and pre-fills a new task's
    deadline hour whenever its category matches — this is how Module 3's
    output actually feeds back into what the user does next, rather than
    the card just being dismissed with no effect.
    """
    preferred = dict(current_user.preferred_hours or {})
    preferred[payload.category] = payload.best_hour
    current_user.preferred_hours = preferred
    db.commit()
    db.refresh(current_user)
    return current_user


@router.get("/api/insights", response_model=schemas.InsightsOut)
def get_insights(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = _history_rows(db, current_user.id)
    tasks = db.query(Task).filter(Task.owner_id == current_user.id).all()

    total_tasks = len(tasks)
    completed_tasks = sum(1 for t in tasks if t.status == "completed")
    overdue_tasks = sum(1 for t in tasks if t.status == "overdue")
    completion_rate = round((completed_tasks / total_tasks) * 100, 1) if total_tasks else 0.0

    by_category = defaultdict(lambda: {"total": 0, "on_time": 0})
    by_hour = defaultdict(lambda: {"total": 0, "on_time": 0})
    for r in rows:
        by_category[r["task_type"]]["total"] += 1
        by_hour[str(r["time_of_day"])]["total"] += 1
        if r["completed_on_time"]:
            by_category[r["task_type"]]["on_time"] += 1
            by_hour[str(r["time_of_day"])]["on_time"] += 1

    by_category_pct = {k: round((v["on_time"] / v["total"]) * 100, 1) for k, v in by_category.items()}
    by_hour_pct = {k: round((v["on_time"] / v["total"]) * 100, 1) for k, v in by_hour.items()}

    trained = train_decision_tree(rows)

    return schemas.InsightsOut(
        total_tasks=total_tasks, completed_tasks=completed_tasks, completion_rate=completion_rate,
        overdue_tasks=overdue_tasks, by_category=by_category_pct, by_hour=by_hour_pct,
        model_accuracy=trained.accuracy if trained else None,
    )
