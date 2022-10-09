"""{{cookiecutter.project_name}} - Gateway - Schemas - Connectivity"""
from pydantic import BaseModel, Field


class HeartbeatResponseSchema(BaseModel):
    """Heartbeat Response Schema"""

    status: str = Field(...)
