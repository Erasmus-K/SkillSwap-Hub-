from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SessionBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    max_participants: int = 1

class SessionCreate(SessionBase):
    skill_id: int

class SessionUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    max_participants: Optional[int] = None
    is_active: Optional[bool] = None

class Session(SessionBase):
    id: int
    skill_id: int
    teacher_id: int
    meet_link: Optional[str] = None
    calendar_event_id: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True