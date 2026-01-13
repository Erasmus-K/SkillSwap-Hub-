from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..deps import get_db, get_current_user
from ...models.session import Session as SessionModel
from ...models.skill import Skill
from ...models.user import User
from ...schemas.session import Session as SessionSchema, SessionCreate, SessionUpdate

router = APIRouter()

@router.post("/", response_model=SessionSchema)
def create_session(
    session: SessionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify skill belongs to current user
    skill = db.query(Skill).filter(Skill.id == session.skill_id).first()
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found"
        )
    
    if skill.teacher_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create session for this skill"
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