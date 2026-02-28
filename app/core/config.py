# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import EmailStr, PostgresDsn  # optional, using PostgreSQL
from typing import Optional, Any


class Settings(BaseSettings):
    # ─────────────────────────────────────────────────────────────
    # App general config
    # ─────────────────────────────────────────────────────────────
    PROJECT_NAME: str = "Financial App"
    PROJECT_DESCRIPTION: str = "App para gestión financiera personal"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    # ─────────────────────────────────────────────────────────────
    # Environment (development, production, testing)
    # ─────────────────────────────────────────────────────────────
    ENVIRONMENT: str = "development"  # Change tp "production" in prod

    # ─────────────────────────────────────────────────────────────
    # Security / JWT
    # ─────────────────────────────────────────────────────────────
    SECRET_KEY: str = "tu-clave-secreta-super-larga-y-random-aqui"  # ¡Change!
    # eg: Generate one with: openssl rand -hex 32
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 días
    ALGORITHM: str = "HS256"

    # ─────────────────────────────────────────────────────────────
    # Data base (eg PostgreSQL, change base in use)
    # ─────────────────────────────────────────────────────────────
    DATABASE_URL: PostgresDsn | str = "postgresql+psycopg://user:password@localhost:5432/financial_db"
    # or SQLite para dev: "sqlite:///./dev.db"

    # ─────────────────────────────────────────────────────────────
    # Others common config (add as needed)
    # ─────────────────────────────────────────────────────────────
    FIRST_SUPERUSER_EMAIL: EmailStr = "admin@example.com"
    FIRST_SUPERUSER_PASSWORD: str = "supersecret"
    BACKEND_CORS_ORIGINS: list[str] | str = ["http://localhost:3000", "http://127.0.0.1:3000"]

    # You can allow all in dev (¡not in production!)
    # BACKEND_CORS_ORIGINS: str = "*"

    model_config = SettingsConfigDict(
        env_file=".env",              # auto reading .env
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",               # ignore extra vars in .env
    )


# Global instance used in the whole project
settings = Settings()