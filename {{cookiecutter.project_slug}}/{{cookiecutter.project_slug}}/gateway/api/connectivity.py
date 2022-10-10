"""{{cookiecutter.project_name}} - Gateway - API - Connectivity"""
from fastapi import APIRouter
from starlette.responses import RedirectResponse

from {{cookiecutter.project_slug}}.application.schemas.connectivity import HeartbeatResponseSchema

router = APIRouter(tags=["Connectivity"])


@router.get("/")
def root_path() -> RedirectResponse:
    """Root path"""
    return RedirectResponse("/docs")


@router.get(
    "/heartbeat",
    status_code=200,
    response_model=HeartbeatResponseSchema,
    responses={
        200: {
            "description": "Heartbeat response",
            "content": {"application/json": {"example": {"status": "ok"}}},
        },
    },
)
async def heartbeat() -> HeartbeatResponseSchema:
    """Heartbeat"""
    return HeartbeatResponseSchema(status="ok")
