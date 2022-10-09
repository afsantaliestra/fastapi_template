"""{{cookiecutter.project_name}} - Infrastructure - Repositories - In Memory - Users"""
from typing import Optional

from {{cookiecutter.project_slug}}.domain.base.repositories import ABCAsyncRepository


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
        self.data[username] = data = {
            "username": username,
            "hashed_password": password,
            "full_name": full_name,
            "email": email,
        }
        return data

    async def find(self):
        """Find"""
        return self.data.values()

    async def get_by_username(self, username: str):
        """Get by username"""
        return self.data.get(username)

    async def get_by_email(self, email: str):
        """Get by email"""
        for user in self.data.values():
            if user["email"] == email:
                return user

        return None

    async def delete_by_username(self, username: str):
        """Delete by username"""
        if username not in self.data:
            return False

        del self.data[username]
        return True
