"""{{cookiecutter.project_name}} - Tests - Gateway - API - Connectivity"""
from requests.models import Response
from tests.utils import assert_response


def test_root_path(test_client):
    """Test root path"""
    assert_response(test_client.get("/"))


def test_heartbeat(test_client):
    """Test heartbeat"""
    response: Response = assert_response(test_client.get("/heartbeat"))

    assert response.json() == {"status": "ok"}
