from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from src.utils.request_context import request_context

_ALLOWED = ("iso", "custom")
_DEFAULT = "custom"


class DateFormatMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        value = request.query_params.get("date_format", _DEFAULT)
        if value not in _ALLOWED:
            value = _DEFAULT
        request_context.set("date_format", value)
        return await call_next(request)
