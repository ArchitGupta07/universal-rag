from uuid import uuid4
from starlette.middleware.base import BaseHTTPMiddleware
import time
from src.utils.logger import setup_logger
from fastapi import Request
from src.config.app_config import APP_CONFIG

logger = setup_logger(__name__)


class RequestLoggerMiddleware(BaseHTTPMiddleware):
    @staticmethod
    def _safe_response_headers(response) -> dict:
        try:
            if hasattr(response.headers, "raw"):
                return {
                    k.decode("utf-8", errors="replace"): v.decode("utf-8", errors="replace")
                    for k, v in response.headers.raw
                }
            return dict(response.headers)
        except Exception:
            return {}

    async def dispatch(self, request: Request, call_next):
        correlation_id = str(uuid4())
        start_time = time.time()

        body = await request.body()
        logger.info(f"[{correlation_id}] {request.method} {request.url}")

        content_type = request.headers.get("content-type", "")
        skip_body_log = (
            not APP_CONFIG.ENABLE_REQUEST_BODY_LOGGING
            or "multipart/form-data" in content_type
            or "application/octet-stream" in content_type
            or "application/vnd.openxmlformats" in content_type
        )
        if not skip_body_log and body:
            try:
                logger.info(f"[{correlation_id}] Body: {body.decode('utf-8')}")
            except UnicodeDecodeError:
                logger.info(f"[{correlation_id}] Body: <binary, {len(body)} bytes>")

        response = await call_next(request)
        duration_ms = round((time.time() - start_time) * 1000, 3)

        logger.info(
            f"[{correlation_id}] {response.status_code} ({duration_ms}ms)"
        )
        return response
