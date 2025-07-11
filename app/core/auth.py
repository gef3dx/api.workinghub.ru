from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config.settings import settings
from app.models.schemas.auth import TokenDataSchema


class AuthManager:
    """Authentication manager."""

    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 30

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password."""
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        """Get password hash."""
        return self.pwd_context.hash(password)

    def create_access_token(
        self, data: dict, expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create access token."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=self.access_token_expire_minutes
            )

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.secret_key, algorithm=self.algorithm
        )
        return encoded_jwt

    def verify_token(self, token: str) -> Optional[TokenDataSchema]:
        """Verify token."""
        try:
            payload = jwt.decode(
                token, settings.secret_key, algorithms=[self.algorithm]
            )
            username: str = payload.get("sub")
            user_id: int = payload.get("user_id")

            if username is None or user_id is None:
                return None

            return TokenDataSchema(username=username, user_id=user_id)
        except JWTError:
            return None


# Singleton instance
auth_manager = AuthManager()
