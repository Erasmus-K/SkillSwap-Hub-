# SkillSwap Hub - Backend API

Production-ready FastAPI backend for the SkillSwap Hub peer-to-peer micro-learning platform.

## Features

- **JWT Authentication** with bcrypt password hashing
- **PostgreSQL** database with SQLAlchemy ORM
- **RESTful API** with automatic OpenAPI documentation
- **Database migrations** with Alembic
- **CORS support** for frontend integration
- **Production-ready** with proper error handling

## Tech Stack

- **FastAPI** - Modern Python web framework
- **SQLAlchemy 2.0** - SQL toolkit and ORM
- **PostgreSQL** - Production database
- **Alembic** - Database migration tool
- **JWT** - JSON Web Token authentication
- **Bcrypt** - Password hashing
- **Pydantic** - Data validation

## Quick Start

### Prerequisites

- Python 3.8+
- PostgreSQL database
- pip or poetry

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables in `.env`:
```bash
DATABASE_URL=postgresql://username:password@localhost:5432/skillswap_db
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

3. Create database:
```bash
createdb skillswap_db
```

4. Run database migrations:
```bash
alembic upgrade head
```

5. Start the server:
```bash
python run.py
# or
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user

### Skills
- `GET /skills` - List all skills
- `POST /skills` - Create new skill (authenticated)
- `GET /skills/{id}` - Get skill by ID
- `PUT /skills/{id}` - Update skill (owner only)
- `DELETE /skills/{id}` - Delete skill (owner only)

## Database Models

### User
- `id` (Integer, Primary Key)
- `name` (String, Required)
- `email` (String, Unique, Required)
- `password_hash` (String, Required)
- `role` (Enum: student/teacher/admin)
- `created_at` (DateTime)

### Skill
- `id` (Integer, Primary Key)
- `title` (String, Required)
- `description` (Text)
- `category` (String, Required)
- `created_by` (Foreign Key → User)
- `created_at` (DateTime)

## Development

### Database Migrations

Create new migration:
```bash
alembic revision --autogenerate -m "Description"
```

Apply migrations:
```bash
alembic upgrade head
```

### Testing with curl

Register user:
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123"
  }'
```

Login:
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "password123"
  }'
```

Create skill (with token):
```bash
curl -X POST "http://localhost:8000/skills" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "title": "Python Programming",
    "description": "Learn Python basics",
    "category": "Programming"
  }'
```

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── auth.py      # Authentication endpoints
│   │   │   └── skills.py    # Skills CRUD endpoints
│   │   └── deps.py          # Dependencies (auth, db)
│   ├── core/
│   │   ├── config.py        # Settings configuration
│   │   └── security.py      # JWT & password utilities
│   ├── db/
│   │   └── database.py      # Database connection
│   ├── models/
│   │   ├── user.py          # User SQLAlchemy model
│   │   └── skill.py         # Skill SQLAlchemy model
│   ├── schemas/
│   │   ├── user.py          # User Pydantic schemas
│   │   └── skill.py         # Skill Pydantic schemas
│   └── main.py              # FastAPI application
├── alembic/                 # Database migrations
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables
└── run.py                   # Development server
```

## Deployment

For production deployment:

1. Set strong `SECRET_KEY` in environment
2. Use production PostgreSQL database
3. Set `reload=False` in uvicorn
4. Use proper ASGI server like Gunicorn
5. Set up reverse proxy (nginx)
6. Enable HTTPS

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Run tests
5. Submit pull request