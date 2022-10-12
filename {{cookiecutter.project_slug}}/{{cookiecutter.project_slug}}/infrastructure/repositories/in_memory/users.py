"""{{cookiecutter.project_name}} - Infrastructure - Repositories - In Memory - Users"""
from typing import Optional

from {{cookiecutter.project_slug}}.domain.base.repositories import ABCAsyncRepository
from {{cookiecutter.project_slug}}.infrastructure.repositories.exceptions import UserNotFoundException


class UserRepository(ABCAsyncRepository):
    """User Repository"""

    def __init__(self):
        """Init"""
        self.data = {}

    async def create_or_replace_user(
        self,
        username: str,
        password: str,
        full_name: Optional[str],
        email: Optional[str],
    ):
        """Create or replace user"""
        self.data[username] = {
            "username": username,
            "hashed_password": password,
            "full_name": full_name,
            "email": email,
        }
        return self.data[username]

    async def find(self):
        """Find"""
        return self.data.values()

    async def get_by_username(self, username: str):
        """Get by username"""
        if user := self.data.get(username):
            return user

        raise UserNotFoundException(username)

    async def get_by_email(self, email: str):
        """Get by email"""
        for user in self.data.values():
            if user["email"] == email:
                return user

        raise UserNotFoundException(email)

    async def delete_by_username(self, username: str):
        """Delete by username"""
        if username not in self.data:
            raise UserNotFoundException(username)

        del self.data[username]
        return True
