from __future__ import annotations

import datetime
from typing import List

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, relationship, mapped_column

from database import Base


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)

    books: Mapped[List["Book"]] = relationship(
        back_populates="author"
    )


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    publication_date: Mapped[datetime.date] = mapped_column(nullable=False)

    author_id: Mapped[int] = mapped_column(
        ForeignKey("authors.id"),
        nullable=False,
    )

    author: Mapped["Author"] = relationship(
        back_populates="books"
    )
