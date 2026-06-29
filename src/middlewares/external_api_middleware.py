from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from src.utils.request_context import request_context


class ExternalApiMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        header_value = request.headers.get("x-is-external", "true").strip().lower()
        request_context.set("is_external_api", header_value == "true")
        return await call_next(request)
