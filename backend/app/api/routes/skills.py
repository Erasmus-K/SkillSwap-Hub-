from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ...db.session import get_db
from ..deps import get_current_user
from ...models.skill import Skill
from ...models.user import User
from ...schemas.skill import Skill as SkillSchema, SkillCreate, SkillUpdate

router = APIRouter()

@router.post("/", response_model=SkillSchema)
def create_skill(
    skill: SkillCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_skill = Skill(
        title=skill.title,
        description=skill.description,
        category=skill.category,
        created_by=current_user.id
    )
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill

@router.get("/", response_model=List[SkillSchema])
def get_skills(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    skills = db.query(Skill).offset(skip).limit(limit).all()
    return skills

@router.get("/{skill_id}", response_model=SkillSchema)
def get_skill(skill_id: int, db: Session = Depends(get_db)):
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found"
        )
    return skill

@router.put("/{skill_id}", response_model=SkillSchema)
def update_skill(
    skill_id: int,
    skill_update: SkillUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found"
        )
    
    if skill.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this skill"
        )
    
    for field, value in skill_update.dict(exclude_unset=True).items():
        setattr(skill, field, value)
    
    db.commit()
    db.refresh(skill)
    return skill

@router.delete("/{skill_id}")
def delete_skill(
    skill_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found"
        )
    
    if skill.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this skill"
        )
    
    db.delete(skill)
    db.commit()
    return {"message": "Skill deleted successfully"}
