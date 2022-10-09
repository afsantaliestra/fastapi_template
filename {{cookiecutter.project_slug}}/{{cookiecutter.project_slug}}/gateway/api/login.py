"""{{cookiecutter.project_name}} - Gateway - Api - Login"""
from typing import Any

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends
from fastapi.security import OAuth2PasswordRequestForm

from {{cookiecutter.project_slug}}.application.services.login import LoginService
from {{cookiecutter.project_slug}}.containers import ApplicationContainer
from {{cookiecutter.project_slug}}.gateway import deps

router = APIRouter(tags=["Login"])


@router.post("/login/access-token", response_model=dict)
@inject
async def login_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    login_service: LoginService = Depends(Provide[ApplicationContainer.services.login_service]),
) -> Any:
    """OAuth2 compatible token login, get an access token for future requests"""
    return {
        "access_token": await login_service.authenticate(
            username=form_data.username,
            plain_password=form_data.password,
        ),
        "token_type": "bearer",
    }


@router.post("/login/test-token", response_model=dict)
async def test_token(
    current_user=Depends(deps.get_current_active_user),
) -> Any:
    """Test access token"""
    return current_user


@router.post("/password-recovery/{email}", response_model=dict)
@inject
async def recover_password(
    email: str,
    login_service: LoginService = Depends(Provide[ApplicationContainer.services.login_service]),
) -> Any:
    """Recover password"""
    return await login_service.password_recovery(email)


@router.post("/reset-password/", response_model=dict)
@inject
async def reset_password(
    new_password: str = Body(...),
    current_user=Depends(deps.get_current_active_user_query),
    login_service: LoginService = Depends(Provide[ApplicationContainer.services.login_service]),
) -> Any:
    """Reset password"""
    await login_service.reset_password(current_user, new_password)
    return {"msg": "Password updated successfully"}
