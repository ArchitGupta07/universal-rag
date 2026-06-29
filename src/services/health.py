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
            "service": os.getenv("APP_NAME", "UniversalRAG"),
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
