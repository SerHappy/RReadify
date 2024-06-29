from app.infra.orm import start_mappers


def bootstrap() -> None:
    """Loads the application configuration."""
    start_mappers()
