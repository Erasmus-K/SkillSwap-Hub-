# SkillSwap

#### Date: 6 January, 2026

## Description

SkillSwap Hub is a peer-to-peer micro-learning platform that allows users to teach, learn, and exchange practical skills in short, focused sessions. A key enhancement in this phase is integrating live video sessions using Google Meet, allowing learners and teachers to book, join, and participate in real-time meetings directly from the application.

#### Software Engineer
- Erasmus Kipkosgei
- Joshua Muriki
- Tonny Bett
- James Isaiah
- Mohamed Shafi

## Project Description

This project is a full-stack web application built as a Single Page Application (SPA) using React on the frontend and FastAPI on the backend. It demonstrates:

- Authentication
- Protected routes
- Database models
- RESTful endpoints
- State management, and 
- Third-party API integration.

## Setup and Installation

### Backend Setup
1. Navigate to backend directory: `cd backend`
2. Create virtual environment: `python3 -m venv venv`
3. Activate virtual environment: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`

### Frontend Setup
1. Navigate to frontend directory: `cd frontend`
2. Install dependencies: `npm install`

### Running the Application

**Option 1: Use the startup script (recommended)**
```bash
./start.sh
```

**Option 2: Run manually**

Backend:
```bash
cd backend
source venv/bin/activate
python -m uvicorn app.main:app --reload --port 8000
```

Frontend (in a new terminal):
```bash
cd frontend
npm run dev
```

### Access the Application
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## API Endpoints

- `GET /` - API root endpoint
- `GET /health` - Health check
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /users/me` - Get current user profile
- `GET /skills` - List all skills
- `POST /skills` - Create new skill
- `GET /sessions` - List learning sessions
- `POST /sessions` - Create new session
- `GET /bookings` - List user bookings
- `POST /bookings` - Create new booking

## Technologies Used

- React 18.2.0
- Python 3.12
- FastAPI 0.104.1
- SQLAlchemy 2.0.23
- SQLite Database
- Vite (Frontend build tool)
- Tailwind CSS

## Contact

Moringa School Software Engineers

## License

MIT License - Copyright (c) 2026
