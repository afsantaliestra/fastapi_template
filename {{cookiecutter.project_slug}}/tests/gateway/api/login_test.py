"""{{cookiecutter.project_name}} - Tests - Gateway - API - Users"""
import unittest

import pytest
from requests.models import Response

from {{cookiecutter.project_slug}}.application.services.login import LoginService
from {{cookiecutter.project_slug}}.domain.entities.users import User
from tests.test_client import FastAPITestClient


@pytest.mark.parametrize(
    "login_data",
    [
        None,
        {},
        {"username": None},
        {"username": ""},
        {"password": None},
        {"password": ""},
        {"username": None, "password": None},
        {"username": "", "password": ""},
        {"username": None, "password": ""},
        {"username": "", "password": None},
    ],
)
def test_login_access_token_missing_information(
    test_client: FastAPITestClient,
    login_data: dict,
) -> None:
    """Test login access token missing information"""
    response: Response = test_client.post(
        "/api/login/access-token",
        status_code_expected=422,
        json=login_data
    )

    for error in response.json()["detail"]:
        assert (error["loc"] == ["body", "username"]) or (error["loc"] == ["body", "password"])


def test_login_access_token(test_client: FastAPITestClient) -> None:
    """Test login access token"""
    login_service_mock = unittest.mock.Mock(LoginService)
    login_service_mock.authenticate.return_value = "123456789abcdef"

    with test_client.app.container.services.login_service.override(login_service_mock):
        response: Response = test_client.post(
            "/api/login/access-token",
            data={"username": "real_username", "password": "real_password"},
        )
    response_body = response.json()
    assert response_body["access_token"] == "123456789abcdef"
    assert response_body["token_type"] == "bearer"


@pytest.mark.parametrize(
    "headers",
    [
        None,
        {},
        {"Authorization": None},
        {"Authorization": ""},
    ],
)
def test_test_token_missing_information(
    test_client: FastAPITestClient,
    headers: dict,
) -> None:
    """Test test token missing token"""
    response: Response = test_client.post(
        "/api/login/test-token",
        status_code_expected=401,
        headers=headers,
    )

    assert response.json()["detail"] == "Not authenticated"


def test_test_token(
    test_client: FastAPITestClient,
    user: User,
) -> None:
    """Test test token"""
    login_service_mock = unittest.mock.Mock(LoginService)
    login_service_mock.get_current_active_user.return_value = user

    with test_client.app.container.services.login_service.override(login_service_mock):
        response: Response = test_client.post(
            "/api/login/test-token",
            headers={"Authorization": "bearer 123456789abcdef"},
        )

    response_body = response.json()
    assert response_body.get("code")
    assert response_body["username"] == user.username


@pytest.mark.parametrize(
    "email",
    [
        None,
        "",
    ],
)
def test_recover_password_missing_information(
    test_client: FastAPITestClient,
    email: str,
) -> None:
    """Test test token missing token"""
    response: Response = test_client.post(
        f"/api/password-recovery/{email or ''}",
        status_code_expected=404,
    )

    assert response.json()["detail"] == "Not Found"


def test_recover_password(
    test_client: FastAPITestClient,
    user: User,
) -> None:
    """Test test token missing token"""
    login_service_mock = unittest.mock.Mock(LoginService)
    login_service_mock.password_recovery.return_value = expected_return = {
        "msg": "Password recovery email sent"
    }

    with test_client.app.container.services.login_service.override(login_service_mock):
        response: Response = test_client.post(f"/api/password-recovery/{user.email or ''}")

    assert response.json() == expected_return


def test_reset_password_missing_information(
    test_client: FastAPITestClient,
) -> None:
    """Test test token missing token"""
    login_service_mock = unittest.mock.Mock(LoginService)
    login_service_mock.reset_password.return_value = expected_return = {
        "msg": "Password updated successfully"
    }

    with test_client.app.container.services.login_service.override(login_service_mock):
        response: Response = test_client.post(
            "/api/reset-password/",
            params={
                "token": "bearer 123456789abcdef",
            },
            data={
                "new_password": "test_password_2",
            },
        )

    assert response.json() == expected_return
