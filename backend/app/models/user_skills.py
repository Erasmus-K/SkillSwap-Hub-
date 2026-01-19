from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Table
from sqlalchemy.sql import func
from ..db.session import Base

# Association table for user skills (many-to-many)
user_skills = Table(
    'user_skills',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('skill_tag_id', Integer, ForeignKey('skill_tags.id'), primary_key=True),
    Column('skill_level', String, default='beginner'),  # beginner, intermediate, advanced
    Column('is_teaching', Boolean, default=False),  # can teach this skill
    Column('is_learning', Boolean, default=False),  # wants to learn this skill
    Column('created_at', DateTime(timezone=True), server_default=func.now())
)

class SkillTag(Base):
    __tablename__ = "skill_tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)  # e.g., "Python", "React", "JavaScript"
    category = Column(String, nullable=False)  # e.g., "Programming", "Design", "Marketing"
    description = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())