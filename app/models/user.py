from sqlalchemy import String
from sqlalchemy.dialects.postgresql import CITEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class UserORM(Base):
    """User ORM model."""

    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(CITEXT(320), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(60), nullable=False)
    is_verified: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
    )
    is_superuser: Mapped[bool] = mapped_column(default=False, nullable=False)

    reviews = relationship("ReviewORM", back_populates="user")
