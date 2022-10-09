"""{{cookiecutter.project_name}} - Application - Schemas - Tokens - Requests"""
from pydantic import BaseModel


class JWTUserSchema(BaseModel):
    """JWT User Schema"""

    username: str
    email: str


class TokenSchema(BaseModel):
    """Token Schema"""

    user: JWTUserSchema
    nbf: int
    exp: int
