<<<<<<< HEAD
import os
from typing import Optional

class Settings:
    database_url: str = "sqlite:///./skillswap.db"
    secret_key: str = "your-secret-key-change-in-production-09876543210987654321"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

settings = Settings()
=======
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
>>>>>>> 8cabe45 (Created skill.py file to add new new skill)
