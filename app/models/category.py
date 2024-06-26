from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.associations import book_category
from app.models.base import Base


class CategoryORM(Base):
    """Category ORM model."""

    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)

    books = relationship(
        "BookORM",
        secondary=book_category,
        back_populates="categories",
    )
