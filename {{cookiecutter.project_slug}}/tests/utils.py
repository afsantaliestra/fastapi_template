"""{{cookiecutter.project_name}} - Tests - Utils"""
from requests.models import Response


def assert_response(
    response: Response,
    status_code: int = None,
) -> Response:
    """Assert response"""
    assert response.status_code == (status_code or 200)
    assert response.headers.get("X-Request-Id") is not None
    assert response.headers.get("X-Process-Time") is not None

    return response
