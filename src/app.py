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
        # db_manager.connect_db()

        auto_migrate = os.getenv("AUTO_MIGRATE", "true").lower() == "true"
        if auto_migrate:
            logger.info("Running database migrations...")
            logger.info("Database migrations completed.")

        container.wire(modules=container.wiring_config.modules)
        logger.info("Dependency injection container wired.")

    except Exception as e:
        logger.error(f"Failed to start application: {str(e)}")
        raise

    yield

    logger.info("Shutting down application.")
    try:
        container.unwire()
        await db_manager.close_db()
    except Exception as e:
        logger.error(f"Error during shutdown: {str(e)}")


def create_app() -> FastAPI:
    app = FastAPI(
        title=APP_CONFIG.APP_NAME,
        description="Universal RAG Application",
        version="1.0.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    setup_middlewares(app)
    setup_routes(app)

    app.add_exception_handler(Exception, global_exception_handler)
    app.add_exception_handler(HTTPException, global_exception_handler)

    return app
