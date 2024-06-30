import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.middlewares.duration import request_duration
from app.api.routes.auth import auth_router
from app.api.routes.register import register_router
from app.bootstrap import bootstrap

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """Context manager to start and stop the application."""
    bootstrap()
    yield
    logger.info("Shutting down application")


app = FastAPI(lifespan=lifespan)

app.middleware("http")(request_duration)
app.include_router(register_router, prefix="/register", tags=["register"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])
