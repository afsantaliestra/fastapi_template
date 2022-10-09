"""{{cookiecutter.project_name}} - Application - Schemas - Users - Requests"""
from pydantic import BaseModel, Field, StrictStr
from pydantic.networks import EmailStr


class ReplaceUserSchema(BaseModel):
    """Replace User Schema"""

    password: StrictStr = Field(...)
    full_name: StrictStr = Field(None)
    email: EmailStr = Field(None)


class CreateUserSchema(ReplaceUserSchema):
    """Create User Schema"""

    username: StrictStr = Field(..., min_length=5)
