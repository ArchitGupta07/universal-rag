# FastAPI Boilerplate — Complete Setup Guide

This document enables any AI agent to recreate this exact FastAPI application structure from scratch. Follow each section in order. All code is production-ready and mirrors the actual project patterns.

---

## 1. Project Structure

```
my-fastapi-app/
├── src/
│   ├── main.py
│   ├── app.py
│   ├── routes.py
│   ├── containers.py
│   ├── config/
│   │   ├── __init__.py
│   │   ├── app_config.py
│   │   └── db_config.py
│   ├── controllers/
│   │   ├── __init__.py
│   │   ├── health.py
│   │   └── item.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── health.py
│   │   └── item.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── base_repository.py
│   │   └── item_repository.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── request/
│   │   │   ├── __init__.py
│   │   │   └── item.py
│   │   └── response/
│   │       ├── __init__.py
│   │       └── item.py
│   ├── db/
│   │   ├── __init__.py
│   │   └── db_manager.py
│   ├── middlewares/
│   │   ├── __init__.py
│   │   ├── middlewares.py
│   │   ├── request_logger.py
│   │   ├── date_format_middleware.py
│   │   └── external_api_middleware.py
│   └── utils/
│       ├── __init__.py
│       ├── logger.py
│       ├── exceptions.py
│       ├── global_exception_handler.py
│       ├── request_context.py
│       └── helper.py
├── .env
├── .env.example
└── pyproject.toml
```

---

## 2. Dependencies — `pyproject.toml`

```toml
[tool.poetry]
name = "my-fastapi-app"
version = "0.1.0"
description = "FastAPI boilerplate"
authors = ["Your Name <you@example.com>"]

[tool.poetry.dependencies]
python = "^3.11"
fastapi = "0.136.0"
uvicorn = {version = "0.30.3", extras = ["standard"]}
pydantic = "2.10.5"
pydantic-settings = "^2.0.0"
motor = "3.6.0"
pymongo = "4.9.0"
dependency-injector = "4.46.0"
python-dotenv = "^1.0.0"
psutil = "^6.0.0"
brotli = "^1.0.9"

[tool.poetry.dev-dependencies]
pytest = "^8.0.0"
pytest-asyncio = "0.23.8"
black = "24.4.2"
pylint = "3.2.6"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

Install: `poetry install`

---

## 3. Environment — `.env.example`

```env
# App
ENVIRONMENT=dev
PORT=8000
APP_NAME=MyFastAPIApp
LOG_LEVEL=INFO

# MongoDB
DATABASE_URI=mongodb://localhost:27017
DATABASE_NAME=myapp_db
MONGODB_MAX_POOL_SIZE=50
MONGODB_MIN_POOL_SIZE=5

# Redis (optional)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_DB=0
REDIS_ENABLED=false

# Compression
ENABLE_COMPRESSION=true
COMPRESSION_MIN_SIZE_BYTES=102400
COMPRESSION_LEVEL=6

# Migrations
AUTO_MIGRATE=true

# Request logging
ENABLE_REQUEST_BODY_LOGGING=false
```

Copy to `.env` and fill in real values.

---

## 4. Config — `src/config/app_config.py`

```python
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from typing import Optional

load_dotenv()


class AppConfig(BaseSettings):
    ENVIRONMENT: str = "dev"
    PORT: str = "8000"
    APP_NAME: str = "MyFastAPIApp"
    LOG_LEVEL: str = "INFO"
    ENABLE_REQUEST_BODY_LOGGING: bool = False
    ENABLE_COMPRESSION: bool = True
    COMPRESSION_MIN_SIZE_BYTES: int = 102400
    COMPRESSION_LEVEL: int = 6

    class Config:
        extra = "allow"
        env_file = ".env"
        env_file_encoding = "utf-8"


