import os
from pathlib import Path

class Settings:
    def __init__(self):
        # Determine backend directory (three levels up from this file: core -> app -> backend)
        backend_dir = Path(__file__).resolve().parents[2]
        default_sqlite_path = backend_dir / "skillswap.db"

        # Database configuration with environment override
        self.database_url: str = os.getenv("DATABASE_URL", f"sqlite:///{default_sqlite_path}")

        # Security settings with environment overrides
        self.secret_key: str = os.getenv(
            "SECRET_KEY",
            "your-secret-key-change-in-production-09876543210987654321",
        )
        self.algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
        self.access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
        self.refresh_token_expire_days: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

settings = Settings()
