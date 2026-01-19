from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from passlib.context import CryptContext
from datetime import datetime

# Database setup
DATABASE_URL = "sqlite:///./skillswap.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

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

Base.metadata.create_all(bind=engine)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Sample users
sample_users = [
    ("john@example.com", "john_doe", "John Doe", "password123", "Software developer"),
    ("jane@example.com", "jane_smith", "Jane Smith", "password123", "UI/UX designer"),
    ("mike@example.com", "mike_wilson", "Mike Wilson", "password123", "Data scientist")
]

db = SessionLocal()

# Clear existing users
db.query(User).delete()

# Add sample users with bcrypt
for email, username, full_name, password, bio in sample_users:
    hashed_password = pwd_context.hash(password)
    db_user = User(
        email=email,
        username=username,
        full_name=full_name,
        hashed_password=hashed_password,
        bio=bio
    )
    db.add(db_user)
    print(f"Added user: {email}")

db.commit()
db.close()

print("\n=== SAMPLE LOGIN CREDENTIALS ===")
print("Email: john@example.com | Password: password123")
print("Email: jane@example.com | Password: password123") 
print("Email: mike@example.com | Password: password123")
print("=================================")