from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SkillBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: str

class SkillCreate(SkillBase):
    pass

class SkillUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None

class Skill(SkillBase):
    id: int
    created_by: int
    created_at: datetime

    class Config:
        from_attributes = True
