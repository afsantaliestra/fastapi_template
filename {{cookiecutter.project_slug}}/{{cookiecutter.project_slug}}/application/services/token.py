"""{{cookiecutter.project_name}} - Application - Services - Token"""
from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from {{cookiecutter.project_slug}}.domain.entities.users import User

EMAIL_RESET_TOKEN_EXPIRE_HOURS = 1


class TokenService:
    """Token Service"""

    def __init__(
        self,
        algorithm,
        secret_key,
        token_expiration,
        reset_password_token_expiration,
    ):
        self.algorithm = algorithm
        self.secret_key = secret_key
        self.token_expiration = token_expiration
        self.reset_password_token_expiration = reset_password_token_expiration
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def encode(self, user: User, ephemeral: bool = None) -> str:
        """Encode"""
        now = datetime.utcnow()
        return jwt.encode(
            {
                "user": {"username": user.username, "email": user.email},
                "nbf": now.timestamp(),
                "exp": (
                    now
                    + timedelta(
                        minutes=self.reset_password_token_expiration
                        if ephemeral
                        else self.token_expiration
                    )
                ).timestamp(),
            },
            key=self.secret_key,
            algorithm=self.algorithm,
        )

    def decode(self, token: str) -> dict[str, str]:
        """Decode"""
        return jwt.decode(
            token=token,
            key=self.secret_key,
            algorithms=self.algorithm,
        )

    def hash_password(self, plain_password: str):
        """Hash Password"""
        return self.pwd_context.hash(
            secret=plain_password,
        )

    def verify_password(self, plain_password: str, hashed_password: str):
        """Verify password"""
        return self.pwd_context.verify(
            secret=plain_password,
            hash=hashed_password,
        )
