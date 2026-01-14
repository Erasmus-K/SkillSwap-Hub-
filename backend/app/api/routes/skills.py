<<<<<<< HEAD
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..deps import get_db, get_current_user
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
    db_skill = Skill(**skill.dict(), teacher_id=current_user.id)
=======
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas import SkillCreate, SkillUpdate, SkillResponse
from app.models import Skill, User
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/", response_model=SkillResponse)
def create_skill(
    skill: SkillCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_skill = Skill(
        title=skill.title,
        description=skill.description,
        category=skill.category,
        created_by=current_user.id
    )
>>>>>>> 8cabe45 (Created skill.py file to add new new skill)
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill

<<<<<<< HEAD
@router.get("/", response_model=List[SkillSchema])
=======
@router.get("/", response_model=List[SkillResponse])
>>>>>>> 8cabe45 (Created skill.py file to add new new skill)
def get_skills(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    skills = db.query(Skill).offset(skip).limit(limit).all()
    return skills

<<<<<<< HEAD
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
    
    if skill.teacher_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this skill"
        )
    
    for field, value in skill_update.dict(exclude_unset=True).items():
=======
@router.get("/{skill_id}", response_model=SkillResponse)
def get_skill(skill_id: int, db: Session = Depends(get_db)):
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if skill is None:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill

@router.put("/{skill_id}", response_model=SkillResponse)
def update_skill(
    skill_id: int,
    skill_update: SkillUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if skill is None:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    if skill.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    update_data = skill_update.dict(exclude_unset=True)
    for field, value in update_data.items():
>>>>>>> 8cabe45 (Created skill.py file to add new new skill)
        setattr(skill, field, value)
    
    db.commit()
    db.refresh(skill)
    return skill

@router.delete("/{skill_id}")
def delete_skill(
    skill_id: int,
<<<<<<< HEAD
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found"
        )
    
    if skill.teacher_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this skill"
        )
=======
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if skill is None:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    if skill.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
>>>>>>> 8cabe45 (Created skill.py file to add new new skill)
    
    db.delete(skill)
    db.commit()
    return {"message": "Skill deleted successfully"}