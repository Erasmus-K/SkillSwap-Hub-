from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import auth, skills
from app.db.database import engine
from app.db.database import Base


# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SkillSwap Hub API",
    description="A peer-to-peer micro-learning platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(skills.router, prefix="/skills", tags=["skills"])

@app.get("/")
def read_root():
    return {"message": "Welcome to SkillSwap Hub API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import auth, users, skills, sessions, bookings
from .db.session import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SkillSwap Hub API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(skills.router, prefix="/skills", tags=["skills"])
app.include_router(sessions.router, prefix="/sessions", tags=["sessions"])
app.include_router(bookings.router, prefix="/bookings", tags=["bookings"])

@app.get("/")
def read_root():
    return {"message": "SkillSwap Hub API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}