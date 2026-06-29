from fastapi import FastAPI
from starlette.middleware.gzip import GZipMiddleware
from .request_logger import RequestLoggerMiddleware
from .date_format_middleware import DateFormatMiddleware
from .external_api_middleware import ExternalApiMiddleware


def setup_middlewares(app: FastAPI):
    app.add_middleware(GZipMiddleware, minimum_size=500)
    app.add_middleware(RequestLoggerMiddleware)
    app.add_middleware(DateFormatMiddleware)
    app.add_middleware(ExternalApiMiddleware)
