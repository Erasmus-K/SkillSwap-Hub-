from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SkillBase(BaseModel):
    title: str
    description: str
    category: str
    difficulty_level: str
    price_per_hour: float

class SkillCreate(SkillBase):
    pass

class SkillUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    difficulty_level: Optional[str] = None
    price_per_hour: Optional[float] = None

class Skill(SkillBase):
    id: int
    teacher_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True