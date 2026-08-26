from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class HistoryRecord(Base):
    __tablename__ = "history_records"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)

    task_type = Column(String, nullable=False)  # category
    time_of_day = Column(Integer, nullable=False)  # hour 0-23 task was scheduled
    planned_duration = Column(Integer, nullable=False)
    actual_duration = Column(Integer, nullable=False)
    completed_on_time = Column(Boolean, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="history")
