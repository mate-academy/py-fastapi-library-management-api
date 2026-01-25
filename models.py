from typing import List

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from datetime import date

from database import Base


class Author(Base):
    __tablename__ = "author"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    bio: Mapped[str] = mapped_column(String(255))
    books: Mapped[List["Book"]] = relationship(
        back_populates="author")


class Book(Base):
    __tablename__ = "book"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(50))
    summary: Mapped[str] = mapped_column(String(255))
    publication_date: Mapped[date]
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"))
    author: Mapped["Author"] = relationship(back_populates="books")
