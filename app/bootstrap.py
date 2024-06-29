import logging

from app.infra.orm import start_mappers

logger = logging.getLogger(__name__)


def bootstrap() -> None:
    """Loads the application configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )

    logger.info("Setting up application")
    start_mappers()
