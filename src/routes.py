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
