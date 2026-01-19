from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from ..deps import get_db, get_current_user
from ...models.user_skills import SkillTag, user_skills
from ...models.user import User
from ...schemas.user_skills import SkillTag as SkillTagSchema, SkillTagCreate, UserSkillCreate, UserSkillUpdate

router = APIRouter()

@router.get("/", response_model=List[SkillTagSchema])
def get_skill_tags(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    skill_tags = db.query(SkillTag).offset(skip).limit(limit).all()
    return skill_tags

@router.post("/", response_model=SkillTagSchema)
def create_skill_tag(skill_tag: SkillTagCreate, db: Session = Depends(get_db)):
    # Check if skill tag already exists
    existing = db.query(SkillTag).filter(SkillTag.name.ilike(skill_tag.name)).first()
    if existing:
        return existing
    
    db_skill_tag = SkillTag(**skill_tag.dict())
    db.add(db_skill_tag)
    db.commit()
    db.refresh(db_skill_tag)
    return db_skill_tag

@router.post("/user-skills", response_model=dict)
def add_user_skill(
    user_skill: UserSkillCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if skill tag exists
    skill_tag = db.query(SkillTag).filter(SkillTag.id == user_skill.skill_tag_id).first()
    if not skill_tag:
        raise HTTPException(status_code=404, detail="Skill tag not found")
    
    # Check if user already has this skill
    existing = db.execute(
        text("SELECT * FROM user_skills WHERE user_id = :user_id AND skill_tag_id = :skill_tag_id"),
        {"user_id": current_user.id, "skill_tag_id": user_skill.skill_tag_id}
    ).first()
    
    if existing:
        # Update existing
        db.execute(
            text("""UPDATE user_skills 
                    SET skill_level = :skill_level, is_teaching = :is_teaching, is_learning = :is_learning
                    WHERE user_id = :user_id AND skill_tag_id = :skill_tag_id"""),
            {
                "user_id": current_user.id,
                "skill_tag_id": user_skill.skill_tag_id,
                "skill_level": user_skill.skill_level,
                "is_teaching": user_skill.is_teaching,
                "is_learning": user_skill.is_learning
            }
        )
    else:
        # Insert new
        db.execute(
            text("""INSERT INTO user_skills (user_id, skill_tag_id, skill_level, is_teaching, is_learning)
                    VALUES (:user_id, :skill_tag_id, :skill_level, :is_teaching, :is_learning)"""),
            {
                "user_id": current_user.id,
                "skill_tag_id": user_skill.skill_tag_id,
                "skill_level": user_skill.skill_level,
                "is_teaching": user_skill.is_teaching,
                "is_learning": user_skill.is_learning
            }
        )
    
    db.commit()
    return {"message": "User skill updated successfully"}

@router.get("/user-skills/me")
def get_my_skills(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    result = db.execute(
        text("""SELECT st.*, us.skill_level, us.is_teaching, us.is_learning, us.created_at as user_skill_created_at
                FROM skill_tags st
                JOIN user_skills us ON st.id = us.skill_tag_id
                WHERE us.user_id = :user_id
                ORDER BY st.category, st.name"""),
        {"user_id": current_user.id}
    ).fetchall()
    
    skills = []
    for row in result:
        skills.append({
            "id": row.id,
            "name": row.name,
            "category": row.category,
            "description": row.description,
            "skill_level": row.skill_level,
            "is_teaching": row.is_teaching,
            "is_learning": row.is_learning,
            "created_at": row.user_skill_created_at
        })
    
    return skills

@router.delete("/user-skills/{skill_tag_id}")
def remove_user_skill(
    skill_tag_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db.execute(
        text("DELETE FROM user_skills WHERE user_id = :user_id AND skill_tag_id = :skill_tag_id"),
        {"user_id": current_user.id, "skill_tag_id": skill_tag_id}
    )
    db.commit()
    return {"message": "Skill removed successfully"}