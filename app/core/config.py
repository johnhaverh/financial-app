# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import EmailStr, PostgresDsn  # Opcional, si usas PostgreSQL
from typing import Optional, Any


class Settings(BaseSettings):
    # ─────────────────────────────────────────────────────────────
    # Configuración general de la app
    # ─────────────────────────────────────────────────────────────
    PROJECT_NAME: str = "Financial App"
    PROJECT_DESCRIPTION: str = "App para gestión financiera personal"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    # ─────────────────────────────────────────────────────────────
    # Entorno (development, production, testing)
    # ─────────────────────────────────────────────────────────────
    ENVIRONMENT: str = "development"  # Cambia a "production" en prod

    # ─────────────────────────────────────────────────────────────
    # Seguridad / JWT
    # ─────────────────────────────────────────────────────────────
    SECRET_KEY: str = "tu-clave-secreta-super-larga-y-random-aqui"  # ¡CAMBIAR OBLIGATORIO!
    # Ejemplo: genera uno con: openssl rand -hex 32
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 días
    ALGORITHM: str = "HS256"

    # ─────────────────────────────────────────────────────────────
    # Base de datos (ejemplo con PostgreSQL, cambia según uses)
    # ─────────────────────────────────────────────────────────────
    DATABASE_URL: PostgresDsn | str = "postgresql+psycopg://user:password@localhost:5432/financial_db"
    # O si usas SQLite para dev: "sqlite:///./dev.db"

    # ─────────────────────────────────────────────────────────────
    # Otras configuraciones comunes (agrega las que necesites)
    # ─────────────────────────────────────────────────────────────
    FIRST_SUPERUSER_EMAIL: EmailStr = "admin@example.com"
    FIRST_SUPERUSER_PASSWORD: str = "supersecret"
    BACKEND_CORS_ORIGINS: list[str] | str = ["http://localhost:3000", "http://127.0.0.1:3000"]

    # Si quieres permitir todos en dev (¡no en producción!)
    # BACKEND_CORS_ORIGINS: str = "*"

    model_config = SettingsConfigDict(
        env_file=".env",              # Lee automáticamente .env
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",               # Ignora vars extras en .env
    )


# Instancia global que usarás en todo el proyecto
settings = Settings()