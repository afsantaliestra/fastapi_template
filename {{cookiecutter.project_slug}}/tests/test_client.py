"""{{cookiecutter.project_name}} - Tests - Test Client"""
from typing import Optional, Union

from fastapi.testclient import TestClient
from requests.models import Response
from starlette.testclient import ASGI2App, ASGI3App


class FastAPITestClient(TestClient):
    """FastAPI Test Client"""

    def __init__(self, app: Union[ASGI2App, ASGI3App]):
        super().__init__(app)

    def _assert_response(
        self,
        response: Response,
        status_code_expected: int = None,
    ) -> Response:
        """Assert response"""
        assert response.status_code == (status_code_expected or 200)
        assert response.headers.get("X-Request-Id") is not None
        assert response.headers.get("X-Process-Time") is not None

        return response

    def get(
        self,
        url: str,
        *,
        status_code_expected: int = None,
        **kwargs,
    ) -> Response:
        """Get"""
        return self._assert_response(
            response=super().get(url, **kwargs),
            status_code_expected=status_code_expected,
        )

    def post(
        self,
        url: str,
        data: Optional[dict] = None,
        json: Optional[dict] = None,
        *,
        status_code_expected: int = None,
        **kwargs,
    ):
        """Post"""
        return self._assert_response(
            response=super().post(
                url,
                data=data,
                json=json,
                **kwargs,
            ),
            status_code_expected=status_code_expected,
        )
