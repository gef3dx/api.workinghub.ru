from dataclasses import dataclass
from os import getenv
from pathlib import Path
import secrets


@dataclass(frozen=True)
class Settings:
    """Настройки проекта"""

    # Database
    database_url: str = getenv(
        "DATABASE_URL",
        f"sqlite+aiosqlite:///{Path(__file__).parent.parent.parent}/database.db",
    )

    # Server
    host: str = getenv("HOST", "127.0.0.1")
    port: int = int(getenv("PORT", "8000"))
    debug: bool = getenv("DEBUG", "False").lower() == "true"

    # Security
    secret_key: str = getenv("SECRET_KEY", secrets.token_urlsafe(32))

    # JWT
    jwt_algorithm: str = getenv("JWT_ALGORITHM", "HS256")
    jwt_expire_minutes: int = int(getenv("JWT_EXPIRE_MINUTES", "30"))


# Singleton instance
settings = Settings()
