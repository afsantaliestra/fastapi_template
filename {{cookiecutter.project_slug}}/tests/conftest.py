"""{{cookiecutter.project_name}} - Tests - Conftest"""
from fastapi.testclient import TestClient
from pytest import fixture

from {{cookiecutter.project_slug}} import app


@fixture
def test_client():
    """FastAPI Test Client"""
    return TestClient(app)
