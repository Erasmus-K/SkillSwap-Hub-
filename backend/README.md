# SkillSwap Hub Backend

FastAPI backend for the SkillSwap Hub application - a platform for skill sharing and learning sessions.

## Features

- JWT Authentication with access and refresh tokens
- User registration and login
- Skills CRUD operations
- Sessions management
- Booking system
- Protected routes
- PostgreSQL database with SQLAlchemy ORM
- Database migrations with Alembic

## Tech Stack

- **FastAPI** - Modern, fast web framework
- **SQLAlchemy 2.0** - SQL toolkit and ORM
- **PostgreSQL** - Database
- **JWT** - Authentication
- **Alembic** - Database migrations
- **Pydantic** - Data validation

## Setup Instructions

### Prerequisites

- Python 3.8+
- PostgreSQL
- pip

### Installation

1. Clone the repository and navigate to backend:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
```

Edit `.env` with your database credentials and secret key:
```
DATABASE_URL=postgresql://username:password@localhost/skillswap_db
SECRET_KEY=your-super-secret-key-here
```

5. Create database:
```bash
createdb skillswap_db
```

6. Run database migrations:
```bash
alembic upgrade head
```

7. Start the server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user

### Users
- `GET /users/me` - Get current user profile
- `PUT /users/me` - Update current user profile
- `GET /users/` - Get all users
- `GET /users/{user_id}` - Get user by ID

### Skills
- `POST /skills/` - Create new skill (protected)
- `GET /skills/` - Get all skills
- `GET /skills/{skill_id}` - Get skill by ID
- `PUT /skills/{skill_id}` - Update skill (protected)
- `DELETE /skills/{skill_id}` - Delete skill (protected)

### Sessions
- `POST /sessions/` - Create new session (protected)
- `GET /sessions/` - Get all sessions
- `GET /sessions/{session_id}` - Get session by ID
- `PUT /sessions/{session_id}` - Update session (protected)
- `DELETE /sessions/{session_id}` - Delete session (protected)

### Bookings
- `POST /bookings/` - Create new booking (protected)
- `GET /bookings/` - Get user's bookings (protected)
- `GET /bookings/{booking_id}` - Get booking by ID (protected)
- `PATCH /bookings/{booking_id}` - Update booking (protected)
- `DELETE /bookings/{booking_id}` - Cancel booking (protected)

## Database Schema

### Models
- **User**: User accounts with authentication
- **Skill**: Skills offered by teachers
- **Session**: Learning sessions for specific skills
- **Booking**: Student bookings for sessions

### Relationships
- User → Skills (1:many)
- User → Sessions (1:many)
- User → Bookings (1:many)
- Skill → Sessions (1:many)
- Session → Bookings (1:many)

## Development

### Running Tests
```bash
pytest
```

### Database Migrations
Create new migration:
```bash
alembic revision --autogenerate -m "Description"
```

Apply migrations:
```bash
alembic upgrade head
```

## License

MIT License