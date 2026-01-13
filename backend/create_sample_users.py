from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from passlib.context import CryptContext
from datetime import datetime

# Database setup
DATABASE_URL = "sqlite:///./skillswap.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# User model
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

# Create tables
Base.metadata.create_all(bind=engine)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

# Sample users
sample_users = [
    {
        "email": "john@example.com",
        "username": "john_doe",
        "full_name": "John Doe",
        "password": "password123",
        "bio": "Software developer and coding instructor"
    },
    {
        "email": "jane@example.com", 
        "username": "jane_smith",
        "full_name": "Jane Smith",
        "password": "password123",
        "bio": "UI/UX designer with 5 years experience"
    },
    {
        "email": "mike@example.com",
        "username": "mike_wilson",
        "full_name": "Mike Wilson",
        "password": "password123", 
        "bio": "Data scientist and Python expert"
    }
]

# Add sample users
db = SessionLocal()

for user_data in sample_users:
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data["email"]).first()
    if not existing_user:
        hashed_password = get_password_hash(user_data["password"])
        db_user = User(
            email=user_data["email"],
            username=user_data["username"],
            full_name=user_data["full_name"],
            hashed_password=hashed_password,
            bio=user_data["bio"]
        )
        db.add(db_user)
        print(f"Added user: {user_data['email']}")
    else:
        print(f"User already exists: {user_data['email']}")

db.commit()
db.close()

print("\nSample login credentials:")
print("Email: john@example.com | Password: password123")
print("Email: jane@example.com | Password: password123") 
print("Email: mike@example.com | Password: password123")