from sqlalchemy import Column, Integer, Table

from app.models.base import Base

book_category = Table(
    "book_category",
    Base.metadata,
    Column("book_id", Integer, primary_key=True),
    Column("category_id", Integer, primary_key=True),
)
