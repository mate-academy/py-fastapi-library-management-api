from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy import String, ForeignKey, Date
from typing import List
from datetime import date

from database import Base


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(48), unique=True)
    bio: Mapped[str] = mapped_column(String(512))
    books: Mapped[List["Book"]] = relationship(
        "Book",
        back_populates="author",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"{self.name} ({self.id})"


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(48), unique=True)
    summary: Mapped[str] = mapped_column(String(512))
    publication_date: Mapped[date] = mapped_column(Date())
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    author: Mapped[Author] = relationship("Author", back_populates="books")
