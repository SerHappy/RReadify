from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.associations import book_category
from app.models.base import Base


class BookORM(Base):
    """Book ORM model."""

    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    cover: Mapped[str | None] = mapped_column(Text)
    isbn: Mapped[str] = mapped_column(String(13), nullable=False)
    published_year: Mapped[int] = mapped_column(nullable=False)
    pages: Mapped[int] = mapped_column(nullable=False)

    categories = relationship(
        "CategoryORM",
        secondary=book_category,
        back_populates="books",
    )
    reviews = relationship("ReviewORM", back_populates="book")
