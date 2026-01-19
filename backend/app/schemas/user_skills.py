from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class SkillTagBase(BaseModel):
    name: str
    category: str
    description: Optional[str] = None

class SkillTagCreate(SkillTagBase):
    pass

class SkillTag(SkillTagBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class UserSkillBase(BaseModel):
    skill_level: str = "beginner"
    is_teaching: bool = False
    is_learning: bool = False

class UserSkillCreate(UserSkillBase):
    skill_tag_id: int

class UserSkillUpdate(BaseModel):
    skill_level: Optional[str] = None
    is_teaching: Optional[bool] = None
    is_learning: Optional[bool] = None

class UserSkill(UserSkillBase):
    skill_tag_id: int
    skill_tag: SkillTag
    created_at: datetime

    class Config:
        from_attributes = True