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

1. Clone the repository
2. Create virtual environment: `python3 -m venv venv`
3. Install dependencies: `venv/bin/pip install -r requirements.txt`
4. Seed database: `venv/bin/python seed.py`
5. Run application: `venv/bin/python app.py`

## API Endpoints

- `GET /heroes` - List all heroes
- `GET /heroes/:id` - Get hero with powers
- `GET /powers` - List all powers
- `GET /powers/:id` - Get specific power
- `PATCH /powers/:id` - Update power description
- `POST /hero_powers` - Create hero-power association

## Technologies Used

- React 
- Python 3.12
- Flask 2.3.3
- SQLAlchemy (Flask-SQLAlchemy 3.0.5)
- SQLite Database

## Contact

Moringa School Software Engineers

## License

MIT License - Copyright (c) 2026
