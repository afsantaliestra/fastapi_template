"""{{cookiecutter.project_name}} - Tests - Gateway - API - Connectivity"""
from requests.models import Response

from tests.test_client import FastAPITestClient


def test_root_path(test_client: FastAPITestClient) -> None:
    """Test root path"""
    test_client.get("/")


def test_heartbeat(test_client: FastAPITestClient) -> None:
    """Test heartbeat"""
    response: Response = test_client.get("/heartbeat")

    assert response.json() == {"status": "ok"}
