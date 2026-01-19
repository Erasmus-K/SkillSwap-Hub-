from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
<<<<<<< HEAD

class UserBase(BaseModel):
    email: str
    username: str
    full_name: str
    bio: Optional[str] = None
=======
from app.models.user import UserRole

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: Optional[UserRole] = UserRole.STUDENT
>>>>>>> 8cabe45 (Created skill.py file to add new new skill)

class UserCreate(UserBase):
    password: str

<<<<<<< HEAD
class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    bio: Optional[str] = None

class User(UserBase):
    id: int
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
=======
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse
>>>>>>> 8cabe45 (Created skill.py file to add new new skill)
