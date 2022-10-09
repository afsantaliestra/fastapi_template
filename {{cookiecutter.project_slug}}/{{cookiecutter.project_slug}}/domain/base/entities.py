"""{{cookiecutter.project_name}} - Domain - Base - Entities"""
from dataclasses import dataclass


@dataclass(slots=True)
class Entity:
    """Entity"""
