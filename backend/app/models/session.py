from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..db.session import Base

class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    max_participants = Column(Integer, default=1)
    meet_link = Column(String)
    calendar_event_id = Column(String)
    is_active = Column(Boolean, default=True)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    skill = relationship("Skill", back_populates="sessions")
    teacher = relationship("User", back_populates="sessions")
    bookings = relationship("Booking", back_populates="session")