"""{{cookiecutter.project_name}} - Gateway - Deps"""
from dependency_injector.wiring import Provide, inject
from fastapi import Depends, Query

from {{cookiecutter.project_slug}}.application.services.login import LoginService
from {{cookiecutter.project_slug}}.containers import ApplicationContainer


@inject
async def get_current_active_user(
    token: str = Depends(LoginService.reusable_oauth2),
    login_service: LoginService = Depends(Provide[ApplicationContainer.services.login_service]),
):
    """Get current active user"""
    return await login_service.get_current_active_user(token)


@inject
async def get_current_active_user_query(
    token: str = Query(...),
    login_service: LoginService = Depends(Provide[ApplicationContainer.services.login_service]),
):
    """Get current active user"""
    return await login_service.get_current_active_user(token)


@inject
async def get_current_active_superuser(
    token: str = Depends(LoginService.reusable_oauth2),
    login_service: LoginService = Depends(Provide[ApplicationContainer.services.login_service]),
):
    """Get current active superuser"""
    return await login_service.get_current_active_superuser(token)
