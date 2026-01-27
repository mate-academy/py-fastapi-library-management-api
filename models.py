from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List
from datetime import date
from database import Base

class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    bio: Mapped[str | None] = mapped_column(nullable=True)
    books: Mapped[List["Book"]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan"
    )

class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    summary: Mapped[str | None]
    publication_date: Mapped[date | None]
    author_id: Mapped[int] = mapped_column(
        ForeignKey("authors.id")
    )
    author: Mapped["Author"] = relationship(
        back_populates="books"
    )
