import uuid

from sqlalchemy import Boolean, Column, String, Table
from sqlalchemy.dialects.postgresql import CITEXT
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import registry

from app.domain.user.entity import User

mapper_registry = registry()


user = Table(
    "users",
    mapper_registry.metadata,
    Column("id", PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("email", CITEXT(320), nullable=False, unique=True),
    Column("password", String(60), nullable=False),
    Column(
        "is_verified",
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
    ),
    Column(
        "is_superuser",
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
    ),
)


def start_mappers() -> None:
    """Starts the mappers for the domain entities."""
    mapper_registry.map_imperatively(
        User,
        user,
        properties={"hashed_password": user.c.password},
    )
