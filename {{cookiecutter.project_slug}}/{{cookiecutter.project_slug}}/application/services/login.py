"""{{cookiecutter.project_name}} - Application - Services - Login"""
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError

from {{cookiecutter.project_slug}}.application.schemas.tokens.requests import TokenSchema
from {{cookiecutter.project_slug}}.application.schemas.users.requests import ReplaceUserSchema
from {{cookiecutter.project_slug}}.application.services.token import TokenService
from {{cookiecutter.project_slug}}.application.services.user import UserService
from {{cookiecutter.project_slug}}.domain.entities.users import User
from {{cookiecutter.project_slug}}.infrastructure.smtp_client import SMTPClient


class LoginService:
    """Login Service"""

    reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/login/access-token")

    def __init__(
        self,
        token_service: TokenService,
        user_service: UserService,
        smtp_client: SMTPClient,
    ):
        self.token_service: TokenService = token_service
        self.user_service: UserService = user_service
        self.smtp_client: SMTPClient = smtp_client

    async def authenticate(self, username: str, plain_password: str):
        """Authenticate"""
        user: User = await self.user_service.read_by_username(username)

        if (
            not user
            or not self.token_service.verify_password(plain_password, user.hashed_password)
            or not user.is_active
        ):
            raise HTTPException(400, "Inactive or incorrect email or password")

        return self.token_service.encode(user=user)

    async def password_recovery(self, email: str):
        """Password recovery"""
        user = await self.user_service.read_by_email(email)
        password_reset_token = self.token_service.encode(user=user, ephemeral=True)

        await self.smtp_client.send_email(
            email_to=[user.email],
            subject=f"Recover password for email {email}",
            text=f"This is your url to reset password: "
            f"http://localhost:8080/api/reset-password?token={password_reset_token}",
        )

        return {"msg": "Password recovery email sent"}

    async def reset_password(self, current_user: User, new_password: str):
        """Reset password"""
        return await self.user_service.replace(
            current_user.username,
            ReplaceUserSchema(
                password=new_password,
                full_name=current_user.full_name,
                email=current_user.email,
            ),
        )

    async def get_current_user(self, token: str):
        """Get current user"""
        try:
            token_payload = self.token_service.decode(token)
            token = TokenSchema(**token_payload)
        except (jwt.JWTError, ValidationError) as exc:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
            ) from exc

        user = await self.user_service.read_by_username(token.user.username)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user

    async def get_current_active_user(self, token: str):
        """Get current active user"""
        current_user: User = await self.get_current_user(token)

        if not current_user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")

        return current_user

    async def get_current_active_superuser(self, token: str):
        """Get current active superuser"""
        current_user: User = await self.get_current_user(token)

        if not current_user.is_active or not current_user.is_superuser:
            raise HTTPException(status_code=400, detail="The user doesn't have enough privileges")

        return current_user
