from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import os

# Database setup
DATABASE_URL = "sqlite:///./skillswap.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    bio = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Skill(Base):
    __tablename__ = "skills"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    category = Column(String)
    difficulty_level = Column(String)
    price_per_hour = Column(Integer)
    teacher_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    max_participants = Column(Integer, default=1)
    skill_id = Column(Integer)
    teacher_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

class UserSkill(Base):
    __tablename__ = "user_skills"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    skill_id = Column(Integer, nullable=False)
    skill_level = Column(String, default="beginner")
    is_teaching = Column(Boolean, default=False)
    is_learning = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, default="pending")
    booking_notes = Column(String)
    student_id = Column(Integer)
    session_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=engine)

# Schemas
class UserCreate(BaseModel):
    email: str
    username: str
    full_name: str
    password: str
    bio: str = None

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    full_name: str
    bio: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

import hashlib

# Security
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"

def get_password_hash(password: str):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str):
    # Try SHA256 first (for sample users)
    if hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password:
        return True
    # Try bcrypt if available
    try:
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.verify(plain_password, hashed_password)
    except:
        return False

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# FastAPI app
app = FastAPI(title="SkillSwap Hub API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
@app.get("/")
def read_root():
    return {"message": "SkillSwap Hub API is running"}

@app.post("/auth/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # Create user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        hashed_password=hashed_password,
        bio=user.bio
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/auth/login", response_model=Token)
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_credentials.email).first()
    
    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=UserResponse)
def get_current_user_info(db: Session = Depends(get_db)):
    # Simple implementation - just return first user for now
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/skills/")
def get_skills(db: Session = Depends(get_db)):
    skills = db.query(Skill).all()
    # Convert to match frontend expectations
    result = []
    for skill in skills:
        result.append({
            "id": skill.id,
            "name": skill.title,  # Frontend expects 'name'
            "title": skill.title,
            "description": skill.description,
            "category": skill.category,
            "difficulty_level": skill.difficulty_level,
            "price_per_hour": skill.price_per_hour,
            "teacher_id": skill.teacher_id,
            "sessions": []  # Add empty sessions array
        })
    return result

@app.get("/skills/search")
def search_skills(q: str, db: Session = Depends(get_db)):
    skills = db.query(Skill).filter(Skill.title.contains(q)).all()
    result = []
    for skill in skills:
        result.append({
            "id": skill.id,
            "name": skill.title,
            "title": skill.title,
            "description": skill.description,
            "category": skill.category,
            "difficulty_level": skill.difficulty_level,
            "price_per_hour": skill.price_per_hour,
            "teacher_id": skill.teacher_id,
            "sessions": []
        })
    return result

@app.get("/skills/{skill_id}")
def get_skill(skill_id: int, db: Session = Depends(get_db)):
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return {
        "id": skill.id,
        "name": skill.title,
        "title": skill.title,
        "description": skill.description,
        "category": skill.category,
        "difficulty_level": skill.difficulty_level,
        "price_per_hour": skill.price_per_hour,
        "teacher_id": skill.teacher_id,
        "sessions": []
    }

@app.post("/skills/")
def create_skill(skill_data: dict, db: Session = Depends(get_db)):
    skill = Skill(**skill_data)
    db.add(skill)
    db.commit()
    db.refresh(skill)
    return skill

@app.put("/skills/{skill_id}")
def update_skill(skill_id: int, skill_data: dict, db: Session = Depends(get_db)):
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    for key, value in skill_data.items():
        setattr(skill, key, value)
    db.commit()
    return skill

@app.delete("/skills/{skill_id}")
def delete_skill(skill_id: int, db: Session = Depends(get_db)):
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    db.delete(skill)
    db.commit()
    return {"message": "Skill deleted"}

@app.get("/sessions/")
def get_sessions(db: Session = Depends(get_db)):
    sessions = db.query(Session).all()
    return sessions

@app.post("/sessions/")
def create_session(session_data: dict, db: Session = Depends(get_db)):
    # Convert datetime strings to datetime objects if needed
    if isinstance(session_data.get('start_time'), str):
        from datetime import datetime
        session_data['start_time'] = datetime.fromisoformat(session_data['start_time'].replace('Z', '+00:00'))
    if isinstance(session_data.get('end_time'), str):
        from datetime import datetime
        session_data['end_time'] = datetime.fromisoformat(session_data['end_time'].replace('Z', '+00:00'))
    
    # Add teacher_id (hardcoded for now)
    session_data['teacher_id'] = 1
    
    session = Session(**session_data)
    db.add(session)
    db.commit()
    db.refresh(session)
    return session

