"""{{cookiecutter.project_name}} - Domain - Base - Repositories"""
from abc import ABC, abstractmethod


class Repository(ABC):
    """Repository"""

    @abstractmethod
    def create(self, data: dict) -> None:
        """Create"""

    @abstractmethod
    def read(self) -> list:
        """Read"""

    @abstractmethod
    def read_by_code(self, code: str) -> dict:
        """Read by code"""

    @abstractmethod
    def read_by_username(self, username: str) -> dict:
        """Read by username"""

    @abstractmethod
    def update(self, username: str, patient_code: str):
        """Update"""

    @abstractmethod
    def delete(self):
        """Delete"""


class AsyncRepository(ABC):
    """Repository"""

    @abstractmethod
    async def create(self, data: dict) -> None:
        """Create"""

    @abstractmethod
    async def read(self) -> list:
        """Read"""

    @abstractmethod
    async def read_by_code(self, code: str) -> dict:
        """Read by code"""

    @abstractmethod
    async def read_by_username(self, username: str) -> dict:
        """Read by username"""

    @abstractmethod
    async def update(self):
        """Update"""

    @abstractmethod
    async def delete(self):
        """Delete"""
