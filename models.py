from datetime import date
from typing import List

from sqlalchemy import String, ForeignKey, Date
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from database import Base


class DBAuthor(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=True)
    bio: Mapped[str] = mapped_column(String(499))
    books: Mapped[List["DBBook"]] = relationship(back_populates="author")


class DBBook(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(99), nullable=False)
    summary: Mapped[str] = mapped_column(String(255), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    author: Mapped["DBAuthor"] = relationship(back_populates="books")
    publication_date: Mapped[date] = mapped_column(Date, nullable=True)
