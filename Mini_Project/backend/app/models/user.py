from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    work_start_hour = Column(Integer, default=9)
    work_end_hour = Column(Integer, default=18)

    tasks = relationship("Task", back_populates="owner", cascade="all, delete-orphan")
    schedule_entries = relationship("ScheduleEntry", back_populates="owner", cascade="all, delete-orphan")
    conflicts = relationship("Conflict", back_populates="owner", cascade="all, delete-orphan")
    history = relationship("HistoryRecord", back_populates="owner", cascade="all, delete-orphan")
