"""{{cookiecutter.project_name}} - Domain - Entities - Users"""
from dataclasses import dataclass
from typing import Optional
from uuid import UUID, uuid4

from {{cookiecutter.project_slug}}.domain.base.entities import Entity


@dataclass
class User(Entity):
    """User"""

    username: str
    hashed_password: str

    code: UUID = uuid4()
    full_name: Optional[str] = None
    email: Optional[str] = None
    is_active: bool = True
    is_superuser: bool = True
