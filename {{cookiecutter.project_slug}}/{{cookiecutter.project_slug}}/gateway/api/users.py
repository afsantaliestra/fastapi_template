"""{{cookiecutter.project_name}} - Gateway - Api - Users"""
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, Path
from pydantic import StrictStr

from {{cookiecutter.project_slug}}.application.schemas.users.requests import CreateUserSchema, ReplaceUserSchema
from {{cookiecutter.project_slug}}.application.services.user import UserService
from {{cookiecutter.project_slug}}.containers import ApplicationContainer
from {{cookiecutter.project_slug}}.gateway import deps

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/")
async def read_users(
    _current_user=Depends(deps.get_current_active_superuser),
    user_service: UserService = Depends(Provide[ApplicationContainer.services.user_service]),
):
    """Read users"""
    return await user_service.read_all()


@router.post("/")
@inject
async def create_user(
    user_data: CreateUserSchema = Body(...),
    user_service: UserService = Depends(Provide[ApplicationContainer.services.user_service]),
):
    """Create user"""
    return await user_service.create(user_data)


@router.get("/me")
async def read_user_me(
    current_user=Depends(deps.get_current_active_user),
):
    """Read user me"""
    return current_user


@router.put("/me")
@inject
async def replace_user_me(
    user_data: ReplaceUserSchema = Body(...),
    current_user=Depends(deps.get_current_active_user),
    user_service: UserService = Depends(Provide[ApplicationContainer.services.user_service]),
):
    """Update user me"""
    return await user_service.replace(current_user.username, user_data)


@router.get("/{username}")
@inject
async def read_user_by_username(
    username: StrictStr = Path(...),
    current_user=Depends(deps.get_current_active_user),
    user_service: UserService = Depends(Provide[ApplicationContainer.services.user_service]),
):
    """Read user by id"""
    return await user_service.read_by_username(current_user=current_user, username=username)


@router.put("/{username}")
@inject
async def replace_user_by_username(
    username: StrictStr = Path(...),
    user_data: ReplaceUserSchema = Body(...),
    _current_user=Depends(deps.get_current_active_superuser),
    user_service: UserService = Depends(Provide[ApplicationContainer.services.user_service]),
):
    """Update user by username"""
    return await user_service.replace(username, user_data)


@router.delete("/{username}")
@inject
async def delete_user_by_username(
    username: StrictStr = Path(...),
    _current_user=Depends(deps.get_current_active_superuser),
    user_service: UserService = Depends(Provide[ApplicationContainer.services.user_service]),
):
    """Delete user by username"""
    return await user_service.delete(username=username)
