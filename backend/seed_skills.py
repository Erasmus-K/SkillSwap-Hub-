from app.db.session import SessionLocal
from app.models.user_skills import SkillTag

def seed_skill_tags():
    db = SessionLocal()
    
    # Programming Languages
    programming_skills = [
        {"name": "Python", "category": "Programming", "description": "Python programming language"},
        {"name": "JavaScript", "category": "Programming", "description": "JavaScript programming language"},
        {"name": "Java", "category": "Programming", "description": "Java programming language"},
        {"name": "C#", "category": "Programming", "description": "C# programming language"},
        {"name": "C++", "category": "Programming", "description": "C++ programming language"},
        {"name": "Go", "category": "Programming", "description": "Go programming language"},
        {"name": "Rust", "category": "Programming", "description": "Rust programming language"},
        {"name": "PHP", "category": "Programming", "description": "PHP programming language"},
        {"name": "Ruby", "category": "Programming", "description": "Ruby programming language"},
        {"name": "Swift", "category": "Programming", "description": "Swift programming language"},
    ]
    
    # Web Development
    web_skills = [
        {"name": "React", "category": "Web Development", "description": "React JavaScript library"},
        {"name": "Vue.js", "category": "Web Development", "description": "Vue.js JavaScript framework"},
        {"name": "Angular", "category": "Web Development", "description": "Angular JavaScript framework"},
        {"name": "Node.js", "category": "Web Development", "description": "Node.js runtime environment"},
        {"name": "Express.js", "category": "Web Development", "description": "Express.js web framework"},
        {"name": "Django", "category": "Web Development", "description": "Django Python web framework"},
        {"name": "Flask", "category": "Web Development", "description": "Flask Python web framework"},
        {"name": "FastAPI", "category": "Web Development", "description": "FastAPI Python web framework"},
        {"name": "HTML", "category": "Web Development", "description": "HTML markup language"},
        {"name": "CSS", "category": "Web Development", "description": "CSS styling language"},
    ]
    
    # Database
    database_skills = [
        {"name": "MySQL", "category": "Database", "description": "MySQL database"},
        {"name": "PostgreSQL", "category": "Database", "description": "PostgreSQL database"},
        {"name": "MongoDB", "category": "Database", "description": "MongoDB NoSQL database"},
        {"name": "Redis", "category": "Database", "description": "Redis in-memory database"},
        {"name": "SQLite", "category": "Database", "description": "SQLite database"},
    ]
    
    # DevOps & Cloud
    devops_skills = [
        {"name": "Docker", "category": "DevOps", "description": "Docker containerization"},
        {"name": "Kubernetes", "category": "DevOps", "description": "Kubernetes orchestration"},
        {"name": "AWS", "category": "Cloud", "description": "Amazon Web Services"},
        {"name": "Azure", "category": "Cloud", "description": "Microsoft Azure"},
        {"name": "Google Cloud", "category": "Cloud", "description": "Google Cloud Platform"},
        {"name": "Git", "category": "DevOps", "description": "Git version control"},
    ]
    
    # Design
    design_skills = [
        {"name": "UI/UX Design", "category": "Design", "description": "User Interface and User Experience Design"},
        {"name": "Figma", "category": "Design", "description": "Figma design tool"},
        {"name": "Adobe Photoshop", "category": "Design", "description": "Adobe Photoshop"},
        {"name": "Adobe Illustrator", "category": "Design", "description": "Adobe Illustrator"},
    ]
    
    all_skills = programming_skills + web_skills + database_skills + devops_skills + design_skills
    
    for skill_data in all_skills:
        existing = db.query(SkillTag).filter(SkillTag.name == skill_data["name"]).first()
        if not existing:
            skill_tag = SkillTag(**skill_data)
            db.add(skill_tag)
    
    db.commit()
    db.close()
    print(f"Seeded {len(all_skills)} skill tags")

if __name__ == "__main__":
    seed_skill_tags()