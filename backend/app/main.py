from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import auth, users, skills, sessions, bookings, skill_tags, google_auth
from .db.session import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SkillSwap Hub API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(google_auth.router, prefix="/auth", tags=["google-auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(skills.router, prefix="/skills", tags=["skills"])
app.include_router(sessions.router, prefix="/sessions", tags=["sessions"])
app.include_router(bookings.router, prefix="/bookings", tags=["bookings"])
app.include_router(skill_tags.router, prefix="/skill-tags", tags=["skill-tags"])

@app.get("/")
def read_root():
    return {"message": "SkillSwap Hub API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
