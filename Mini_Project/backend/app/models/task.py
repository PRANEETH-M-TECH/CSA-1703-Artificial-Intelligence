from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    title = Column(String, nullable=False)
    category = Column(String, default="General")
    deadline = Column(DateTime(timezone=True), nullable=False)
    duration_minutes = Column(Integer, nullable=False, default=60)
    priority = Column(Integer, default=2)  # 1=Low 2=Medium 3=High
    status = Column(String, default="pending")  # pending | scheduled | completed | overdue
    notes = Column(String, default="")

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="tasks")
    schedule_entry = relationship("ScheduleEntry", back_populates="task", uselist=False, cascade="all, delete-orphan")
