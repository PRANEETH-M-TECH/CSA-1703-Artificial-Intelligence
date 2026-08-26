from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field


# ---------- Auth ----------
class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=6)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    work_start_hour: int
    work_end_hour: int
    preferred_hours: dict = {}

    class Config:
        from_attributes = True


class UserSettingsUpdate(BaseModel):
    work_start_hour: Optional[int] = None
    work_end_hour: Optional[int] = None
    name: Optional[str] = None


# ---------- Tasks ----------
class TaskCreate(BaseModel):
    title: str
    category: str = "General"
    deadline: datetime
    duration_minutes: int = 60
    priority: int = 2
    notes: str = ""


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    deadline: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    priority: Optional[int] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class TaskOut(BaseModel):
    id: int
    title: str
    category: str
    deadline: datetime
    duration_minutes: int
    priority: int
    status: str
    notes: str

    class Config:
        from_attributes = True


# ---------- Schedule ----------
class ScheduleEntryOut(BaseModel):
    id: int
    task_id: int
    task_title: str
    category: str
    priority: int
    start_time: datetime
    end_time: datetime
    slack_minutes: float

    class Config:
        from_attributes = True


class ScheduleGenerateResponse(BaseModel):
    entries: List[ScheduleEntryOut]
    unscheduled_task_ids: List[int]
    algorithm: str
    total_lateness_minutes: float


# ---------- Conflicts ----------
class ConflictOut(BaseModel):
    id: int
    conflict_type: str
    task_a_id: Optional[int]
    task_b_id: Optional[int]
    description: str
    suggestion: str
    resolved: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ConflictExplainOut(BaseModel):
    conflict_id: int
    trace: List[str]


class ConflictResolveRequest(BaseModel):
    action: str  # "reschedule" | "shorten" | "drop"


# ---------- Learning ----------
class HistoryCreate(BaseModel):
    task_id: Optional[int] = None
    task_type: str
    time_of_day: int
    planned_duration: int
    actual_duration: int
    completed_on_time: bool


class RecommendationOut(BaseModel):
    category: str
    message: str
    confidence: float
    best_hour: int


class AcceptRecommendationRequest(BaseModel):
    category: str
    best_hour: int


class InsightsOut(BaseModel):
    model_config = {"protected_namespaces": ()}

    total_tasks: int
    completed_tasks: int
    completion_rate: float
    overdue_tasks: int
    by_category: dict
    by_hour: dict
    model_accuracy: Optional[float]
