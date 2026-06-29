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
