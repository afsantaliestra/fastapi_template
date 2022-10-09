"""{{cookiecutter.project_name}} - Domain - Infrastructure - Users"""  # pylint: disable=duplicate-code
from abc import ABC, abstractmethod
from typing import Optional


class UserRepository(ABC):
    """User Repository"""

    @abstractmethod
    async def create_or_replace_user(
        self,
        username: str,
        password: str,
        full_name: Optional[str],
        email: Optional[str],
    ):
        """Create or replace user"""

    @abstractmethod
    async def find(self):
        """Find"""

    @abstractmethod
    async def get_by_username(self, username: str):
        """Get by username"""

    @abstractmethod
    async def get_by_email(self, email: str):
        """Get by email"""

    @abstractmethod
    async def delete_by_username(self, username: str):
        """Delete by username"""
