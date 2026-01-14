from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SkillBase(BaseModel):
    title: str
<<<<<<< HEAD
    description: str
    category: str
    difficulty_level: str
    price_per_hour: float
=======
    description: Optional[str] = None
    category: str
>>>>>>> 8cabe45 (Created skill.py file to add new new skill)

class SkillCreate(SkillBase):
    pass

class SkillUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
<<<<<<< HEAD
    difficulty_level: Optional[str] = None
    price_per_hour: Optional[float] = None

class Skill(SkillBase):
    id: int
    teacher_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

=======

class SkillResponse(SkillBase):
    id: int
    created_by: int
    created_at: datetime
    
>>>>>>> 8cabe45 (Created skill.py file to add new new skill)
    class Config:
        from_attributes = True