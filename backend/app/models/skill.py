# add_skill.py

from sqlalchemy.orm import Session
from app.db.database import SessionLocal, engine
from app.models.skill import Skill  # adjust path if needed
from app.models.user import User     # needed if you reference creator

# Create tables if they don't exist
from app.db.database import Base
Base.metadata.create_all(bind=engine)

def add_skill(title: str, description: str, category: str, created_by: int):
    db: Session = SessionLocal()
    try:
        skill = Skill(
            title=title,
            description=description,
            category=category,
            created_by=created_by
        )
        db.add(skill)
        db.commit()
        db.refresh(skill)
        print(f"Skill added: {skill.title} (ID: {skill.id})")
    except Exception as e:
        print("Error:", e)
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    # Example: add a Python skill created by user with ID 
    add_skill(
        title="Python Programming",
        description="Learn the basics of Python programming.",
        category="Programming",
        created_by=1  # Ensure this user ID exists in your database
    )