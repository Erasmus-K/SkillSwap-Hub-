import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect('skillswap.db')
cursor = conn.cursor()

# Sample skills
skills = [
    (1, "Python Programming", "Learn Python from basics to advanced", "Programming", "Beginner", 25, 1),
    (2, "Web Design", "Create beautiful websites with HTML/CSS", "Design", "Intermediate", 30, 2),
    (3, "Data Analysis", "Analyze data with Python and pandas", "Data Science", "Advanced", 40, 3)
]

cursor.executemany('''
INSERT OR REPLACE INTO skills (id, title, description, category, difficulty_level, price_per_hour, teacher_id)
VALUES (?, ?, ?, ?, ?, ?, ?)
''', skills)

# Sample sessions
now = datetime.now()
sessions = [
    (1, "Python Basics Workshop", "2-hour intro to Python", now + timedelta(days=1), now + timedelta(days=1, hours=2), 5, 1, 1),
    (2, "CSS Grid Masterclass", "Learn modern CSS layouts", now + timedelta(days=2), now + timedelta(days=2, hours=1.5), 3, 2, 2),
    (3, "Data Visualization", "Create charts with matplotlib", now + timedelta(days=3), now + timedelta(days=3, hours=3), 4, 3, 3)
]

cursor.executemany('''
INSERT OR REPLACE INTO sessions (id, title, description, start_time, end_time, max_participants, skill_id, teacher_id)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
''', sessions)

conn.commit()
conn.close()

print("Added sample skills and sessions to database")