APP_CONFIG = AppConfig()
```

---

## 5. Config — `src/config/db_config.py`

```python
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class DBConfig(BaseSettings):
    DATABASE_URI: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "myapp_db"
    MONGODB_MAX_POOL_SIZE: int = 200
    MONGODB_MIN_POOL_SIZE: int = 10
    MONGODB_MAX_IDLE_TIME_MS: int = 30000
    MONGODB_CONNECT_TIMEOUT_MS: int = 10000
    MONGODB_SOCKET_TIMEOUT_MS: int = 60000
    MONGODB_SERVER_SELECTION_TIMEOUT_MS: int = 15000

    class Config:
        extra = "allow"
        env_file = ".env"
        env_file_encoding = "utf-8"


DB_CONFIG = DBConfig()
```

---

## 6. Logger — `src/utils/logger.py`

```python
from datetime import datetime
import logging
import sys
import json
from src.config.app_config import APP_CONFIG


class CustomFormatter(logging.Formatter):
    """Human-readable format for dev environments."""

    def format(self, record):
        record.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")[:-3]
        record.label = f"[{APP_CONFIG.APP_NAME}]"
        return super().format(record)


class JSONFormatter(logging.Formatter):
    """Structured JSON format for production environments."""

    def format(self, record):
        log_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")[:-3],
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
        }
        return json.dumps(log_entry)


