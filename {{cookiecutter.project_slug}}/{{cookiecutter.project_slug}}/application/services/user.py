"""{{cookiecutter.project_name}} - Application - Services - User"""
from typing import Optional

from fastapi import HTTPException

from {{cookiecutter.project_slug}}.application.schemas.users.requests import CreateUserSchema, ReplaceUserSchema
from {{cookiecutter.project_slug}}.application.services.token import TokenService
from {{cookiecutter.project_slug}}.domain.entities.users import User
from {{cookiecutter.project_slug}}.domain.infrastructure.repositories.users import UserRepository


class UserService:
    """User Service"""

    def __init__(
        self,
        token_service: TokenService,
        user_repository: UserRepository,
    ):
        self.token_service: TokenService = token_service
        self.user_repository: UserRepository = user_repository

    async def create(self, user_data: CreateUserSchema):
        """Create"""
        return User(
            **(
                await self.user_repository.create_or_replace_user(
                    username=user_data.username,
                    password=self.token_service.hash_password(plain_password=user_data.password),
                    full_name=user_data.full_name,
                    email=user_data.email,
                )
            )
        )

    async def read_all(self):
        """Read all"""
        return [User(**user) for user in await self.user_repository.find()]

    async def read_by_username(self, username: str, current_user: Optional[User] = None):
        """Read by username"""
        user = await self.user_repository.get_by_username(username)

        if current_user and user != current_user and not current_user.is_superuser:
            raise HTTPException(
                status_code=400,
                detail="The user doesn't have enough privileges",
            )

        return User(**user)

    async def read_by_email(self, email: str, current_user: Optional[User] = None):
        """Read by email"""
        user = await self.user_repository.get_by_email(email)

        if current_user and user != current_user and not current_user.is_superuser:
            raise HTTPException(
                status_code=400,
                detail="The user doesn't have enough privileges",
            )

        return User(**user)

    async def replace(self, username: str, user_data: ReplaceUserSchema):
        """Replace"""
        return User(
            **(
                await self.user_repository.create_or_replace_user(
                    username=username,
                    password=self.token_service.hash_password(plain_password=user_data.password),
                    full_name=user_data.full_name,
                    email=user_data.email,
                )
            )
        )

    async def delete(self, username: str):
        """Delete"""
        return await self.user_repository.delete_by_username(username)
