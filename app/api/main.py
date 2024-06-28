import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes.register import register_router
from app.infra.orm import start_mappers

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """Starts the mappers when the application starts."""
    start_mappers()
    yield


logger.info("Setting up application")

app = FastAPI(lifespan=lifespan)

app.include_router(register_router, prefix="/register", tags=["register"])
