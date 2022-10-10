"""{{cookiecutter.project_name}} - Utils"""
import contextvars
import types

global_request_context = contextvars.ContextVar(
    "global_request_context",
    default=types.SimpleNamespace(),
)
