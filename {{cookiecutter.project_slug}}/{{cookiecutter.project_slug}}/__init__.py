"""{{cookiecutter.project_name}} - Init"""
from typing import Optional, Sequence, Type

import toml
from dependency_injector.containers import DeclarativeContainer
from fastapi import Depends, FastAPI

from {{cookiecutter.project_slug}}.containers import ApplicationContainer
from {{cookiecutter.project_slug}}.gateway.api import connectivity, login, users
from {{cookiecutter.project_slug}}.gateway.middlewares import request_middleware


class API(FastAPI):
    """API"""

    container: Type[DeclarativeContainer]

    def __init__(
        self,
        *,
        title: Optional[str] = None,
        pyproject_path: Optional[str] = None,
        container: Optional[Type[DeclarativeContainer]] = None,
        dependencies: Optional[Sequence[Depends]] = None
    ):
        _pyproject = toml.load(pyproject_path or "pyproject.toml")

        super().__init__(
            title=title or self.__doc__,
            description=_pyproject["tool"]["poetry"]["description"],
            version=_pyproject["tool"]["poetry"]["version"],
            dependencies=dependencies,
        )

        self.include_router(connectivity.router)

        self.container = container


app = API(
    title="{{cookiecutter.project_name}}",
    container=ApplicationContainer(),
)

app.middleware("http")(request_middleware)

app.include_router(users.router, prefix="/api")
app.include_router(login.router, prefix="/api")
