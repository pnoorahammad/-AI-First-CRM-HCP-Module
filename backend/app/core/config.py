"""
Application configuration loaded from environment variables.
"""

from pydantic_settings import BaseSettings
from pydantic import model_validator
from sqlalchemy.engine import URL


class Settings(BaseSettings):
    """Application settings loaded from .env file."""

    # Database — can supply either a full URL or individual credentials
    DATABASE_URL: str = ""
    DB_HOST: str = ""
    DB_PORT: int = 5432
    DB_NAME: str = "postgres"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = ""

    # Supabase HTTPS API
    SUPABASE_URL: str = ""
    SUPABASE_ANON_KEY: str = ""
    SUPABASE_SERVICE_ROLE_KEY: str = ""

    # Security
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    # Groq AI
    GROQ_API_KEY: str = ""
    LLM_MODEL: str = "gemma2-9b-it"

    # CORS
    FRONTEND_URL: str = "http://localhost:5173"

    # Environment
    ENVIRONMENT: str = "development"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
    }

    @model_validator(mode="after")
    def build_database_url(self) -> "Settings":
        """If DATABASE_URL is empty, build it from individual DB_* credentials."""
        if not self.DATABASE_URL and self.DB_HOST:
            url = URL.create(
                drivername="postgresql+psycopg2",
                username=self.DB_USER,
                password=self.DB_PASSWORD,  # SQLAlchemy handles encoding internally
                host=self.DB_HOST,
                port=self.DB_PORT,
                database=self.DB_NAME,
            )
            self.DATABASE_URL = str(url)
        elif not self.DATABASE_URL:
            # Fallback to SQLite for local dev if nothing configured
            self.DATABASE_URL = "sqlite:///./crm.db"
        return self

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"

    @property
    def is_sqlite(self) -> bool:
        return self.DATABASE_URL.startswith("sqlite")


settings = Settings()
