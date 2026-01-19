from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..deps import get_db, get_current_user
from ...models.session import Session as SessionModel
from ...models.skill import Skill
from ...models.user import User
from ...schemas.session import Session as SessionSchema, SessionCreate, SessionUpdate

router = APIRouter()

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from ..deps import get_db, get_current_user
from ...models.session import Session as SessionModel
from ...models.user_skills import SkillTag
from ...models.user import User
from ...schemas.session import Session as SessionSchema, SessionCreate, SessionUpdate

router = APIRouter()

@router.post("/", response_model=SessionSchema)
def create_session(
    session: SessionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify skill tag exists and user can teach it
    skill_tag = db.query(SkillTag).filter(SkillTag.id == session.skill_id).first()
    if not skill_tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found"
        )
    
    # Check if user has this skill and can teach it
    user_skill = db.execute(
        text("SELECT * FROM user_skills WHERE user_id = :user_id AND skill_tag_id = :skill_tag_id AND is_teaching = 1"),
        {"user_id": current_user.id, "skill_tag_id": session.skill_id}
    ).first()
    
    if not user_skill:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to teach this skill. Please add it to your teaching skills first."
        )
    
    db_session = SessionModel(**session.dict(), teacher_id=current_user.id)
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

@router.get("/", response_model=List[SessionSchema])
def get_sessions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    sessions = db.query(SessionModel).offset(skip).limit(limit).all()
    return sessions

@router.get("/{session_id}", response_model=SessionSchema)
def get_session(session_id: int, db: Session = Depends(get_db)):
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    return session

@router.put("/{session_id}", response_model=SessionSchema)
def update_session(
    session_id: int,
    session_update: SessionUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    if session.teacher_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this session"
        )
    
    for field, value in session_update.dict(exclude_unset=True).items():
        setattr(session, field, value)
    
    db.commit()
    db.refresh(session)
    return session

@router.delete("/{session_id}")
def delete_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    if session.teacher_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this session"
        )
    
    db.delete(session)
    db.commit()
    return {"message": "Session deleted successfully"}