@app.get("/skill-tags/")
def get_skill_tags(db: Session = Depends(get_db)):
    skills = db.query(Skill).all()
    result = []
    for skill in skills:
        result.append({
            "id": skill.id,
            "name": skill.title,
            "category": skill.category
        })
    return result

@app.get("/skill-tags/user-skills/me")
def get_my_skills(db: Session = Depends(get_db)):
    # Get user skills with skill details
    user_skills = db.query(UserSkill).filter(UserSkill.user_id == 1).all()
    result = []
    for user_skill in user_skills:
        skill = db.query(Skill).filter(Skill.id == user_skill.skill_id).first()
        if skill:
            result.append({
                "id": skill.id,  # Use skill ID, not user_skill ID
                "user_skill_id": user_skill.id,  # Keep user_skill ID for deletion
                "name": skill.title,
                "skill_level": user_skill.skill_level,
                "is_teaching": user_skill.is_teaching,
                "is_learning": user_skill.is_learning
            })
    return result

@app.post("/skill-tags/user-skills")
def add_user_skill(skill_data: dict, db: Session = Depends(get_db)):
    user_skill = UserSkill(
        user_id=1,  # Hardcoded for now
        skill_id=skill_data["skill_tag_id"],
        skill_level=skill_data["skill_level"],
        is_teaching=skill_data["is_teaching"],
        is_learning=skill_data["is_learning"]
    )
    db.add(user_skill)
    db.commit()
    db.refresh(user_skill)
    return {"message": "Skill added successfully"}

@app.delete("/skill-tags/user-skills/{skill_id}")
def remove_user_skill(skill_id: int, db: Session = Depends(get_db)):
    user_skill = db.query(UserSkill).filter(UserSkill.id == skill_id).first()
    if user_skill:
        db.delete(user_skill)
        db.commit()
    return {"message": "Skill removed successfully"}

@app.get("/bookings/")
def get_bookings(db: Session = Depends(get_db)):
    bookings = db.query(Booking).all()
    return bookings

@app.post("/bookings/")
def create_booking(booking_data: dict, db: Session = Depends(get_db)):
    booking = Booking(**booking_data)
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking

# Missing endpoints from frontend APIs
@app.post("/auth/logout")
def logout():
    return {"message": "Logged out successfully"}

@app.post("/auth/refresh")
def refresh_token():
    return {"message": "Token refresh not implemented"}

@app.post("/auth/google")
def google_auth(token_data: dict):
    return {"message": "Google auth not implemented"}

@app.get("/sessions/{session_id}")
def get_session(session_id: int, db: Session = Depends(get_db)):
    session = db.query(Session).filter(Session.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@app.put("/sessions/{session_id}")
def update_session(session_id: int, session_data: dict, db: Session = Depends(get_db)):
    session = db.query(Session).filter(Session.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    for key, value in session_data.items():
        setattr(session, key, value)
    db.commit()
    return session

@app.delete("/sessions/{session_id}")
def delete_session(session_id: int, db: Session = Depends(get_db)):
    session = db.query(Session).filter(Session.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    db.delete(session)
    db.commit()
    return {"message": "Session deleted"}

@app.post("/sessions/{session_id}/book")
def book_session(session_id: int, db: Session = Depends(get_db)):
    booking = Booking(session_id=session_id, student_id=1, status="confirmed")
    db.add(booking)
    db.commit()
    return {"message": "Session booked successfully"}

@app.delete("/sessions/{session_id}/book")
def cancel_booking(session_id: int, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.session_id == session_id).first()
    if booking:
        db.delete(booking)
        db.commit()
    return {"message": "Booking cancelled"}

@app.get("/bookings/my")
def get_my_bookings(db: Session = Depends(get_db)):
    bookings = db.query(Booking).filter(Booking.student_id == 1).all()
    return bookings

@app.post("/skill-tags/")
def create_skill_tag(skill_tag: dict, db: Session = Depends(get_db)):
    skill = Skill(**skill_tag)
    db.add(skill)
    db.commit()
    db.refresh(skill)
    return skill