"""{{cookiecutter.project_name}} - Tests - Conftest"""
import pytest

from {{cookiecutter.project_slug}} import app
from {{cookiecutter.project_slug}}.domain.entities.users import User
from tests.test_client import FastAPITestClient

@pytest.fixture
def test_client():
    """FastAPI Test Client fixture"""
    return FastAPITestClient(app)


@pytest.fixture
def user():
    """User fixture"""
    return User(
        username="test_username",
        hashed_password="test_hashed_password",
        email="test@email.com",
    )
