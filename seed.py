#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.db.session import SessionLocal, engine, Base
from app.models.user import User
from app.models.skill import Skill
from app.models.session import Session
from app.models.booking import Booking
from app.core.security import get_password_hash
from datetime import datetime, timedelta

def create_sample_data():
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(User).first():
            print("Database already contains data. Skipping seed.")
            return
        
        # Create sample users
        users = [
            User(
                email="john@example.com",
                username="john_doe",
                full_name="John Doe",
                hashed_password=get_password_hash("password123"),
                bio="Experienced web developer with 5+ years in React and Python"
            ),
            User(
                email="jane@example.com",
                username="jane_smith",
                full_name="Jane Smith",
                hashed_password=get_password_hash("password123"),
                bio="UI/UX designer passionate about creating beautiful user experiences"
            ),
            User(
                email="mike@example.com",
                username="mike_wilson",
                full_name="Mike Wilson",
                hashed_password=get_password_hash("password123"),
                bio="Data scientist and machine learning enthusiast"
            )
        ]
        
        for user in users:
            db.add(user)
        db.commit()
        
        # Create sample skills
        skills = [
            Skill(
                title="React Development",
                description="Learn modern React development with hooks, context, and best practices",
                category="Web Development",
                difficulty_level="intermediate",
                price_per_hour=50.0,
                teacher_id=1
            ),
            Skill(
                title="UI/UX Design Fundamentals",
                description="Master the basics of user interface and user experience design",
                category="Design",
                difficulty_level="beginner",
                price_per_hour=40.0,
                teacher_id=2
            ),
            Skill(
                title="Python Data Analysis",
                description="Learn data analysis with Python, pandas, and matplotlib",
                category="Data Science",
                difficulty_level="intermediate",
                price_per_hour=60.0,
                teacher_id=3
            )
        ]
        
        for skill in skills:
            db.add(skill)
        db.commit()
        
        print("✅ Sample data created successfully!")
        print("Sample users:")
        print("- john@example.com / password123")
        print("- jane@example.com / password123") 
        print("- mike@example.com / password123")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_data()