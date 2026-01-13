import sqlite3
import hashlib

# Simple password hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Connect to database
conn = sqlite3.connect('skillswap.db')
cursor = conn.cursor()

# Create users table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE,
    username TEXT UNIQUE,
    full_name TEXT,
    hashed_password TEXT,
    bio TEXT,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Sample users
sample_users = [
    ("john@example.com", "john_doe", "John Doe", "password123", "Software developer"),
    ("jane@example.com", "jane_smith", "Jane Smith", "password123", "UI/UX designer"),
    ("mike@example.com", "mike_wilson", "Mike Wilson", "password123", "Data scientist")
]

# Insert sample users
for email, username, full_name, password, bio in sample_users:
    hashed_password = hash_password(password)
    try:
        cursor.execute('''
        INSERT OR IGNORE INTO users (email, username, full_name, hashed_password, bio)
        VALUES (?, ?, ?, ?, ?)
        ''', (email, username, full_name, hashed_password, bio))
        print(f"Added user: {email}")
    except Exception as e:
        print(f"Error adding {email}: {e}")

conn.commit()
conn.close()

print("\n=== SAMPLE LOGIN CREDENTIALS ===")
print("Email: john@example.com | Password: password123")
print("Email: jane@example.com | Password: password123") 
print("Email: mike@example.com | Password: password123")
print("=================================")