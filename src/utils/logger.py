from datetime import datetime
import logging
import sys
import json
from src.config.app_config import APP_CONFIG


class CustomFormatter(logging.Formatter):
    def format(self, record):
        record.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")[:-3]
        record.label = f"[{APP_CONFIG.APP_NAME}]"
        return super().format(record)


class JSONFormatter(logging.Formatter):
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
