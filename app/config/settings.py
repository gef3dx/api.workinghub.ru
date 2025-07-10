from dataclasses import dataclass
from os import getenv
from pathlib import Path


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
    secret_key: str = getenv("SECRET_KEY", "secret-key")


# Singleton instance
settings = Settings()