def setup_logger(name: str) -> logging.Logger:
    root = logging.getLogger()
    root.handlers.clear()

    logger = logging.getLogger(name)
    logger.handlers.clear()

    log_level = APP_CONFIG.LOG_LEVEL.upper()
    logger.setLevel(log_level)
    root.setLevel(log_level)

    if not logger.hasHandlers():
        handler = logging.StreamHandler(sys.stdout)
        formatter = (
            CustomFormatter() if APP_CONFIG.ENVIRONMENT == "dev" else JSONFormatter()
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
```

---

## 7. Custom Exceptions — `src/utils/exceptions.py`

```python
from typing import Any, Dict, List, Optional


class CustomException(Exception):
    """Base exception for all service layer exceptions."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class AppException(CustomException):
    """Base exception for application-level errors."""

    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message, details)


class InvalidIdFormatError(AppException):
    """Raised when an ID format is invalid."""

    def __init__(self, entity_id: str, reason: Optional[str] = None):
        self.entity_id = entity_id
        message = f"Invalid ID format: {entity_id}"
        if reason:
            message += f" ({reason})"
        super().__init__(message, {"entity_id": entity_id, "reason": reason})


class EntityNotFoundError(AppException):
    """Raised when a requested entity is not found."""

    def __init__(self, entity_type: str, entity_id: str, message: Optional[str] = None):
        self.entity_type = entity_type
        self.entity_id = entity_id
        default_message = f"{entity_type} not found with ID: {entity_id}"
        super().__init__(
            message or default_message,
            {"entity_type": entity_type, "entity_id": entity_id},
        )


class ItemNotFoundError(EntityNotFoundError):
    def __init__(self, item_id: str, message: Optional[str] = None):
        super().__init__("Item", item_id, message)


class BatchOperationError(AppException):
    """Raised when a batch operation has partial failures."""

    def __init__(
        self,
        message: str,
        successful_ids: List[str],
        failed_ids: List[str],
        errors: Dict[str, str],
    ):
        self.successful_ids = successful_ids
        self.failed_ids = failed_ids
        self.errors = errors
        super().__init__(
            message,
            {
                "successful_ids": successful_ids,
                "failed_ids": failed_ids,
                "errors": errors,
            },
        )


class ValidationError(AppException):
    """Raised when validation fails."""

    def __init__(self, message: str, field: Optional[str] = None):
        self.field = field
        details = {"field": field} if field else {}
        super().__init__(message, details)
```

---

## 8. Global Exception Handler — `src/utils/global_exception_handler.py`

```python
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
    """Universal error handler for all exceptions."""

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
```

---

## 9. Request Context — `src/utils/request_context.py`

This replaces `genesis_common_utility.request_context`. Uses Python `contextvars` for per-request isolated state.

```python
from contextvars import ContextVar
from typing import Any

_store: ContextVar[dict] = ContextVar("request_context", default={})


class _RequestContext:
    def set(self, key: str, value: Any) -> None:
        ctx = _store.get({})
        _store.set({**ctx, key: value})

    def get(self, key: str, default: Any = None) -> Any:
        return _store.get({}).get(key, default)

    def clear(self) -> None:
        _store.set({})


request_context = _RequestContext()
```

---

## 10. Database Manager — `src/db/db_manager.py`

```python
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from src.config.db_config import DB_CONFIG
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class DatabaseManager:
    def __init__(self):
        self.client: AsyncIOMotorClient = None
        self.db = None

    def connect_db(self):
        self.client = AsyncIOMotorClient(
            DB_CONFIG.DATABASE_URI,
            maxPoolSize=DB_CONFIG.MONGODB_MAX_POOL_SIZE,
            minPoolSize=DB_CONFIG.MONGODB_MIN_POOL_SIZE,
            maxIdleTimeMS=DB_CONFIG.MONGODB_MAX_IDLE_TIME_MS,
            connectTimeoutMS=DB_CONFIG.MONGODB_CONNECT_TIMEOUT_MS,
            socketTimeoutMS=DB_CONFIG.MONGODB_SOCKET_TIMEOUT_MS,
            serverSelectionTimeoutMS=DB_CONFIG.MONGODB_SERVER_SELECTION_TIMEOUT_MS,
        )
        self.db = self.client[DB_CONFIG.DATABASE_NAME]
        logger.info(f"Connected to MongoDB: {DB_CONFIG.DATABASE_NAME}")

    async def close_db(self):
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed.")

    def get_collection(self, collection_name: str) -> AsyncIOMotorCollection:
        if self.db is None:
            raise RuntimeError("Database not initialized. Call connect_db() first.")
        return self.db[collection_name]


db_manager = DatabaseManager()
```

---

## 11. Base Repository — `src/repositories/base_repository.py`

```python
from typing import Any, Dict, List, Optional, Tuple
from motor.motor_asyncio import AsyncIOMotorCollection
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class BaseRepository:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def get_many_by_query(
        self,
        query: Dict[str, Any],
        sort: Optional[List[Tuple[str, int]]] = None,
        projection: Optional[Dict] = None,
    ) -> List[Dict[str, Any]]:
        try:
            cursor = self.collection.find(query, projection)
            if sort:
                cursor = cursor.sort(sort)
            return await cursor.to_list(length=None)
        except Exception as e:
            logger.error(f"get_many_by_query error: {e}", exc_info=True)
            raise

    async def get_one_by_query(
        self,
        query: Dict[str, Any],
        projection: Optional[Dict] = None,
    ) -> Optional[Dict[str, Any]]:
        try:
            return await self.collection.find_one(query, projection)
        except Exception as e:
            logger.error(f"get_one_by_query error: {e}", exc_info=True)
            raise

    async def insert_one(self, document: Dict[str, Any]) -> Dict[str, Any]:
        try:
            result = await self.collection.insert_one(document)
            return await self.collection.find_one({"_id": result.inserted_id})
        except Exception as e:
            logger.error(f"insert_one error: {e}", exc_info=True)
            raise

    async def update_one(
        self,
        query: Dict[str, Any],
        update_data: Dict[str, Any],
        projection: Optional[Dict] = None,
    ) -> Optional[Dict[str, Any]]:
        try:
            await self.collection.update_one(query, {"$set": update_data})
            return await self.collection.find_one(query, projection)
        except Exception as e:
            logger.error(f"update_one error: {e}", exc_info=True)
            raise

    async def delete_one(self, query: Dict[str, Any]) -> bool:
        try:
            result = await self.collection.delete_one(query)
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"delete_one error: {e}", exc_info=True)
            raise

    async def aggregate(
        self, pipeline: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        try:
            cursor = self.collection.aggregate(pipeline)
            return await cursor.to_list(length=None)
        except Exception as e:
            logger.error(f"aggregate error: {e}", exc_info=True)
            raise

    async def count(self, query: Dict[str, Any] = None) -> int:
        try:
            return await self.collection.count_documents(query or {})
        except Exception as e:
            logger.error(f"count error: {e}", exc_info=True)
            raise
```

---

## 12. Item Repository — `src/repositories/item_repository.py`

```python
from src.repositories.base_repository import BaseRepository


class ItemRepository(BaseRepository):
    """Repository for Item collection operations."""

    def __init__(self, collection):
        super().__init__(collection)

    async def find_by_name(self, name: str):
        return await self.get_one_by_query({"name": name})
```

---

## 13. Helper — `src/utils/helper.py`

```python
from typing import Optional


class Helper:
    @staticmethod
    def format_uptime(seconds: float) -> str:
        days = int(seconds // 86400)
        hours = int((seconds % 86400) // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        parts = []
        if days:
            parts.append(f"{days}d")
        if hours:
            parts.append(f"{hours}h")
        if minutes:
            parts.append(f"{minutes}m")
        parts.append(f"{secs}s")
        return " ".join(parts)

    @staticmethod
    def get_status_code_title(status_code: int) -> str:
        titles = {
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            409: "Conflict",
            422: "Unprocessable Entity",
            500: "Internal Server Error",
        }
        return titles.get(status_code, "Error")
```

---

## 14. Middlewares

### `src/middlewares/request_logger.py`

```python
import asyncio
from datetime import datetime
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
```

### `src/middlewares/date_format_middleware.py`

```python
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from src.utils.request_context import request_context

_ALLOWED = ("iso", "custom")
_DEFAULT = "custom"


class DateFormatMiddleware(BaseHTTPMiddleware):
    """Reads ?date_format=iso|custom and stores in request_context."""

    async def dispatch(self, request: Request, call_next):
        value = request.query_params.get("date_format", _DEFAULT)
        if value not in _ALLOWED:
            value = _DEFAULT
        request_context.set("date_format", value)
        return await call_next(request)
```

### `src/middlewares/external_api_middleware.py`

```python
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from src.utils.request_context import request_context


class ExternalApiMiddleware(BaseHTTPMiddleware):
    """Reads x-is-external header and stores in request_context.
    
    Defaults to True (external) when header is absent.
    """

    async def dispatch(self, request: Request, call_next):
        header_value = request.headers.get("x-is-external", "true").strip().lower()
        request_context.set("is_external_api", header_value == "true")
        return await call_next(request)
```

### `src/middlewares/middlewares.py`

```python
from fastapi import FastAPI
from starlette.middleware.gzip import GZipMiddleware
from .request_logger import RequestLoggerMiddleware
from .date_format_middleware import DateFormatMiddleware
from .external_api_middleware import ExternalApiMiddleware


def setup_middlewares(app: FastAPI):
    """Registers middlewares in order (outermost to innermost)."""

    # GZipMiddleware must be outermost to compress the final response
    app.add_middleware(GZipMiddleware, minimum_size=500)
    app.add_middleware(RequestLoggerMiddleware)
    app.add_middleware(DateFormatMiddleware)
    app.add_middleware(ExternalApiMiddleware)
```

> **Middleware order matters.** FastAPI applies them in reverse registration order (last added = first to run on request). The order above puts GZip outermost (wraps everything) and ExternalApi/DateFormat innermost (run first on request, set context for controllers).

---

## 15. Models

### `src/models/request/item.py`

```python
from pydantic import BaseModel
from typing import Optional


class CreateItemRequest(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    in_stock: bool = True


class UpdateItemRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    in_stock: Optional[bool] = None
```

### `src/models/response/item.py`

```python
from pydantic import BaseModel
from typing import Optional


class ItemResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    price: float
    in_stock: bool


class ItemListResponse(BaseModel):
    items: list[ItemResponse]
    total: int
```

---

## 16. Services

### `src/services/health.py`

```python
import os
import time
from typing import Dict, Any
import psutil
from src.utils.logger import setup_logger
from src.utils.helper import Helper

logger = setup_logger(__name__)


class HealthService:
    def __init__(self):
        self.start_time = time.time()

    async def check_system_health(self) -> Dict[str, Any]:
        process = psutil.Process()
        memory = process.memory_info()
        uptime = Helper.format_uptime(time.time() - self.start_time)

        return {
            "status": "up",
            "service": os.getenv("APP_NAME", "MyFastAPIApp"),
            "environment": os.getenv("ENVIRONMENT", "dev"),
            "uptime": uptime,
            "memory": {
                "rss": f"{memory.rss / (1024 * 1024):.2f} MB",
                "vms": f"{memory.vms / (1024 * 1024):.2f} MB",
                "percent": process.memory_percent(),
            },
            "cpu": {
                "percent": process.cpu_percent(interval=0.1),
                "threads": process.num_threads(),
            },
        }
```

### `src/services/item.py`

```python
from typing import Dict, Any, List, Optional
from bson import ObjectId
from src.repositories.item_repository import ItemRepository
from src.utils.exceptions import EntityNotFoundError, ValidationError
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class ItemService:
    def __init__(self, item_repository: ItemRepository):
        self.item_repository = item_repository

    def _serialize(self, doc: Dict) -> Dict:
        if doc and "_id" in doc:
            doc["id"] = str(doc.pop("_id"))
        return doc

    async def get_all(self) -> List[Dict[str, Any]]:
        docs = await self.item_repository.get_many_by_query({})
        return [self._serialize(d) for d in docs]

    async def get_by_id(self, item_id: str) -> Dict[str, Any]:
        if not ObjectId.is_valid(item_id):
            raise EntityNotFoundError("Item", item_id, "Invalid ID format")
        doc = await self.item_repository.get_one_by_query({"_id": ObjectId(item_id)})
        if not doc:
            raise EntityNotFoundError("Item", item_id)
        return self._serialize(doc)

    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if not data.get("name"):
            raise ValidationError("Item name is required", field="name")
        existing = await self.item_repository.find_by_name(data["name"])
        if existing:
            raise ValidationError(f"Item with name '{data['name']}' already exists")
        doc = await self.item_repository.insert_one(data)
        return self._serialize(doc)

    async def update(self, item_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        if not ObjectId.is_valid(item_id):
            raise EntityNotFoundError("Item", item_id, "Invalid ID format")
        query = {"_id": ObjectId(item_id)}
        doc = await self.item_repository.get_one_by_query(query)
        if not doc:
            raise EntityNotFoundError("Item", item_id)
        update_data = {k: v for k, v in data.items() if v is not None}
        updated = await self.item_repository.update_one(query, update_data)
        return self._serialize(updated)

    async def delete(self, item_id: str) -> bool:
        if not ObjectId.is_valid(item_id):
            raise EntityNotFoundError("Item", item_id, "Invalid ID format")
        query = {"_id": ObjectId(item_id)}
        doc = await self.item_repository.get_one_by_query(query)
        if not doc:
            raise EntityNotFoundError("Item", item_id)
        return await self.item_repository.delete_one(query)
```

---

## 17. Controllers

### `src/controllers/health.py`

```python
from fastapi import APIRouter, Request
from typing import Dict, Any
from src.containers import ApplicationContainer as Container
from src.services.health import HealthService
from src.utils.logger import setup_logger
from dependency_injector.wiring import inject, Provide

logger = setup_logger(__name__)


class HealthController:

    @inject
    def __init__(
        self,
        health_service: HealthService = Provide[Container.services.health_service],
    ):
        self.health_service = health_service
        self.router = APIRouter()
        self.setup_routes()

    def setup_routes(self):
        self.router.get("", response_model=Dict[str, Any], summary="System health check")(
            self.get_system_health
        )

    async def get_system_health(self, request: Request) -> Dict[str, Any]:
        return await self.health_service.check_system_health()
```

### `src/controllers/item.py`

```python
from fastapi import APIRouter, Request
from typing import Dict, Any, List
from src.containers import ApplicationContainer as Container
from src.services.item import ItemService
from src.models.request.item import CreateItemRequest, UpdateItemRequest
from src.utils.logger import setup_logger
from dependency_injector.wiring import inject, Provide

logger = setup_logger(__name__)


class ItemController:

    @inject
    def __init__(
        self,
        item_service: ItemService = Provide[Container.services.item_service],
    ):
        self.item_service = item_service
        self.router = APIRouter()
        self.setup_routes()

    def setup_routes(self):
        self.router.get("", summary="List all items")(self.get_all)
        self.router.get("/{item_id}", summary="Get item by ID")(self.get_by_id)
        self.router.post("", status_code=201, summary="Create item")(self.create)
        self.router.put("/{item_id}", summary="Update item")(self.update)
        self.router.delete("/{item_id}", status_code=204, summary="Delete item")(self.delete)

    async def get_all(self, request: Request) -> List[Dict[str, Any]]:
        return await self.item_service.get_all()

    async def get_by_id(self, item_id: str, request: Request) -> Dict[str, Any]:
        return await self.item_service.get_by_id(item_id)

    async def create(self, body: CreateItemRequest, request: Request) -> Dict[str, Any]:
        return await self.item_service.create(body.model_dump())

    async def update(
        self, item_id: str, body: UpdateItemRequest, request: Request
    ) -> Dict[str, Any]:
        return await self.item_service.update(item_id, body.model_dump())

    async def delete(self, item_id: str, request: Request) -> None:
        await self.item_service.delete(item_id)
```

---

## 18. DI Container — `src/containers.py`

```python
from dependency_injector import containers, providers
from src.services.health import HealthService
from src.services.item import ItemService
from src.repositories.item_repository import ItemRepository
from src.db.db_manager import db_manager


class Services(containers.DeclarativeContainer):
    health_service = providers.Singleton(HealthService)

    item_repository = providers.Singleton(
        ItemRepository,
        collection=providers.Callable(
            lambda: db_manager.get_collection("items")
        ),
    )

    item_service = providers.Singleton(
        ItemService,
        item_repository=item_repository,
    )


class ApplicationContainer(containers.DeclarativeContainer):
    services = providers.Container(Services)

    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.controllers.health",
            "src.controllers.item",
        ]
    )
```

> **To add a new service:** register the repository in `Services`, register the service with its injected dependencies, add the controller module to `wiring_config.modules`.

---

## 19. Routes — `src/routes.py`

```python
from fastapi import APIRouter, FastAPI
from typing import Protocol
from src.controllers.health import HealthController
from src.controllers.item import ItemController


class ControllerProtocol(Protocol):
    router: APIRouter


def setup_routes(app: FastAPI):
    root_router = APIRouter(prefix="/api/v1")

    controllers: list[tuple[ControllerProtocol, str, str]] = [
        (HealthController(), "/health", "Health"),
        (ItemController(), "/items", "Items"),
    ]

    for controller, route, name in controllers:
        root_router.include_router(controller.router, prefix=route, tags=[name])

    app.include_router(root_router)
```

> **To add a new resource:** instantiate its controller in the `controllers` list with a route prefix and tag name.

---

## 20. App Factory — `src/app.py`

```python
import asyncio
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.containers import ApplicationContainer as Container
from src.routes import setup_routes
from src.config.app_config import APP_CONFIG
from src.middlewares.middlewares import setup_middlewares
from src.db.db_manager import db_manager
from src.utils.logger import setup_logger
from src.utils.global_exception_handler import global_exception_handler

logger = setup_logger(__name__)

container = Container()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application.")
    try:
        # Connect to MongoDB
        db_manager.connect_db()

        # Run DB migrations if enabled
        auto_migrate = os.getenv("AUTO_MIGRATE", "true").lower() == "true"
        if auto_migrate:
            logger.info("Running database migrations...")
            # Add your migration runner here
            logger.info("Database migrations completed.")

        # Wire DI container
        container.wire(modules=container.wiring_config.modules)
        logger.info("Dependency injection container wired.")

    except Exception as e:
        logger.error(f"Failed to start application: {str(e)}")
        raise

    yield

    # Shutdown
    logger.info("Shutting down application.")
    try:
        container.unwire()
        await db_manager.close_db()
    except Exception as e:
        logger.error(f"Error during shutdown: {str(e)}")


def create_app() -> FastAPI:
    app = FastAPI(
        title=APP_CONFIG.APP_NAME,
        description="FastAPI Boilerplate Application",
        version="1.0.0",
        lifespan=lifespan,
    )

    # CORS — tighten allow_origins in production
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    setup_middlewares(app)
    setup_routes(app)

    # Register global exception handlers
    app.add_exception_handler(Exception, global_exception_handler)
    app.add_exception_handler(HTTPException, global_exception_handler)

    return app
```

---

## 21. Entry Point — `src/main.py`

```python
from src.app import create_app
from src.config.app_config import APP_CONFIG

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(APP_CONFIG.PORT), log_config=None)
```

Run: `uvicorn src.main:app --reload --port 8000`

---

## 22. All `__init__.py` Files

Create empty `__init__.py` in every directory:
- `src/__init__.py`
- `src/config/__init__.py`
- `src/controllers/__init__.py`
- `src/services/__init__.py`
- `src/repositories/__init__.py`
- `src/models/__init__.py`
- `src/models/request/__init__.py`
- `src/models/response/__init__.py`
- `src/db/__init__.py`
- `src/middlewares/__init__.py`
- `src/utils/__init__.py`

---

## 23. Architecture Patterns Reference

### Request Flow
```
Client → CORS → GZip → RequestLogger → DateFormat → ExternalApi
       → Router → Controller → Service → Repository → MongoDB
       ← Repository ← Service ← Controller ← Router ← Response
```

### Controller Pattern
- `@inject` on `__init__`
- Services injected via `Provide[Container.services.xxx]`
- `self.router = APIRouter()` created in `__init__`
- Routes registered in `setup_routes()` method
- All handlers are `async def`

### Service Pattern
- Inject repositories in `__init__`
- Business logic only — no HTTP concerns
- Raise custom exceptions (`EntityNotFoundError`, `ValidationError`, etc.)
- Never raise `HTTPException` — let the global handler translate

### Repository Pattern
- Extend `BaseRepository`
- Pass MongoDB collection in `__init__`
- Add domain-specific query methods
- No business logic — data access only

### DI Container Pattern
- `providers.Singleton` for stateful services/repos
- `providers.Callable` for collection factories (lazy MongoDB access)
- Wire controller modules in `wiring_config.modules`
- `container.wire()` on startup, `container.unwire()` on shutdown

### Exception → HTTP Mapping
| Exception | HTTP Status |
|---|---|
| `EntityNotFoundError` | 404 |
| `InvalidIdFormatError` | 400 |
| `ValidationError` | 400 |
| `BatchOperationError` | 207 |
| `AppException` | 400 |
| `HTTPException` | (as-is) |
| Any `Exception` | 500 |

### Logging Pattern
- `setup_logger(__name__)` at module level
- `dev` env → human-readable `CustomFormatter`
- Non-dev → JSON `JSONFormatter` (structured for log aggregators)
- Never log sensitive data or large binary payloads

### Middleware Registration Order (reversed at runtime)
```python
app.add_middleware(GZipMiddleware)        # runs last (outermost)
app.add_middleware(RequestLoggerMiddleware)
app.add_middleware(DateFormatMiddleware)
app.add_middleware(ExternalApiMiddleware) # runs first (innermost)
```

### `request_context` Usage
```python
from src.utils.request_context import request_context

# In middleware
request_context.set("date_format", "iso")

# In service/controller
date_format = request_context.get("date_format", "custom")
is_external = request_context.get("is_external_api", True)
```

---

## 24. Quick Checklist for Adding a New Resource

1. Create `src/models/request/myresource.py` — Pydantic request models
2. Create `src/models/response/myresource.py` — Pydantic response models
3. Create `src/repositories/myresource_repository.py` — extend `BaseRepository`
4. Create `src/services/myresource.py` — business logic, inject repository
5. Create `src/controllers/myresource.py` — inject service, define routes
6. Register in `src/containers.py` — add repository + service as `Singleton`
7. Add controller module to `wiring_config.modules` in `containers.py`
8. Add controller instance to `controllers` list in `src/routes.py`
