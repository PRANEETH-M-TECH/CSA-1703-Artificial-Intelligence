from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Conflict(Base):
    __tablename__ = "conflicts"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    conflict_type = Column(String, nullable=False)  # overlap | overdue | priority
    task_a_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    task_b_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)

    description = Column(String, nullable=False)
    suggestion = Column(String, default="")
    rule_trace = Column(String, default="")  # JSON-encoded backward-chaining trace

    resolved = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="conflicts")
