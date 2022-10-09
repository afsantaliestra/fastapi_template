"""{{cookiecutter.project_name}} - Application - Schemas - Tokens - Responses"""
from pydantic import BaseModel, Field


class JWTSchema(BaseModel):
    """JWT Schema"""

    access_token: str = Field(...)
    token_type: str = Field("bearer")
