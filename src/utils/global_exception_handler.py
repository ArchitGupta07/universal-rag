from fastapi import Request, HTTPException
from starlette.responses import JSONResponse
from src.utils.logger import setup_logger
from src.utils.exceptions import (
    AppException,
    InvalidIdFormatError,
    EntityNotFoundError,
    BatchOperationError,
    ValidationError,
)

logger = setup_logger(__name__)

_STATUS_TITLES = {
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    409: "Conflict",
    422: "Unprocessable Entity",
    500: "Internal Server Error",
}


def global_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, HTTPException):
        logger.error(f"HTTP Exception: {exc.detail}", exc_info=True)
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "message": exc.detail,
                "statusCode": exc.status_code,
                "error": _STATUS_TITLES.get(exc.status_code, "Error"),
            },
        )

    if isinstance(exc, InvalidIdFormatError):
        logger.warning(f"Invalid ID format: {exc.entity_id}")
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": exc.message,
                "statusCode": 400,
                "error": "Bad Request",
                "details": exc.details,
            },
        )

    if isinstance(exc, EntityNotFoundError):
        logger.warning(f"{exc.entity_type} not found: {exc.entity_id}")
        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "message": exc.message,
                "statusCode": 404,
                "error": "Not Found",
                "details": exc.details,
            },
        )

    if isinstance(exc, BatchOperationError):
        logger.warning(f"Batch operation partial failure: {exc.message}")
        return JSONResponse(
            status_code=207,
            content={
                "success": False,
                "message": exc.message,
                "statusCode": 207,
                "error": "Partial Success",
                "details": exc.details,
            },
        )

    if isinstance(exc, ValidationError):
        logger.warning(f"Validation error: {exc.message}")
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": exc.message,
                "statusCode": 400,
                "error": "Validation Error",
                "details": exc.details,
            },
        )

    if isinstance(exc, AppException):
        logger.error(f"Application error: {exc.message}")
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": exc.message,
                "statusCode": 400,
                "error": "Bad Request",
                "details": exc.details,
            },
        )

    logger.error(f"Internal Server Error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": f"An unexpected error occurred: {exc}",
            "statusCode": 500,
            "error": "Internal Server Error",
        },
    )
