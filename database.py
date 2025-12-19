from datetime import datetime, date
from typing import List

from sqlalchemy import String, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from engine import Base


class Book(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    summary: Mapped[str] = mapped_column(String(255))
    publication_date: date = mapped_column(Date)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"), nullable=False)

    author: Mapped["Author"] = relationship(back_populates="books")


class Author(Base):
    __tablename__ = "authors"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    bio: Mapped[str] = mapped_column(String(300))
    books: Mapped[list["Book"]] = relationship(back_populates="author", cascade="all, delete-orphan")

