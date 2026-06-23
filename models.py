from datetime import date
from typing import List
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    bio: Mapped[str | None] = mapped_column(String, nullable=True)

    books: Mapped[List["Book"]] = relationship(back_populates="author")


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True, nullable=False)
    summary: Mapped[str | None] = mapped_column(String, nullable=True)
    publication_date: Mapped[date | None] = mapped_column(nullable=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"), nullable=False)

    author: Mapped["Author"] = relationship(back_populates="books")
