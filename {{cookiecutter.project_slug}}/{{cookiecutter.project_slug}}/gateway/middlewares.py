"""{{cookiecutter.project_name}} - Gateway - Middlewares"""
import time
from typing import Callable
from uuid import uuid4

from fastapi import Request, Response

from {{cookiecutter.project_slug}}.utils import global_request_context


async def request_middleware(request: Request, call_next: Callable):
    """Request Middleware"""
    start_time = time.time()
    request_id = request.headers.get("X-Request-Id", uuid4().hex)
    global_request_context.set({"request_id": request_id})

    response: Response = await call_next(request)

    response.headers["X-Process-Time"] = str(time.time() - start_time)
    response.headers["X-Request-Id"] = request_id

    return response
