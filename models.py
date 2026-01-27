from datetime import date
from typing import List

from sqlalchemy import Integer, String, func, ForeignKey, Text
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    relationship,
    mapped_column
)


class Base(DeclarativeBase):
    pass


class Author(Base):
    __tablename__ = "author"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    bio: Mapped[str] = mapped_column(Text)
    books: Mapped[List["Book"]] = relationship(back_populates="author")


class Book(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(50))
    summary: Mapped[str] = mapped_column(Text)
    publication_date: Mapped[date] = mapped_column(
        server_default=func.current_date()
    )
    author: Mapped["Author"] = relationship(back_populates="books")
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"))
