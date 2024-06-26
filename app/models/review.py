from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class ReviewORM(Base):
    """Review ORM model."""

    __tablename__ = "review"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"), nullable=False)
    rating: Mapped[int] = mapped_column(nullable=False)

    user = relationship("UserORM", back_populates="reviews")
    book = relationship("BookORM", back_populates="reviews")
