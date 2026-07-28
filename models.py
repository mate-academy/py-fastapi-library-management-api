from datetime import date
from typing import List

from sqlalchemy import Date, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Author(Base):
    __tablename__ = "author"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)
    bio: Mapped[str] = mapped_column(String(150))

    books: Mapped[List["Book"]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan",
    )


class Book(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(60))
    summary: Mapped[str] = mapped_column(String(150))

    publication_date: Mapped[date] = mapped_column(
        Date,
        server_default=func.current_date(),
    )

    author_id: Mapped[int] = mapped_column(
        ForeignKey("author.id")
    )

    author: Mapped["Author"] = relationship(
        back_populates="books"
    )